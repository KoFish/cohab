from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils.timezone import now
from django.db import models
from django.template.defaultfilters import slugify


class TaskArea(models.Model):
    slug = models.SlugField(unique=True, max_length=255, editable=False)
    name = models.CharField(_('name'), max_length=255, unique=True, db_index=True)
    owner = models.ForeignKey(User, null=True, blank=True, related_name="areas")

    def has_task(self):
        return self.tasks.filter(completed__isnull=True).exists()
    has_task.boolean = True

    def __unicode__(self):
        return self.name

    def save(self, *a, **kw):
        if not self.slug:
            new_slug = slug = slugify(self.name)
            slug_count = 0
            while TaskArea.objects.filter(slug=new_slug).exists():
                slug_count += 1
                new_slug = slug + "-" + slug_count
            self.slug = new_slug
        super(TaskArea, self).save(*a, **kw)


class TaskAction(models.Model):
    slug = models.SlugField(unique=True, max_length=255, editable=False)
    name = models.CharField(_('name'), max_length=255, unique=True)
    has_area = models.BooleanField(_('has area'), default=False)
    listable = models.BooleanField(_('listable'), default=False)

    def has_task(self):
        return self.tasks.filter(completed__isnull=True).exists()
    has_task.boolean = True

    def __unicode__(self):
        return self.name

    def save(self, *a, **kw):
        if not self.slug:
            new_slug = slug = slugify(self.name)
            slug_count = 0
            while TaskAction.objects.filter(slug=new_slug).exists():
                slug_count += 1
                new_slug = slug + "-" + slug_count
            self.slug = new_slug
        super(TaskAction, self).save(*a, **kw)


class Task(models.Model):
    action = models.ForeignKey(TaskAction, verbose_name=_('action'), related_name="tasks")
    object = models.CharField(_('object'), max_length=255, blank=True, null=True)
    area = models.ForeignKey(TaskArea, related_name="tasks", verbose_name=_('area'), blank=True, null=True)
    deadline = models.DateTimeField(_('deadline'), blank=True, null=True)
    owner = models.ForeignKey(User, verbose_name=_('owner'), related_name="owned_tasks", blank=True, null=True)
    assigned = models.ForeignKey(User, verbose_name=_('assignee'), related_name="tasks", blank=True, null=True)
    completedby = models.ForeignKey(User, blank=True, null=True, verbose_name=_('completed by'), related_name="completed")
    completed = models.DateTimeField(_('completed'), blank=True, null=True)
    added = models.DateTimeField(_('added'), editable=False)
    modified = models.DateTimeField(_('modified'), editable=False)
    repeater = models.ForeignKey('RepeatingTask', blank=True, null=True, related_name="tasks", editable=False, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-completed', 'deadline', '-added']

    def is_completed(self):
        return bool(self.completed)
    is_completed.boolean = True

    def is_repeating(self):
        return bool(self.repeater)
    is_repeating.boolean = True

    @property
    def days_left(self):
        return (self.deadline - now()).days

    @property
    def name(self):
        return ("%s %s" % (self.action.name, (self.area.name if self.area else None) or self.object or "")).strip()

    def __unicode__(self):
        return "%s (%s: %s)" % (self.name,
                "completed" if self.completed else "deadline",
                self.completed or self.deadline)

    def save(self, *a, **kw):
        if not self.id:
            self.added = now()
        if not self.assigned:
            self.assigned = self.owner
        self.modified = now()
        return super(Task, self).save(*a, **kw)

    def complete(self, request=None):
        if self.completed:
            raise Exception("This task has already been completed")
        user = request.user if request else self.assigned or self.owner
        self.completed = now()
        self.completedby = user
        self.save()
        if self.repeater:
            self.repeater.queue()

    def claim(self, request=None):
        if self.owner:
            raise Exception("This task is already claimed")
        if request and request.user:
            self.owner = request.user
            self.save()
        else:
            raise Exception("You are nobody, you can't claim anything.")

    def assign_to(self, user):
        self.assigned = user
        self.save()


class RepeatingTask(models.Model):
    action = models.ForeignKey(TaskAction, related_name="repeated_tasks")
    object = models.CharField(_('object'), max_length=255, blank=True, null=True)
    area = models.ForeignKey(TaskArea, related_name="repeated_tasks", blank=True, null=True)
    delay = models.IntegerField(_('days to delay'), blank=True, null=True)
    require_completed = models.BooleanField(_('require completed'),
                                            default=True,
                                            help_text=_('Require that all instances of this '
                                                        'task should have been completed '
                                                        'before adding another.'))
    deadline = models.IntegerField(_('days from start to deadline'), blank=True, null=True)
    modified = models.DateTimeField(_('modified'), editable=False)

    class Meta:
        ordering = ['-modified']

    @property
    def name(self):
        return ("Repeating: %s %s" % (self.action.name, (self.area.name if self.area else None) or self.object or "")).strip()

    def has_instance(self):
        return bool(self.get_last_instance())
    has_instance.boolean = True

    def get_last_instance(self):
        tasks = self.tasks.filter(completed__isnull=True)
        if tasks.exists():
            return tasks.latest('added')
        else:
            return None

    def get_next_owner(self):
        if self.area and self.area.owner:
            return self.area.owner
        else:
            tasks = self.tasks.filter(completed__isnull=False).order_by('-completed')
            users = list(User.objects.filter(is_active=True))
            for task in tasks:
                if len(users) == 1:
                    return users[0]
                if task.completedby in users:
                    users.remove(task.completedby)
            if users:
                user = sorted([(u.tasks.filter(completed__isnull=True).count(), u) for u in users], key=lambda k: k[0])[0][1]
                return user
            else:
                return None

    @property
    def days_to_next(self):
        if not self.delay or not self.tasks.exists() or self.tasks.filter(completed__isnull=True).exists():
            return None
        return (timedelta(days=self.delay) - (now() - self.tasks.latest('completed').completed)).days

    def __unicode__(self):
        return "<RepeatTask: %s %s>" % (self.action.name, self.object or self.area or "")

    def create_task(self):
        if not (self.get_last_instance() and self.require_completed):
            Task.objects.create(action=self.action,
                                object=self.object or None,
                                area=self.area,
                                deadline=now() + timedelta(days=self.deadline),
                                owner=self.get_next_owner(),
                                repeater=self)

    def queue(self):
        pass  # TODO: Add logic for queueing up the creation of a new instance

    def save(self, *a, **kw):
        self.modified = now()
        return super(RepeatingTask, self).save(*a, **kw)

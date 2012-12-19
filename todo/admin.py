from django.contrib import admin
from todo.models import TaskArea, TaskAction
from todo.models import Task, RepeatingTask


class TaskAreaAdmin(admin.ModelAdmin):
    fields = ('name', 'owner')


class TaskActionAdmin(admin.ModelAdmin):
    fields = ('name', 'has_area')


class TaskObjectAdmin(admin.ModelAdmin):
    fields = ('type', 'options')


class TaskAdmin(admin.ModelAdmin):
    list_filter = ['added', 'modified', 'deadline', 'completed']
    list_display = ['name', 'days_left', 'is_repeating', 'is_completed',
                    'owner', 'assigned', 'deadline', 'completed']
    excludes = ('modified', 'added')
    fieldsets = (
            (None, {'fields': ('action', 'area', 'object', 'owner', 'deadline')}),
            ("Status", {'fields': ('completed', 'completedby', 'assigned')}))

    actions = ['make_completed', 'make_not_completed']

    def make_completed(self, request, queryset):
        for t in queryset.all():
            t.complete(request=request)
    make_completed.short_description = "Make tasks completed"

    def make_not_completed(self, request, queryset):
        queryset.update(completed=None, completedby=None)
    make_not_completed.short_description = "Make tasks not completed"


class RepeatingTaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'has_instance', 'days_to_next']
    actions = ['make_new_instance', 'add_to_queue']

    def make_new_instance(self, request, queryset):
        for t in queryset.all():
            t.create_task()
    make_new_instance.short_description = "Make new instance of repeating task"

    def add_to_queue(self, request, queryset):
        for t in queryset.all():
            t.queue()
    add_to_queue.short_description = "Add to queue for creating new instance"


admin.site.register(Task, TaskAdmin)
admin.site.register(RepeatingTask, RepeatingTaskAdmin)
admin.site.register(TaskArea, TaskAreaAdmin)
admin.site.register(TaskAction, TaskActionAdmin)

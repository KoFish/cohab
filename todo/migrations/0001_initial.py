# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TaskArea'
        db.create_table('todo_taskarea', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='areas', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('todo', ['TaskArea'])

        # Adding model 'TaskAction'
        db.create_table('todo_taskaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('has_area', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('todo', ['TaskAction'])

        # Adding model 'Task'
        db.create_table('todo_task', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tasks', to=orm['todo.TaskAction'])),
            ('object', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tasks', null=True, to=orm['todo.TaskArea'])),
            ('deadline', self.gf('django.db.models.fields.DateTimeField')()),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tasks', to=orm['auth.User'])),
            ('checkedoutby', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='checkouts', null=True, to=orm['auth.User'])),
            ('checkedout', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('completedby', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='completed', null=True, to=orm['auth.User'])),
            ('completed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('added', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('repeater', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tasks', null=True, to=orm['todo.RepeatingTask'])),
        ))
        db.send_create_signal('todo', ['Task'])

        # Adding model 'RepeatingTask'
        db.create_table('todo_repeatingtask', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(related_name='repeated_tasks', to=orm['todo.TaskAction'])),
            ('object', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='repeated_tasks', null=True, to=orm['todo.TaskArea'])),
            ('delay', self.gf('django.db.models.fields.IntegerField')()),
            ('require_completed', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('deadline', self.gf('django.db.models.fields.IntegerField')()),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('todo', ['RepeatingTask'])


    def backwards(self, orm):
        # Deleting model 'TaskArea'
        db.delete_table('todo_taskarea')

        # Deleting model 'TaskAction'
        db.delete_table('todo_taskaction')

        # Deleting model 'Task'
        db.delete_table('todo_task')

        # Deleting model 'RepeatingTask'
        db.delete_table('todo_repeatingtask')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'todo.repeatingtask': {
            'Meta': {'ordering': "['-modified']", 'object_name': 'RepeatingTask'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'repeated_tasks'", 'to': "orm['todo.TaskAction']"}),
            'area': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repeated_tasks'", 'null': 'True', 'to': "orm['todo.TaskArea']"}),
            'deadline': ('django.db.models.fields.IntegerField', [], {}),
            'delay': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'object': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'require_completed': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'todo.task': {
            'Meta': {'ordering': "['-completed', '-deadline', '-checkedout', '-added']", 'object_name': 'Task'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks'", 'to': "orm['todo.TaskAction']"}),
            'added': ('django.db.models.fields.DateTimeField', [], {}),
            'area': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tasks'", 'null': 'True', 'to': "orm['todo.TaskArea']"}),
            'checkedout': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'checkedoutby': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'checkouts'", 'null': 'True', 'to': "orm['auth.User']"}),
            'completed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'completedby': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'completed'", 'null': 'True', 'to': "orm['auth.User']"}),
            'deadline': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'object': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks'", 'to': "orm['auth.User']"}),
            'repeater': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tasks'", 'null': 'True', 'to': "orm['todo.RepeatingTask']"})
        },
        'todo.taskaction': {
            'Meta': {'object_name': 'TaskAction'},
            'has_area': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'todo.taskarea': {
            'Meta': {'object_name': 'TaskArea'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'areas'", 'null': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['todo']
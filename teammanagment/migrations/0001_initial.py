# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Team'
        db.create_table('teammanagment_team', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('manager', self.gf('django.db.models.fields.related.ForeignKey')(related_name='manager', to=orm['auth.User'])),
            ('team_lead', self.gf('django.db.models.fields.related.ForeignKey')(related_name='team_lead', to=orm['auth.User'])),
        ))
        db.send_create_signal('teammanagment', ['Team'])

        # Adding model 'DeveloperTeam'
        db.create_table('teammanagment_developerteam', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teammanagment.Team'])),
            ('developer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('teammanagment', ['DeveloperTeam'])

        # Adding model 'Sprint'
        db.create_table('teammanagment_sprint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('teammanagment', ['Sprint'])

        # Adding model 'TaskCategory'
        db.create_table('teammanagment_taskcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('icon', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
        ))
        db.send_create_signal('teammanagment', ['TaskCategory'])

        # Adding model 'Task'
        db.create_table('teammanagment_task', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('sprint', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teammanagment.Sprint'])),
            ('desc', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teammanagment.TaskCategory'])),
            ('developer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teammanagment.DeveloperTeam'], null=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date_theory', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end_date_actual', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('teammanagment', ['Task'])

        # Adding model 'DailyTask'
        db.create_table('teammanagment_dailytask', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('day', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('teammanagment', ['DailyTask'])

        # Adding model 'ItemDailyTask'
        db.create_table('teammanagment_itemdailytask', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tasks', to=orm['teammanagment.DailyTask'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teammanagment.Task'], null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('teammanagment', ['ItemDailyTask'])


    def backwards(self, orm):
        # Deleting model 'Team'
        db.delete_table('teammanagment_team')

        # Deleting model 'DeveloperTeam'
        db.delete_table('teammanagment_developerteam')

        # Deleting model 'Sprint'
        db.delete_table('teammanagment_sprint')

        # Deleting model 'TaskCategory'
        db.delete_table('teammanagment_taskcategory')

        # Deleting model 'Task'
        db.delete_table('teammanagment_task')

        # Deleting model 'DailyTask'
        db.delete_table('teammanagment_dailytask')

        # Deleting model 'ItemDailyTask'
        db.delete_table('teammanagment_itemdailytask')


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
        'teammanagment.dailytask': {
            'Meta': {'object_name': 'DailyTask'},
            'day': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'teammanagment.developerteam': {
            'Meta': {'object_name': 'DeveloperTeam'},
            'developer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teammanagment.Team']"})
        },
        'teammanagment.itemdailytask': {
            'Meta': {'object_name': 'ItemDailyTask'},
            'day': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks'", 'to': "orm['teammanagment.DailyTask']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teammanagment.Task']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'teammanagment.sprint': {
            'Meta': {'object_name': 'Sprint'},
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        'teammanagment.task': {
            'Meta': {'object_name': 'Task'},
            'desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'developer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teammanagment.DeveloperTeam']", 'null': 'True'}),
            'end_date_actual': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'end_date_theory': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sprint': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teammanagment.Sprint']"}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teammanagment.TaskCategory']"})
        },
        'teammanagment.taskcategory': {
            'Meta': {'object_name': 'TaskCategory'},
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'teammanagment.team': {
            'Meta': {'object_name': 'Team'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manager': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'manager'", 'to': "orm['auth.User']"}),
            'team_lead': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_lead'", 'to': "orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        }
    }

    complete_apps = ['teammanagment']
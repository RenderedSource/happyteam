# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MergeMaster'
        db.create_table('mergemaster_mergemaster', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('jabber', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
        ))
        db.send_create_signal('mergemaster', ['MergeMaster'])

        # Adding model 'MergeRequest'
        db.create_table('mergemaster_mergerequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('developer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('branch', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('task_id', self.gf('django.db.models.fields.IntegerField')()),
            ('status_code', self.gf('django.db.models.fields.CharField')(default='pending', max_length=20)),
            ('cr_required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('qa_required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('mergemaster', ['MergeRequest'])

        # Adding model 'MergeRequestAction'
        db.create_table('mergemaster_mergerequestaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('merge_request', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mergemaster.MergeRequest'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('action_code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('mergemaster', ['MergeRequestAction'])

        # Adding model 'MergeNotification'
        db.create_table('mergemaster_mergenotification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('request', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=60)),
        ))
        db.send_create_signal('mergemaster', ['MergeNotification'])

        # Adding model 'JabberMessage'
        db.create_table('mergemaster_jabbermessage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('jabber', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('mergemaster', ['JabberMessage'])


    def backwards(self, orm):
        # Deleting model 'MergeMaster'
        db.delete_table('mergemaster_mergemaster')

        # Deleting model 'MergeRequest'
        db.delete_table('mergemaster_mergerequest')

        # Deleting model 'MergeRequestAction'
        db.delete_table('mergemaster_mergerequestaction')

        # Deleting model 'MergeNotification'
        db.delete_table('mergemaster_mergenotification')

        # Deleting model 'JabberMessage'
        db.delete_table('mergemaster_jabbermessage')


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
        'mergemaster.jabbermessage': {
            'Meta': {'object_name': 'JabberMessage'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jabber': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'mergemaster.mergemaster': {
            'Meta': {'object_name': 'MergeMaster'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jabber': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'mergemaster.mergenotification': {
            'Meta': {'object_name': 'MergeNotification'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'request': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'mergemaster.mergerequest': {
            'Meta': {'object_name': 'MergeRequest'},
            'branch': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'cr_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'developer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'qa_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'status_code': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '20'}),
            'task_id': ('django.db.models.fields.IntegerField', [], {})
        },
        'mergemaster.mergerequestaction': {
            'Meta': {'object_name': 'MergeRequestAction'},
            'action_code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'merge_request': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mergemaster.MergeRequest']"}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['mergemaster']
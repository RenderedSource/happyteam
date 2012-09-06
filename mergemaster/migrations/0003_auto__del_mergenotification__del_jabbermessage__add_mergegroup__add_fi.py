# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'MergeNotification'
        db.delete_table('mergemaster_mergenotification')

        # Deleting model 'JabberMessage'
        db.delete_table('mergemaster_jabbermessage')

        # Adding model 'MergeGroup'
        db.create_table('mergemaster_mergegroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('main_branch', self.gf('django.db.models.fields.CharField')(max_length=60)),
        ))
        db.send_create_signal('mergemaster', ['MergeGroup'])

        # Adding field 'MergeRequest.merge_group'
        db.add_column('mergemaster_mergerequest', 'merge_group',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mergemaster.MergeGroup'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'MergeNotification'
        db.create_table('mergemaster_mergenotification', (
            ('request', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('mergemaster', ['MergeNotification'])

        # Adding model 'JabberMessage'
        db.create_table('mergemaster_jabbermessage', (
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('jabber', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('mergemaster', ['JabberMessage'])

        # Deleting model 'MergeGroup'
        db.delete_table('mergemaster_mergegroup')

        # Deleting field 'MergeRequest.merge_group'
        db.delete_column('mergemaster_mergerequest', 'merge_group_id')


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
        'mergemaster.mergeactioncomment': {
            'Meta': {'object_name': 'MergeActionComment'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'merge_action': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mergemaster.MergeRequestAction']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'mergemaster.mergegroup': {
            'Meta': {'object_name': 'MergeGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_branch': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'mergemaster.mergemaster': {
            'Meta': {'object_name': 'MergeMaster'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jabber': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
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
            'merge_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mergemaster.MergeGroup']", 'null': 'True'}),
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
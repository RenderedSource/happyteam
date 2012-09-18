# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        REQUIRED = 0
        IN_PROGRESS = 1
        REJECTED = 2
        APPROVED = 3
        IDLE = 4
        REQUEST_PENDING = 0
        REQUEST_REJECTED = 1
        REQUEST_MERGED = 2
        REQUEST_SUSPENDED = 3

        for request in orm['mergemaster.mergerequest'].objects.all():
            if request.status_code == 'pending':
                request.merge_status = REQUEST_PENDING
                request.cr_status = REQUIRED if request.cr_required else APPROVED
                request.qa_status = REQUIRED if request.qa_required else APPROVED
            elif request.status_code == 'cr_in_progress':
                request.merge_status = REQUEST_PENDING
                request.cr_status = IN_PROGRESS
                request.qa_status = REQUIRED if request.qa_required else APPROVED
            elif request.status_code ==  'qa_in_progress':
                request.merge_status = REQUEST_PENDING
                request.qa_status = IN_PROGRESS
                request.cr_status = REQUIRED if request.cr_required else APPROVED
            elif request.status_code ==  'rejected':
                request.merge_status = REQUEST_REJECTED
                request.cr_status = REJECTED
                request.qa_status = REJECTED
            elif request.status_code ==  'approved':
                request.merge_status = REQUEST_PENDING
                request.cr_status = APPROVED
                request.qa_status = APPROVED
                pass
            elif request.status_code ==  'merged':
                request.merge_status = REQUEST_MERGED
                request.cr_status = APPROVED
                request.qa_status = APPROVED
                pass
            elif request.status_code ==  'canceled':
                request.merge_status = REQUEST_SUSPENDED
                request.cr_status = IDLE
                request.qa_status = IDLE
                pass

            request.save()

            old_request_status = None
            for action in request.mergerequestaction_set.all().order_by('id'):
                new_request_status = None
                if action.action_code == 'request_merge':
                    new_request_status = REQUEST_PENDING
                    action.new_cr_status = REQUIRED
                    action.new_qa_status = REQUIRED
                elif action.action_code == 'reject':
                    new_request_status = REQUEST_REJECTED
                    action.new_cr_status = REJECTED
                    action.new_qa_status = REJECTED
                elif action.action_code == 'start_cr':
                    new_request_status = REQUEST_PENDING
                    action.new_cr_status = IN_PROGRESS
                elif action.action_code == 'approve_cr':
                    new_request_status = REQUEST_PENDING
                    action.new_cr_status = APPROVED
                    action.new_qa_status = None
                elif action.action_code == 'start_qa':
                    new_request_status = REQUEST_PENDING
                    action.new_cr_status = None
                    action.new_qa_status = IN_PROGRESS
                elif action.action_code == 'approve_qa':
                    new_request_status = REQUEST_PENDING
                    action.new_cr_status = None
                    action.new_qa_status = APPROVED
                elif action.action_code == 'merge':
                    new_request_status = REQUEST_MERGED
                    action.new_cr_status = None
                    action.new_qa_status = APPROVED
                elif action.action_code == 'cancel':
                    new_request_status = REQUEST_SUSPENDED
                    action.new_cr_status = IDLE
                    action.new_qa_status = IDLE

                if new_request_status is not None and new_request_status != old_request_status:
                    action.new_merge_status = new_request_status
                    old_request_status = new_request_status

                action.save()

    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")

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
            'cr_status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'developer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'merge_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mergemaster.MergeGroup']"}),
            'merge_status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'qa_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'qa_status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'status_code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'task_id': ('django.db.models.fields.IntegerField', [], {})
        },
        'mergemaster.mergerequestaction': {
            'Meta': {'object_name': 'MergeRequestAction'},
            'action_code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'merge_request': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mergemaster.MergeRequest']"}),
            'new_cr_status': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'new_merge_status': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'new_qa_status': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['mergemaster']
    symmetrical = True

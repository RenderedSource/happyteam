from django.contrib.auth.models import User
from django.db import models, transaction
from statuses import STATUSES, ACTIONS

class MergeMaster(models.Model):
    user = models.ForeignKey(User)
    enabled = models.BooleanField(default=True)
    jabber = models.CharField(blank = True, max_length = 60)

    def __unicode__(self):
        return self.user.username

class MergeRequest(models.Model):
    STATUS_CHOICES = [(s.code(), str(s)) for s in STATUSES]
    STATUS_DICT = dict((s.code(), s) for s in STATUSES)

    MERGE_REQUEST = 'merge_request'
    REJECTED = 'rejected'
    CODE_REVIEW_STARTED = 'cr_started'
    CODE_REVIEW_APPROVED = 'cr_approved'
    QA_STARTED = 'qa_started'
    QA_APPROVED = 'qa_approved'
    MERGED = 'merged'
    CANCELED = 'canceled'

    developer = models.ForeignKey(User)
    branch = models.CharField(max_length = 60)
    task_id = models.IntegerField()

    status = models.CharField(choices = STATUS_CHOICES, max_length = 20)
    qa_required = models.BooleanField()
    code_review_required = models.BooleanField()
    date_created = models.DateTimeField(auto_now = True, verbose_name = 'Date Created')
    date_modified = models.DateTimeField(auto_now = True, verbose_name = 'Date Modified')

    def label_css_class(self):
        return self.STATUS_DICT[self.status].label_css_class()

    def next_actions(self):
        return self.STATUS_DICT[self.status].next_actions()

    def update_status_by_action(self, action):
        """
        @type action: MergeRequestAction
        """
        if action.status == action.MERGE_REQUEST:
            self.status = self.PENDING
            self.code_review_required = True
            self.qa_required = True
        elif action.status == action.CODE_REVIEW_APPROVED:
            self.code_review_required = False
            self.status = self.PENDING
        elif action.status == action.QA_APPROVED:
            self.qa_required = False
            self.status = self.PENDING
        elif action.status == action.REJECTED:
            self.status = self.REJECTED
            self.code_review_required = False
            self.qa_required = False
        elif action.status == action.MERGED:
            self.status = self.MERGED
            self.code_review_required = False
            self.qa_required = False
        elif action.status == action.CANCELED:
            self.status = self.CANCELED
            self.code_review_required = False
            self.qa_required = False

    def __unicode__(self):
        return '%s - %s' % (self.developer, self.branch)

class MergeRequestAction(models.Model):
    ACTION_CHOICES = [(a.code(), str(a)) for a in ACTIONS]
    ACTION_DICT = dict((a.code(), a) for a in ACTIONS)

    merge_request = models.ForeignKey(MergeRequest)
    merge_master = models.ForeignKey(MergeMaster)
    status = models.CharField(choices = ACTION_CHOICES, max_length = 20)
    reason = models.CharField(blank = True, max_length = 100)
    date = models.DateTimeField(auto_now = True)

    def row_css_class(self):
        return self.ACTION_DICT[self.status].row_css_class()

    def user_friendly_status(self):
        return str(self.ACTION_DICT[self.status])

    @transaction.commit_manually
    def save(self, *args, **kwargs):
        try:
            if self.id is None:
                # update merge request if action is new
                self.merge_request.update_status_by_action(self)
                self.merge_request.save()

            super(self.__class__, self).save(*args, **kwargs)
        except:
            transaction.rollback()
            raise
        else:
            transaction.commit()


#class MergeComment(models.Model):
#    merge_request = models.ForeignKey(MergeRequest)
#    user = models.ForeignKey(User)
#    message = models.TextField()
#    date = models.DateTimeField(auto_now_add = True)

#    def __unicode__(self):
#        return self.user.username

MERGE_NOTIFICATION_TYPE = (
    ('error', 'alert-error'),
    ('success', 'alert-success'),
    ('info', ' alert-info')
    )

class MergeNotification(models.Model):
    message = models.TextField()
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    request = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=60, choices=MERGE_NOTIFICATION_TYPE)

    def __unicode__(self):
        return self.message


#class MergeStats(models.Model):
#    merge_master = models.ForeignKey(MergeMaster)
#    action = models.CharField(max_length=60, choices = MERGE_REQUEST_STATUS)
#    date = models.DateTimeField(auto_now_add=True)
#
#    def __unicode__(self):
#        return '%s %s' % (self.merge_master.user.username, self.action)


class JabberMessage(models.Model):
    jabber = models.CharField(max_length=60)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self): return self.jabber

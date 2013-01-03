import django.core.exceptions
from django.contrib.auth.models import User
from django.db import models, transaction

class MergeMaster(models.Model):
    user = models.ForeignKey(User)
    enabled = models.BooleanField(default = True)
    jabber = models.CharField(blank = True, max_length = 60)

    def __unicode__(self):
        return self.user.username

class MergeGroup(models.Model):
    main_branch = models.CharField(max_length = 60, blank = False)
    owner = models.ForeignKey(User)
    def __unicode__(self):
        return self.main_branch

REQUEST_PENDING = 0
REQUEST_REJECTED = 1
REQUEST_MERGED = 2
REQUEST_SUSPENDED = 3
REQUEST_STATUS_CHOICES = (
    (REQUEST_PENDING, 'Pending'),
    (REQUEST_REJECTED, 'Rejected'),
    (REQUEST_MERGED, 'Merged'),
    (REQUEST_SUSPENDED, 'Suspended'),
)

REQUEST_STATUS_LABEL_COLORS = {
    REQUEST_PENDING: 'label-warning',
    REQUEST_REJECTED: ' label-important',
    REQUEST_MERGED: 'label-success',
    REQUEST_SUSPENDED: 'label-inverse'
}

REQUIRED = 0
IN_PROGRESS = 1
REJECTED = 2
APPROVED = 3
IDLE = 4
STATUS_CHOICES = (
    (REQUIRED, 'Required'),
    (IN_PROGRESS, 'In progress'),
    (REJECTED, 'Rejected'),
    (APPROVED, 'Approved'),
    (IDLE, 'Idle')
)

STATUS_LABEL_COLORS = {
    REQUIRED: 'label-warning',
    IN_PROGRESS: 'label-info',
    REJECTED: ' label-important',
    APPROVED: 'label-success',
    IDLE: ''
}

class MergeRequest(models.Model):
    developer = models.ForeignKey(User)
    branch = models.CharField(max_length = 60)
    task_id = models.IntegerField()
    merge_group = models.ForeignKey(MergeGroup)

    merge_status = models.SmallIntegerField(choices = REQUEST_STATUS_CHOICES, default = REQUEST_PENDING)
    cr_status = models.SmallIntegerField(choices = STATUS_CHOICES, default = REQUIRED)
    qa_status = models.SmallIntegerField(choices = STATUS_CHOICES, default = REQUIRED)

    date_created = models.DateTimeField(auto_now = True, verbose_name = 'Date Created')
    date_modified = models.DateTimeField(auto_now = True, verbose_name = 'Date Modified')

    def merge_status_value(self):
        return next(name for value, name in REQUEST_STATUS_CHOICES if value == self.merge_status)

    def merge_status_label_class(self):
        return REQUEST_STATUS_LABEL_COLORS.get(self.merge_status, '')

    def show_cr_qa_labels(self):
        return self.merge_status == REQUEST_PENDING or self.merge_status == REQUEST_REJECTED

    def cr_status_value(self):
        return next(name for value, name in STATUS_CHOICES if value == self.cr_status)

    def cr_status_label_class(self):
        return STATUS_LABEL_COLORS.get(self.cr_status, '')

    def qa_status_value(self):
        return next(name for value, name in STATUS_CHOICES if value == self.qa_status)

    def qa_status_label_class(self):
        return STATUS_LABEL_COLORS.get(self.qa_status, '')

    @transaction.commit_manually
    def save(self, *args, **kwargs):
        try:
            is_new = True if self.id is None else False
            super(self.__class__, self).save(*args, **kwargs)

            if is_new:
                merge_action = MergeRequestAction()
                merge_action.merge_request = self
                merge_action.user = self.developer
                merge_action.new_merge_status = REQUEST_PENDING
                merge_action.new_cr_status = REQUIRED
                merge_action.new_qa_status = REQUIRED
                merge_action.save()
        except:
            transaction.rollback()
            raise
        else:
            transaction.commit()

    def get_last_action_id(self):
        try:
            return self.mergerequestaction_set.latest('id').id
        except django.core.exceptions.ObjectDoesNotExist:
            return None

    def __unicode__(self):
        return '%s - %s' % (self.developer, self.branch)

class MergeRequestAction(models.Model):
    merge_request = models.ForeignKey(MergeRequest)
    user = models.ForeignKey(User)
    new_merge_status = models.SmallIntegerField(choices = REQUEST_STATUS_CHOICES, null = True, blank = True)
    new_cr_status = models.SmallIntegerField(choices = STATUS_CHOICES, null = True, blank = True)
    new_qa_status = models.SmallIntegerField(choices = STATUS_CHOICES, null = True, blank = True)
    reason = models.CharField(blank = True, max_length = 100)
    date = models.DateTimeField(auto_now = True)

    def new_merge_status_value(self):
        if self.new_merge_status is None:
            return ''
        else:
            return next(name for value, name in REQUEST_STATUS_CHOICES if value == self.new_merge_status)

    def merge_status_label_class(self):
        return REQUEST_STATUS_LABEL_COLORS.get(self.new_merge_status, '')

    def new_cr_status_value(self):
        if self.new_cr_status is None:
            return ''
        else:
            return next(name for value, name in STATUS_CHOICES if value == self.new_cr_status)

    def cr_status_label_class(self):
        return STATUS_LABEL_COLORS.get(self.new_cr_status, '')

    def new_qa_status_value(self):
        if self.new_qa_status is None:
            return ''
        else:
            return next(name for value, name in STATUS_CHOICES if value == self.new_qa_status)

    def qa_status_label_class(self):
        return STATUS_LABEL_COLORS.get(self.new_qa_status, '')

    def __unicode__(self):
        return "%s - %s" % (self.merge_request.branch, self.user)

class MergeActionComment(models.Model):
    merge_action = models.ForeignKey(MergeRequestAction)
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add = True)
    content = models.TextField()

    def __unicode__(self):
        return self.user.username


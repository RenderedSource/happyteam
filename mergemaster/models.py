from django.contrib.auth.models import User
from django.db import models, transaction
from state_machine import STATUSES, ACTIONS, DEFAULT_STATUS, DEFAULT_ACTION

class MergeMaster(models.Model):
    user = models.ForeignKey(User)
    enabled = models.BooleanField(default = True)
    jabber = models.CharField(blank = True, max_length = 60)

    def __unicode__(self):
        return self.user.username

class MergeGroup(models.Model):
    main_branch = models.CharField(max_length = 60, blank = False)

    def __unicode__(self):
        return self.main_branch

class MergeRequest(models.Model):
    STATUS_CHOICES = [(s.code(), str(s)) for s in STATUSES]
    STATUS_DICT = dict((s.code(), s) for s in STATUSES)

    developer = models.ForeignKey(User)
    branch = models.CharField(max_length = 60)
    task_id = models.IntegerField()
    merge_group = models.ForeignKey(MergeGroup)

    status_code = models.CharField(choices = STATUS_CHOICES, max_length = 20, default = DEFAULT_STATUS.code())
    cr_required = models.BooleanField(verbose_name = 'Code review required')
    qa_required = models.BooleanField(verbose_name = 'QA required')
    date_created = models.DateTimeField(auto_now = True, verbose_name = 'Date Created')
    date_modified = models.DateTimeField(auto_now = True, verbose_name = 'Date Modified')

    def label_css_class(self):
        status = self.status()
        return status.label_css_class() if status else ''

    def next_actions(self):
        status = self.status()
        return status.next_actions() if status else ()

    def status(self):
        return self.STATUS_DICT.get(self.status_code, None)

    @transaction.commit_manually
    def save(self, *args, **kwargs):
        try:
            is_new = True if self.id is None else False
            if is_new:
                DEFAULT_ACTION.update_merge_request(self)

            super(self.__class__, self).save(*args, **kwargs)

            if is_new:
                merge_action = MergeRequestAction()
                merge_action.merge_request = self
                merge_action.user = self.developer
                merge_action.action_code = DEFAULT_ACTION.code()
                merge_action.save(update_merge_request=False)
        except:
            transaction.rollback()
            raise
        else:
            transaction.commit()

    def __unicode__(self):
        return '%s - %s' % (self.developer, self.branch)

class MergeRequestAction(models.Model):
    ACTION_CHOICES = [(a.code(), str(a)) for a in ACTIONS]
    ACTION_DICT = dict((a.code(), a) for a in ACTIONS)

    merge_request = models.ForeignKey(MergeRequest)
    user = models.ForeignKey(User)
    action_code = models.CharField(choices = ACTION_CHOICES, max_length = 20)
    reason = models.CharField(blank = True, max_length = 100)
    date = models.DateTimeField(auto_now = True)

    def row_css_class(self):
        action = self.action()
        return action.row_css_class() if action else ''

    def button_css_class(self):
        action = self.action()
        return action.button_css_class() if action else ''

    def past_form_name(self):
        action = self.action()
        return str(action.past_form_name()) if action else ''

    def action(self):
        return self.ACTION_DICT.get(self.action_code, None)

    @transaction.commit_manually
    def save(self, update_merge_request=True, *args, **kwargs):
        try:
            if self.id is None and update_merge_request:
                # update merge request if action is new
                self.action().update_merge_request(self.merge_request)
                self.merge_request.save()

            super(self.__class__, self).save(*args, **kwargs)
        except:
            transaction.rollback()
            raise
        else:
            transaction.commit()

    def __unicode__(self):
        return "%s - %s - %s" % (self.merge_request.branch, str(self.action()), self.user)

class MergeActionComment(models.Model):
    merge_action = models.ForeignKey(MergeRequestAction)
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add = True)
    content = models.TextField()

    def __unicode__(self):
        return self.user.username


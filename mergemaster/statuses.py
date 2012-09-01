LABEL_CLASS_DEFAULT = ''
LABEL_CLASS_SUCCESS = 'label-success'
LABEL_CLASS_WARNING = 'label-warning'
LABEL_CLASS_ERROR = 'label-important'
LABEL_CLASS_INVERSE = 'label-inverse'

ROW_CLASS_SUCCESS = 'success'
ROW_CLASS_ERROR = 'error'
ROW_CLASS_INFO = 'info'

class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls,*args,**kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance

class Status(object):
    __metaclass__ = Singleton

    def code(self):
        raise NotImplementedError()

    def label_css_class(self):
        raise NotImplementedError()

    def next_actions(self):
        raise NotImplementedError()

class StatusPending(Status):
    def code(self):
        return 'pending'

    def label_css_class(self):
        return LABEL_CLASS_DEFAULT

    def next_actions(self):
        return (
            ActionStartCodeReview(),
            ActionStartQa(),
            ActionCancel(),
        )

    def __str__(self):
        return 'Pending'

class StatusCodeReviewInProgress(Status):
    def code(self):
        return 'cr_in_progress'

    def label_css_class(self):
        return LABEL_CLASS_WARNING

    def next_actions(self):
        return (
            ActionApproveCodeReview(),
            ActionReject(),
        )

    def __str__(self):
        return 'Code review in progress'

class StatusQaInProgress(Status):
    def code(self):
        return 'qa_in_progress'

    def label_css_class(self):
        return LABEL_CLASS_WARNING

    def next_actions(self):
        return (
            ActionApproveQa(),
            ActionReject(),
        )

    def __str__(self):
        return 'QA in progress'

class StatusRejected(Status):
    def code(self):
        return 'rejected'

    def label_css_class(self):
        return LABEL_CLASS_ERROR

    def next_actions(self):
        return (
            ActionRequestMerge(),
            ActionCancel(),
        )

    def __str__(self):
        return 'Rejected'

class StatusApproved(Status):
    def code(self):
        return 'approved'

    def label_css_class(self):
        return LABEL_CLASS_SUCCESS

    def next_actions(self):
        return (
            ActionRequestMerge(),
            ActionMerge(),
            ActionReject(),
            ActionCancel(),
        )

    def __str__(self):
        return 'Approved'

class StatusMerged(Status):
    def code(self):
        return 'merged'

    def label_css_class(self):
        return LABEL_CLASS_SUCCESS

    def next_actions(self):
        return (
            ActionReject(),
            ActionCancel(),
        )

    def __str__(self):
        return 'Merged'

class StatusCanceled(Status):
    def code(self):
        return 'canceled'

    def label_css_class(self):
        return LABEL_CLASS_INVERSE

    def next_actions(self):
        return (
            ActionRequestMerge(),
        )

    def __str__(self):
        return 'Canceled'

STATUSES = (
    StatusPending(),
    StatusCodeReviewInProgress(),
    StatusQaInProgress(),
    StatusRejected(),
    StatusApproved(),
    StatusMerged(),
    StatusCanceled(),
)

class Action(object):
    __metaclass__ = Singleton

    def code(self):
        raise NotImplementedError()

    def row_css_class(self):
        raise NotImplementedError()

    def past_form_name(self):
        raise NotImplementedError()

    def update_merge_request(self, merge_request):
        raise NotImplementedError()

class ActionRequestMerge(Action):
    def code(self):
        return 'merge_request'

    def row_css_class(self):
        return ROW_CLASS_INFO

    def past_form_name(self):
        return 'Merge requested'

    def update_merge_request(self, merge_request):
        merge_request.status = StatusPending().code()
        merge_request.code_review_required = True
        merge_request.qa_required = True

    def __str__(self):
        return 'Request merge'

class ActionReject(Action):
    def code(self):
        return 'rejected'

    def row_css_class(self):
        return ROW_CLASS_ERROR

    def past_form_name(self):
        return 'Rejected'

    def update_merge_request(self, merge_request):
        merge_request.status = StatusRejected().code()
        merge_request.code_review_required = False
        merge_request.qa_required = False

    def __str__(self):
        return 'Reject'

class ActionStartCodeReview(Action):
    def code(self):
        return 'cr_started'

    def row_css_class(self):
        return ROW_CLASS_INFO

    def past_form_name(self):
        return 'Code review started'

    def update_merge_request(self, merge_request):
        merge_request.status = StatusCodeReviewInProgress().code()
        merge_request.code_review_required = False

    def __str__(self):
        return 'Start code review'

class ActionApproveCodeReview(Action):
    def code(self):
        return 'cr_approved'

    def row_css_class(self):
        return ROW_CLASS_SUCCESS

    def past_form_name(self):
        return 'Code review approved'

    def update_merge_request(self, merge_request):
        merge_request.status = StatusPending().code()
        merge_request.code_review_required = False

    def __str__(self):
        return 'Approve code review'

class ActionStartQa(Action):
    def code(self):
        return 'qa_started'

    def row_css_class(self):
        return ROW_CLASS_INFO

    def past_form_name(self):
        return 'QA started'

    def update_merge_request(self, merge_request):
        merge_request.status = StatusQaInProgress().code()
        merge_request.qa_required = False

    def __str__(self):
        return 'Start QA'

class ActionApproveQa(Action):
    def code(self):
        return 'qa_approved'

    def row_css_class(self):
        return ROW_CLASS_SUCCESS

    def past_form_name(self):
        return 'QA approved'

    def update_merge_request(self, merge_request):
        merge_request.status = StatusPending().code()
        merge_request.qa_required = False

    def __str__(self):
        return 'Approve QA'

class ActionMerge(Action):
    def code(self):
        return 'merged'

    def row_css_class(self):
        return ROW_CLASS_SUCCESS

    def past_form_name(self):
        return 'Merged'

    def update_merge_request(self, merge_request):
        merge_request.status = StatusMerged().code()
        merge_request.code_review_required = False
        merge_request.qa_required = False

    def __str__(self):
        return 'Merge'

class ActionCancel(Action):
    def code(self):
        return 'canceled'

    def row_css_class(self):
        return ROW_CLASS_ERROR

    def past_form_name(self):
        return 'Canceled'

    def update_merge_request(self, merge_request):
        merge_request.status = StatusCanceled().code()
        merge_request.code_review_required = False
        merge_request.qa_required = False

    def __str__(self):
        return 'Cancel'

ACTIONS = (
    ActionRequestMerge(),
    ActionReject(),
    ActionStartCodeReview(),
    ActionApproveCodeReview(),
    ActionStartQa(),
    ActionApproveQa(),
    ActionMerge(),
    ActionCancel(),
)
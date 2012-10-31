from knowledge.utils import get_module
from knowledge import settings
from mailer import send_html_mail
from website.local_settings import EMAIL_HOST_USER


def send_alerts(target_dict, response=None, question=None, **kwargs):
    """
    This can be overridden via KNOWLEDGE_ALERTS_FUNCTION_PATH.
    """
    from django.contrib.auth.models import User
    from django.template.loader import render_to_string
    from django.contrib.sites.models import Site

    site = Site.objects.get_current()

    for email, name in target_dict.items():
        if isinstance(name, User):
            name = u'{0} {1}'.format(name.first_name, name.last_name)
        else:
            name = name[0]

        context = {
            'name': name,
            'email': email,
            'response': response,
            'question': question,
            'site': site
        }

        subject = render_to_string(
            'django_knowledge/emails/subject.txt', context)

        message = render_to_string(
            'django_knowledge/emails/message.txt', context)

        message_html = render_to_string(
            'django_knowledge/emails/message.html', context)
        send_html_mail(subject,message ,message_html, EMAIL_HOST_USER,
            [email])

def knowledge_post_save(sender, instance, created, **kwargs):
    """
    Gathers all the responses for the sender's parent question
    and shuttles them to the predefined module.
    """
    from knowledge.models import Question, Response
    func = get_module(settings.ALERTS_FUNCTION_PATH)

    if settings.ALERTS and created:
        # pull together the out_dict:
        out_dict = []
        if isinstance(instance, Response):
            instances = list(instance.question.get_responses())
            instances += [instance.question]

            # dedupe people who want alerts thanks to dict keys...
            out_dict = dict([[i.get_email(), i.get_user_or_pair()]
                            for i in instances if i.alert])

        elif isinstance(instance, Question):
            out_dict = dict({instance.categories.owner.email:instance.categories.owner})
        # remove the creator...
        if instance.get_email() in out_dict.keys():
            del out_dict[instance.get_email()]


        func(
            target_dict=out_dict,
            response=instance if isinstance(instance, Response) else None,
            question=instance if isinstance(instance, Question) else None
        )

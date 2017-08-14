from django.template import loader
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.conf import settings


def send_reset_password_email(receiver):
    content = {
        'email': receiver.private_email,
        'domain': settings.DOMAIN,
        'site_name': 'SIS',
        'uid': urlsafe_base64_encode(force_bytes(receiver.pk)),
        'user': receiver,
        'token': default_token_generator.make_token(receiver),
        'protocol': 'http',
    }
    subject_template = 'accounts/password_reset_subject.html'
    body_template = 'accounts/password_reset_email.html'
    subject = loader.render_to_string(subject_template, content)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    email = loader.render_to_string(body_template, content)
    send_mail(subject, email, settings.DEFAULT_FROM_EMAIL,
              [receiver.private_email],
              fail_silently=False)

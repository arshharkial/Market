from django.db import models
from django.contrib.auth.models import AbstractUser

# from django.dispatch import receiver
# from django_rest_passwordreset.signals import reset_password_token_created

USERTYPE = [
    ("seller", "SELLER"),
    ("buyer", "BUYER"),
]


class User(AbstractUser):
    kind = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        choices=USERTYPE,
    )


# @receiver(reset_password_token_created)
# def password_reset_token_created(
#     sender, instance, reset_password_token, *args, **kwargs
# ):
#     # This is a function that is called when a user requests a password reset. It sends an email to the
#     # user with a link to reset their password.
#     email_plaintext_message = "<p>Token to reset password: {}</p><br><p>http://3.109.188.125/password_reset/confirm/</p><br>".format(
#         reset_password_token.key
#     )

#     message = Mail(
#         from_email="theadsh99@gmail.com",
#         to_emails=[reset_password_token.user.email],
#         subject="Password Reset for {title}".format(title="Creator360"),
#         html_content=email_plaintext_message,
#     )
#     try:
#         sg.send(message)
#     except Exception as e:
#         print(e)

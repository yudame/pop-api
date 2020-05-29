import logging

from anymail.message import AnymailMessageMixin
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from settings import DEFAULT_FROM_EMAIL, LOCAL

SIB_TEMPLATES = {
    'account-activate': {'id': 17, 'subject': "Verify and Activate Account"},
    # 'account-password-reset': {'id': 6, 'subject': "Reset Password"},
    'account-activate-mobile': {'id': 11, 'subject': "Confirm your account"},
    'account-login-code': {'id': 19, 'subject': "Login Code"},

    'artist-new-follower': {'id': 7, 'subject': "You have a new follower!"},
    'artist-published-video': {'id': 20, 'subject': "Video Published 🚀"},
    'artist-promoted-video': {'id': 14, 'subject': "Video Appreciated 👏"},

    'viewer-new-video-by-artist': {'id': 8, 'subject': "new video from your favorite artist"},

    # 'account-activate-confirmation': {'id': 0, 'subject': ""},
    # 'account-password-reset-confirmation': {'id': 0, 'subject': ""},
    # 'account-email-verification': {'id': 0, 'subject': ""},
    # 'account-closed': {'id': 0, 'subject': ""},
    # 'account-announcement': {'id': 0, 'subject': ""},
}


class SIBEmail(AnymailMessageMixin, EmailMultiAlternatives):

    def __init__(self, from_email=DEFAULT_FROM_EMAIL,
                 to_user=None, cc_user=None,
                 to_email="", cc_email="", bcc_email="",
                 subject="", message="", template_name="", data={}):
        """

		:param to_email: string or list of strings
		:param from_email:
		:param message:
		:param template_name:
		:param data:
		"""
        self.from_email = from_email

        self.to_user = to_user
        self.cc_user = cc_user

        self.to_email = to_email
        self.cc_email = cc_email
        self.bcc_email = bcc_email

        self.subject = subject
        self.message = message
        self.template_name = template_name
        self.data = data or {}
        super().__init__()

    def user_to_verify_at_url(self, url: str):
        """
		When an email requests an action (eg. validate address, reset password)
		This function will creat a one time token and add to url

		:param url: the url where the user should go to verify the action
		:return:
		"""
        if not isinstance(self.to_user, AbstractUser):
            raise UserWarning("to_user must already assigned before calling this function")

        account_activation_token = PasswordResetTokenGenerator()

        self.data['verification_url'] = "".join([
            f"{url}",
            f"?user_id={urlsafe_base64_encode(force_bytes(self.to_user.pk))}",
            f"&token={account_activation_token.make_token(self.to_user)}",
        ])

    def resolve_recipient_addresses(self):

        self.to = []
        if self.to_user and self.to_user.email and self.to_user.email_is_verified:
            if self.to_user.email.endswith("@example.com"):
                self.to.append(DEFAULT_FROM_EMAIL)
            else:
                self.to.append(self.to_user.email)
        if self.to_email:
            if isinstance(self.to_email, str):
                self.to.append(self.to_email)
            elif isinstance(self.to_email, list):
                self.to += self.to_email

        self.cc = []
        if self.cc_user and self.cc_user.email:
            self.cc.append(self.cc_user.email)
        if self.cc_email:
            if isinstance(self.cc_email, str):
                self.cc.append(self.cc_email)
            elif isinstance(self.cc_email, list):
                self.cc += self.cc_email

        self.bcc = []
        if self.bcc_email:
            if isinstance(self.bcc_email, str):
                self.bcc.append(self.bcc_email)
            elif isinstance(self.bcc_email, list):
                self.bcc += self.bcc_email

        # if not PRODUCTION:
        #     self.bcc.append(DEFAULT_FROM_EMAIL)

    def prepare_data(self):
        if SIB_TEMPLATES.get(self.template_name):
            self.template_id = SIB_TEMPLATES[self.template_name]['id']
            if not self.subject:
                self.subject = SIB_TEMPLATES[self.template_name]['subject']

        self.data["user_username"] = self.to_user.username
        self.data["user_email"] = self.to_user.email

        if self.message:
            self.data['message'] = self.message

    def send_to_user(self, user):
        self.to_user = user
        self.send()

    # @start_new_thread
    def send(self):
        self.resolve_recipient_addresses()
        self.prepare_data()

        self.merge_global_data = self.data
        try:
            if LOCAL:  # and not all([email.endswith("@pop.yuda.me") for email in self.to]):
                print(
                    f"On LOCAL, successful mock sending of email data {self.data} using SIB template {self.template_name}")
            elif not len(self.recipients()):
                logging.warning("WARNING: email attempted to send to 0 recipients!")
            else:
                logging.debug(
                    f"Sending email to recipients {self.recipients()} data {self.data} using SIB template {self.template_name}")
                super().send()
                logging.debug(f"Email successfully sent.")

        except Exception as e:
            logging.critical(f"this is the self.__dict__: {self.__dict__}")
            logging.critical(str(e))

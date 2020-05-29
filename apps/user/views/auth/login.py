from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.forms import forms
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.communication.views.email.email import SIBEmail
from apps.user.models import User
from static.image.qr import HOSTNAME


class CustomAuthenticationForm(AuthenticationForm):

    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

    def clean(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(Q(username=username) | Q(email=username)).first()
        if user and not user.is_active and not user.email_is_verified and user.email:

            # Send an email to the user with the token:
            email = SIBEmail(to_user=user, template_name="account-activate")
            email.to_email = user.email
            email.user_to_verify_at_url(
                HOSTNAME +
                reverse("activate_account")
            )
            email.send()

            raise forms.ValidationError(
                f"This account is not active yet. An email has been sent to {user.email}. Click the activation link in the email to continue login.",
                code='yet_active',
                params={'username': self.username_field.verbose_name},
            )

        return super().clean()


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm

    def dispatch(self, request, *args, **kwargs):
        # if user is not active, send different error message
        # "This account not active. Click the verification link in your email."
        # and send new verifiction email
        response = super().dispatch(request, *args, **kwargs)

        # print("account is not active yet" in str(response.__dict__['context_data']['form']))
        try:
            if "account is not active yet" in str(response.__dict__['context_data']['form']):
                messages.info(request, "Check email for account activation link.")
        except:
            pass

        return response

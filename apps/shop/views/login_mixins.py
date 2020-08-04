import base64
from django.contrib.auth import login
from django.contrib.auth.mixins import AccessMixin, UserPassesTestMixin
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlsafe_base64_decode
from django.views import View

from apps.shop.models import Shop
from apps.user.models import User


class LineRichMenuLoginMixin(AccessMixin):
    """Authenticate a user via uuid of LineChannelMembership in LineRichMenu"""
    def dispatch(self, request, *args, **kwargs):
        eid = request.GET.get('eid', None)
        if not eid:
            return super().dispatch(request, *args, **kwargs)

        lcm_uuid = urlsafe_base64_decode(eid).decode()
        line_channel_id, line_user_profile_id = lcm_uuid.split(':')
        if line_user_profile_id:
            user = User.objects.filter(line_user_profile__line_user_id=line_user_profile_id).first()
            if user:
                # todo: use something more temporary. maybe RemoteUserBackend ??
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        elif lcm_uuid:
            # in the case an unrecognizeable eid is provided
            # then immediately deny access
            self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class OTPLoginMixin(AccessMixin):
    """Authenticate a user via username and OTP_code as get params."""
    def dispatch(self, request, *args, **kwargs):

        username, otp = request.GET.get('username'), request.GET.get('otp')
        if username and otp:
            user = User.objects.filter(username=username).first()
            if user and otp == user.get_otp(num_digits=len(otp)):
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            elif not request.user.is_authenticated:
                # in the case that an invalid username and otp were provided AND the user was not already logged in
                # then we should immediately deny access and not allow other kinds of auth
                self.handle_no_permission()
        # other kinds of auth can be tested if no otp code attempted

        return super().dispatch(request, *args, **kwargs)

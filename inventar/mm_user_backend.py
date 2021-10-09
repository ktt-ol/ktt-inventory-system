# -*- coding: utf-8 -*-
# Copyright (c) 2015 Holger Cremer <HolgerCremer@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
#
#
# A user backend against our MoinMoin wiki. Uses the https://github.com/smilix/moinAuthProvider wiki action.
#

import logging
import random
import string
from json import JSONDecodeError

import requests
import requests.packages.urllib3
from django.conf import settings
from django.contrib.auth.backends import ModelBackend, UserModel
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


class MoinMoinUserBackend(ModelBackend):
    def __init__(self):
        self._check_for("MM_AUTH_PROVIDER_URL")
        self._check_for("MM_AUTH_PROVIDER_PSK")

        requests.packages.urllib3.disable_warnings()
        # self._session = requests.Session()

    def authenticate(self, request, username=None, password=None, **kwargs):
        logger.debug('Make auth request...')
        result = self._make_request("loginCheck", {
            "login": username,
            "password": password
        })
        auth_result = result["result"]
        logger.debug('Tried to authenticate user "%s". Result is "%s".' % (username, auth_result))

        if auth_result == "ok":
            try:
                user = User.objects.get(username=username)
            except UserModel.DoesNotExist:
                logger.info('User "%s" doesn\'t exist. Creating a new one.' % username)
                # Create a new user. Note that we can set password
                # to anything, because it won't be checked;
                # But we set it to a safe random string, in case the original backend is switched on
                user = User(username=username, password=self._make_rnd_pw())
                user.is_staff = True
                user.save()

            logger.info('Authenticate succeed, user "%s" logged in.' % username)
            return user
        else:
            logger.info('Authenticate failed, user "%s" not found.' % username)
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

    @staticmethod
    def _check_for(key):
        if not hasattr(settings, key):
            raise ValueError('No "%s" in config found.' % key)

    @staticmethod
    def _make_rnd_pw(size=20, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def _make_request(self, do_type, json=None):
        if not json:
            json = {}
        url = settings.MM_AUTH_PROVIDER_URL + "?action=authService&do=" + do_type
        try:
            resp = requests.post(url, headers={
                "Auth-Token": settings.MM_AUTH_PROVIDER_PSK
            },
             json=json,
             verify=settings.MM_AUTH_PROVIDER_SSL_VERIFY,
             allow_redirects=False)
            if resp.status_code != 200:
                raise Exception(f"Unexpected response code {resp.status_code:d} for '{url}'. \nServer response was: {resp.text}")
        except requests.exceptions.SSLError as e:
            logger.error("SSLError: %s", e)
            raise e

        try:
            return resp.json()
        except JSONDecodeError as e:
            logger.error("Can't decode the following JSON:\n%s", resp.text)
            raise e

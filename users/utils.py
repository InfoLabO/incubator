from datetime import datetime

import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator


def current_year():
    """ returns """

    now = datetime.today()
    if now.month < 9:
        return now.year - 1
    elif now.month == 9:
        return now.year - 1 if now.day < 15 else now.year
    else:
        return now.year

"""
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.is_email_verified))


generate_token = TokenGenerator()"""


from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    '''Class to generate a token to allow new users to signup '''

    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.profile.email_confirmed)
        )

account_activation = AccountActivationTokenGenerator()
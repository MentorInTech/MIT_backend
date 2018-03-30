"""
Copyright (c) 2018， Silicon Valley Career Women.
All rights reserved.
"""
from datetime import date

from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """Token generator class for account activation."""

    def _make_hash_value(self, user: User, timestamp: date) -> str:
        """Override the function in PasswordResetTokenGenerator to also hash the user.is_active value.

        (This is a protected method so client won't interact with this method directly.)
        Args:
            user: Django User model.
            timestamp: The current time.

        Returns:
            A str to be hashed.
        """
        return str(user.pk) + str(timestamp) + str(user.is_active)


account_activation_token = AccountActivationTokenGenerator()

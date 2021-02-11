from django.db import models
from django.contrib.auth.models import User
import string
import random


class Account(User):
    class Meta:
        # app_label = 'account'
        proxy = True

    @classmethod
    def random_password(cls, size: int = 10):
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for x in range(size))

    def set_random_password(self, size: int = 10):
        self.password = self.random_password(size=size)
        return self.password

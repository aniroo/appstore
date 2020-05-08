import os

from allauth.socialaccount.models import SocialApp
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for app in ['GITHUB', 'GOOGLE']:
            SocialApp.objects.create(
                name='braini' if app == 'GOOGLE' else 'github',
                client_id=os.environ[f'{app}_CLIENT_ID'],
                secret=os.environ.get(f'{app}_SECRET'),
                provider=app.lower(),
                key='',
            )
        Group.objects.create(name='whitelisted')

        print("Successfully added social applications GitHub and Google!")

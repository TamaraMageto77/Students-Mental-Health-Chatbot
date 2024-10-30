from django.core.management.base import BaseCommand
from accounts.models import Account

class Command(BaseCommand):
    help = 'Update the email and password of a superuser'

    def add_arguments(self, parser):
        parser.add_argument('old_email', type=str, help='Current email of the superuser')
        parser.add_argument('new_email', type=str, help='New email to set for the superuser')
        parser.add_argument('new_password', type=str, help='New password to set for the superuser')

    def handle(self, *args, **kwargs):
        old_email = kwargs['old_email']
        new_email = kwargs['new_email']
        new_password = kwargs['new_password']

        try:
            superuser = Account.objects.get(email=old_email, is_superuser=True)
            superuser.email = new_email
            superuser.set_password(new_password)
            superuser.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully updated superuser email to {new_email} and password'))
        except Account.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Superuser with email {old_email} does not exist'))
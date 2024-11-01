from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import models
from django.apps import apps
from datetime import timedelta

class Command(BaseCommand):
    help = 'Convert all DateTimeField values from UTC to GMT+3'

    def handle(self, *args, **options):
        time_shift = timedelta(hours=3)

        # Iterate through all models and their DateTimeFields
        for model in apps.get_models():
            for field in model._meta.fields:
                if isinstance(field, models.DateTimeField):
                    # Fetch all rows with DateTimeField data
                    for instance in model.objects.all():
                        datetime_value = getattr(instance, field.name)
                        if datetime_value:
                            new_datetime = datetime_value + time_shift
                            setattr(instance, field.name, new_datetime)
                            instance.save()

        self.stdout.write(self.style.SUCCESS('All DateTimeFields converted to GMT+3'))

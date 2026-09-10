from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create a default superuser if it does not exist'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'admin'
        password = 'grandbrook123'

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                password=password,
                email='admin@grandbrook.com'
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully!'))
        else:
            self.stdout.write('Superuser already exists.')
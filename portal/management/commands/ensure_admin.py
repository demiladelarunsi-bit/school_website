from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create a default superuser if it does not exist'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'admin'
        password = 'grandbrook123'

        # Get the user if it exists, or create it if it doesn't
        user, created = User.objects.get_or_create(username=username)
        
        # ALWAYS set the password to make sure it's correct
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        
        if created:
            self.stdout.write(self.style.SUCCESS('Superuser created successfully!'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser password updated successfully!'))
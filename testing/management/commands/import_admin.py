from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import termcolors
from decouple import config

class Command(BaseCommand):
    help = 'Creates a superuser with predefined data'
    
    def handle(self, *args, **kwargs):
        UserModel = get_user_model()
        username = config('DJANGO_ADMIN_USERNAME', default='admin')
        email = config('DJANGO_ADMIN_USER_MAIL', default='admin@admin.com')
        password = config('DJANGO_ADMIN_USER_PASWORD', default='admin')
        
        try:
            if not UserModel.objects.filter(username=username).exists():
                user = UserModel.objects.create_superuser(username=username, email=email, password=password)
                user.is_active = True
                user.is_staff = True
                user.save()
                
                self.stdout.write(termcolors.make_style(fg="green")('✔ Superuser created successfully!'))
            else:
                self.stdout.write(termcolors.make_style(fg="red")(f"✘ Superuser already exists!"))

        except Exception as e:
            self.stdout.write(termcolors.make_style(fg="red")(f"✘ {str(e)}"))
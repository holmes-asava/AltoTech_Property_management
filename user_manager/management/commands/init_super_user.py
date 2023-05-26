from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        email = "dev@gmail.com"
        password = settings.SUPER_ADMIN_PASS

        if User.objects.filter(email__iexact=email).exists():
            u = User.objects.get(email=email)
            u.set_password(password)
            u.save()
            self.stdout.write(
                "The admin account has already existed. Password will be reset."
            )
        else:
            User.objects.create_superuser(email, password)
            self.stdout.write("The admin account has been created.")

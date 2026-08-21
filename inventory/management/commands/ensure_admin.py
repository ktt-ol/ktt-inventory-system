import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Ensure the admin user exists (idempotent)"

    def handle(self, *args, **options):
        username = os.environ.get("ADMIN_USERNAME", "admin")
        password = os.environ.get("ADMIN_PASSWORD")
        if not password:
            raise CommandError("ADMIN_PASSWORD is not set")

        if User.objects.filter(username=username).exists():
            self.stdout.write(f"  {username}: exists")
            return

        User.objects.create_superuser(username, email="", password=password)
        self.stdout.write(f"  {username}: created")

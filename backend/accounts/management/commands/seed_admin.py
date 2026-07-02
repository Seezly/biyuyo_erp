from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Seed a superuser if the database is empty"

    def handle(self, *args, **options):
        User = get_user_model()

        if User.objects.count() > 0:
            self.stdout.write(self.style.WARNING("Users exist, skipping seed"))
            return

        User.objects.create_superuser(
            first_name="Admin",
            last_name="Biyuyo",
            email="admin@biyuyo.com",
            identification_number="V00000000",
            phone="04000000000",
            password="admin123",
        )

        self.stdout.write(self.style.SUCCESS("Superuser seeded: admin@biyuyo.com"))

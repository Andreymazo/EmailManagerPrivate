from django.core.management import BaseCommand

from worktimeprivate.models import CustomUser, Employer


# from users.models import CustomUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        customuser = CustomUser.objects.create(
                email='efimka_rabotodatel@nha.com',
                is_admin=False
            )
        customuser.set_password('qwert123asd')
        customuser.save()
        employee = Employer.objects.create(
            customuser=CustomUser.objects.get(email='efimka_rabotodatel@nha.com'),
            name='efimka_rabotodatel',
        )
        # employee.set_password('qwert123asd')
        employee.save()
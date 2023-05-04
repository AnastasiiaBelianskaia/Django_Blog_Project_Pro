from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from faker import Faker

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = 'Creates users for database (from 10 to 1000).'  # noqa: A003

    def add_arguments(self, parser):
        parser.add_argument('quantity', type=int, choices=range(10, 1001))

    def handle(self, *args, **kwargs):
        quantity = kwargs['quantity']
        users_list = []
        for number in range(quantity):
            users_list.append(User(first_name=fake.first_name(),
                                   last_name=fake.last_name(),
                                   username=fake.user_name(),
                                   email=fake.email(),
                                   password=make_password(fake.password())))
        User.objects.bulk_create(users_list)
        self.stdout.write(f'{quantity} users have been created in database!')

from blog.models import Post

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from faker import Faker

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = 'Creates posts for database (from 10 to 1000).'  # noqa: A003

    def add_arguments(self, parser):
        parser.add_argument('quantity', type=int, choices=range(10, 1001))

    def handle(self, *args, **kwargs):
        quantity = kwargs['quantity']
        posts_list = []
        for number in range(quantity):
            posts_list.append(Post(heading=fake.sentence(nb_words=5),
                                   text=fake.text(),
                                   short_definition=fake.paragraph(nb_sentences=3),
                                   is_published=True,
                                   author_id=User.objects.values_list("id", flat=True).order_by('?').first(),
                                   ))
        Post.objects.bulk_create(posts_list)
        self.stdout.write(f"{quantity} posts have been created in database!")

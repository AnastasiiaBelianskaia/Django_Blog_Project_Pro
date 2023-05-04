from blog.models import Comment, Post

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from faker import Faker

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = 'Creates comments for database (from 10 to 1000).'  # noqa: A003

    def add_arguments(self, parser):
        parser.add_argument('quantity', type=int, choices=range(10, 1001))

    def handle(self, *args, **kwargs):
        quantity = kwargs['quantity']
        comments_list = []
        for number in range(quantity):
            comments_list.append(Comment(author=fake.user_name(),
                                         post_id=Post.objects.values_list("id", flat=True).order_by('?').first(),
                                         text=fake.paragraph(nb_sentences=5),
                                         is_published=True,
                                         ))
        Comment.objects.bulk_create(comments_list)
        self.stdout.write(f"{quantity} comments have been created in database!")

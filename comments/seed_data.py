from django_seed import Seed
from comments.models import Comment
from posts.models import Post
from django.contrib.auth.models import User
import random

def seed_comments(count=60):
    seeder = Seed.seeder()
    seeder.add_entity(Comment, count, {
        'post': lambda x: random.choice(Post.objects.all()),
        'user': lambda x: random.choice(User.objects.all()),
        'content': lambda x: seeder.faker.sentence(nb_words=15),
    })
    inserted = seeder.execute()
    print(f"✅ Seeded {count} comments.")
    return inserted
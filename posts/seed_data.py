from django_seed import Seed
from posts.models import Post
from django.contrib.auth.models import User
import random

def seed_posts(count=20):
    seeder = Seed.seeder()
    seeder.add_entity(Post, count, {
        'user': lambda x: random.choice(User.objects.all()),
        'title': lambda x: seeder.faker.sentence(nb_words=10),
        'content': lambda x: seeder.faker.paragraph(nb_sentences=15),
    })
    inserted = seeder.execute()
    print(f"✅ Seeded {count} posts.")
    return inserted
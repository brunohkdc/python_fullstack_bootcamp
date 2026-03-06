from posts.models import Post
from django.contrib.auth.models import User
from faker import Faker
import random

fake = Faker()

def seed_posts(count=20):
    users = list(User.objects.all())
    if not users:
        print("❌ No users found. Create users first.")
        return

    for _ in range(count):
        Post.objects.create(
            title=fake.sentence(nb_words=10).rstrip('.'),
            post=fake.paragraph(nb_sentences=15),
            user=random.choice(users),
        )
    print(f"✅ Seeded {count} posts.")
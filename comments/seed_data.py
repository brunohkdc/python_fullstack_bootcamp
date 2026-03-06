from comments.models import Comment
from posts.models import Post
from django.contrib.auth.models import User
from faker import Faker
import random

fake = Faker()

def seed_comments(count=60):
    posts = list(Post.objects.all())
    users = list(User.objects.all())

    if not posts or not users:
        print("❌ No posts or users found. Create them first.")
        return

    for _ in range(count):
        Comment.objects.create(
            post=random.choice(posts),
            user=random.choice(users),
            content=fake.sentence(nb_words=30),
        )
    print(f"✅ Seeded {count} comments.")
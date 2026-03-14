from django.contrib.auth.models import User, Group

from faker import Faker

fake = Faker()

def seed_users(count=7):
    
    for _ in range(count):
        User.objects.create_user(
            username=Faker().user_name(),
            email=Faker().email(),
            password='abcdef123456',
            first_name=Faker().first_name(),
            last_name=Faker().last_name(),
            is_active=True,
            is_staff=False,
            is_superuser=False
        )

    # Assign all users to the 'user' group
    group = Group.objects.get(name='user')

    for user in User.objects.filter(is_active=True):
        user.groups.add(group)

    print(f"✅ Seeded {count} users.")

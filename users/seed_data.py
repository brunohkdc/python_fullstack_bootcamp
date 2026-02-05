from django_seed import Seed
from django.contrib.auth.models import User, Group

def seed_users(count=7):
    seeder = Seed.seeder()
    seeder.add_entity(User, count, {
        'username': lambda x: seeder.faker.unique.user_name(),
        'email': lambda x: seeder.faker.email(),
        'first_name': lambda x: seeder.faker.first_name(),
        'last_name': lambda x: seeder.faker.last_name(),
        'is_active': True,
        'is_staff': False,
        'is_superuser': False,
    })
    seeder.execute()

    # Assign all users to the 'user' group
    group = Group.objects.get(name='user')

    for user in User.objects.filter(is_active=True):
        user.groups.add(group)

    print(f"✅ Seeded {count} users.")

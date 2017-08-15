from faker import Faker
from accounts.models import StudentProfile
import random

fake_gen = Faker()


def gen_user():
    name = fake_gen.name()
    location = fake_gen.address()
    password = 'hust1234'
    status = 'ST'
    birth_day = random_birthday()
    user = StudentProfile.objects.get_or_create(name=name,
                                                student_id='123',
                                                email='123@gmail.com',
                                                home_address=location,
                                                password=password,
                                                status=status,
                                                gender=True,
                                                date_of_birth=birth_day)[0]
    user.save()


def random_birthday():
    year = random.choice(range(1992, 1998))
    month = random.choice(range(1, 13))
    day = random.choice(range(1, 29))
    return '{}-{}-{}'.format(year, month, day)


def populate_user(N=20):
    for entry in range(20):
        gen_user()


def update_location():
    user_list = StudentProfile.objects.all()
    for user in user_list:
        user.home_address = fake_gen.address()
        user.save()


print("Start populate")
update_location()
print("End populate")

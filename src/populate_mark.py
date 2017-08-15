import random
from subjects.models import Subject, Mark
from accounts.models import StudentProfile

user_list = StudentProfile.objects.all()
subject_list = Subject.objects.all()


def populate():
    for user in user_list:
        for subject in subject_list:
            mark = Mark.objects.get_or_create(student=user, subject=subject,
                                              mid_term_mark=random_mark(),
                                              final_mark=random_mark())[0]
            mark.save()


def random_mark():
    return random.choice(range(1, 11))


print('Start')
populate()
print('End')

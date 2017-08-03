import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.urls import reverse
from django.db.models.signals import post_save


class StudentProfileManager(BaseUserManager):
    def create_user(self, name, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        user = self.model(name=name, **extra_fields)
        user.password = password
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password=None,
                         **extra_fields):
        extra_fields['status'] = StudentProfile.ADMIN
        user = self.create_user(name=name, password=password,
                                **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)


def convert_student_id(id):
    # student_id first part is current year,last part is user id with 4 number formatted
    student_id_first_part = datetime.datetime.now().year
    student_id_last_part = '{0:0{width}}'.format(int(id), width=4)
    return '{}{}'.format(student_id_first_part, student_id_last_part)


def create_student_email(id):
    return '{}@hust.edu.vn'.format(convert_student_id(id))


class StudentProfile(AbstractBaseUser, PermissionsMixin):
    STUDYING = 'ST'
    GRADUATED = 'GT'
    ADMIN = 'AD'

    STATUS_CHOICES = (
        (STUDYING, 'Studying'),
        (GRADUATED, 'Graduated'),
        (ADMIN, 'Administrator')
    )

    student_id = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, blank=True)
    private_email = models.EmailField(max_length=255, default='',
                                      null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/',
                                    default='images/user-default.jpg')
    status = models.CharField(max_length=2, choices=STATUS_CHOICES,
                              default=STUDYING)
    date_of_birth = models.DateField(max_length=8, default='2017-01-01')
    # True is male,False is female
    gender = models.BooleanField(default=True)
    joined_time = models.DateField(auto_now=True)
    graduated_year = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    home_address = models.CharField(max_length=256, null=True, blank=True,
                                    default='')
    mobile_phone = models.CharField(max_length=12, null=True, blank=True,
                                    default='')
    objects = StudentProfileManager()

    USERNAME_FIELD = 'student_id'
    REQUIRED_FIELDS = ['name', 'email']

    class Meta:
        db_table = 'StudentProfiles'

    def get_gender(self):
        if self.gender:
            return 'Male'
        return 'Female'

    def get_absolute_url(self):
        return reverse('accounts:profile',
                       kwargs={'student_id': self.student_id})

    def get_thread_list_api(self):
        return reverse('thread-apis:user_thread')

    def get_comment_list_api(self):
        return reverse('comment-apis:user_comment')

    def get_activity_link(self):
        return reverse('accounts:activity',
                       kwargs={'student_id': self.student_id})

    def get_update_url(self):
        return reverse('accounts:profile-update',
                       kwargs={'student_id': self.student_id})

    def get_image_upload_url(self):
        return reverse('accounts:image-update',
                       kwargs={'student_id': self.student_id})

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.name


def post_save_student_receiver(sender, instance, created, *args, **kwargs):
    if created:
        instance.set_password(instance.password)
        instance.student_id = convert_student_id(instance.id)
        instance.email = create_student_email(instance.id)
        instance.save()


post_save.connect(post_save_student_receiver, sender=StudentProfile)

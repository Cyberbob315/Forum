from django.db import models
from subjects.models import Subject
from accounts.models import StudentProfile


class Subforum(models.Model):
    subject = models.OneToOneField(Subject, related_name='subforum')
    title = models.CharField(max_length=255)

    class Meta:
        db_table = 'Subforums'

    def get_last_post(self):
        thread_list =  self.threads.filter(published_date__isnull=False).order_by(
            '-published_date')
        if thread_list.count() >0:
            return thread_list[0]
        return 'There is no thread in this subforum'

    def count_threads(self):
        return self.threads.filter(published_date__isnull=False).count()

    def count_comments(self):
        pass

    def __str__(self):
        return self.title


class Thread(models.Model):
    subforum = models.ForeignKey(Subforum, related_name='threads')
    title = models.CharField(max_length=350)
    author = models.ForeignKey(StudentProfile, related_name='threads')
    likes = models.ManyToManyField(StudentProfile, related_name='thread_likes')
    created_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'Threads'

    def __str__(self):
        return self.title


class ThreadImages(models.Model):
    thread = models.ForeignKey(Thread, related_name='images')
    image = models.ImageField(upload_to='thread_pics/')

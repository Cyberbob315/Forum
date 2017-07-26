from django.db import models
from accounts.models import StudentProfile
from threads.models import Thread


class Comment(models.Model):
    thread = models.ForeignKey(Thread, related_name='comments')
    author = models.ForeignKey(StudentProfile, related_name='comments')
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Comments'


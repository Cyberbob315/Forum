from django.db import models
from accounts.models import StudentProfile
from subforums.models import Thread


class Comment(models.Model):
    thread = models.ForeignKey(Thread, related_name='comments')
    author = models.ForeignKey(StudentProfile, related_name='comments')
    created_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Comments'

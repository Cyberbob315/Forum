from django.db import models
from django.urls import reverse
from accounts.models import StudentProfile


class Comment(models.Model):
    thread = models.ForeignKey('threads.Thread', related_name='comments')
    author = models.ForeignKey(StudentProfile, related_name='comments')
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Comments'

    def get_delete_api_url(self):
        return reverse('comment-apis:delete', kwargs={'pk': self.id})

    def __str__(self):
        return '{} by {}'.format(self.thread, self.author)

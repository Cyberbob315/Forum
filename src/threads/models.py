from django.db import models
from django.core.urlresolvers import reverse
import misaka
from subforums.models import Subforum
from accounts.models import StudentProfile


class Thread(models.Model):
    subforum = models.ForeignKey(Subforum, related_name='threads')
    title = models.CharField(max_length=350)
    content = models.TextField()
    content_html = models.TextField(editable=False, default='', blank=True)
    author = models.ForeignKey(StudentProfile, related_name='threads')
    likes = models.ManyToManyField(StudentProfile, related_name='thread_likes')
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)
    is_pinned = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'Threads'

    def get_detail_link(self):
        return reverse('threads:detail', kwargs={'pk': self.pk})

    def get_like_url(self):
        return reverse('threads:like', kwargs={'pk': self.pk})

    def save(self, *args,**kwargs):
        self.content_html = misaka.html(self.content)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title


class ThreadImages(models.Model):
    thread = models.ForeignKey(Thread, related_name='images')
    image = models.ImageField(upload_to='thread_pics/')

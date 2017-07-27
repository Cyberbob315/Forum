from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import slugify

from subforums.models import Subforum
from accounts.models import StudentProfile


class Thread(models.Model):
    subforum = models.ForeignKey(Subforum, related_name='threads')
    title = models.CharField(max_length=350)
    content = models.TextField()
    content_html = models.TextField(editable=False, default='', blank=True)
    author = models.ForeignKey(StudentProfile, related_name='threads')
    likes = models.ManyToManyField(StudentProfile, related_name='thread_likes',
                                   blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)
    is_pinned = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'Threads'

    def summarize_content(self):
        if len(self.content) > 20:
            return '{}...'.format(self.content[:20])
        else:
            return self.content

    def increase_view(self):
        self.view_count += 1
        self.save()

    def get_detail_link(self):
        return reverse('threads:detail', kwargs={'pk': self.pk})

    def get_image_file_name(self, filename):
        slug = slugify(self.title)
        return 'thread_images/{}-{}'.format(slug, filename)

    def get_like_url(self):
        return reverse('threads:like', kwargs={'pk': self.pk})

    def get_check_like_url(self):
        return reverse('threads:check-like', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class ThreadImages(models.Model):
    thread = models.ForeignKey(Thread, related_name='images')
    image = models.ImageField(upload_to='thread_images/', )

    def __str__(self):
        return self.image.name

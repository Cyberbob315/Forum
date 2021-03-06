from django.db import models
from django.core.urlresolvers import reverse

from subjects.models import Subject
from accounts.models import StudentProfile
from django.utils.text import slugify
from comments import models as comment_models


class Subforum(models.Model):
    subject = models.OneToOneField(Subject, related_name='subforum')
    title = models.CharField(max_length=255, unique=True)
    short_name = models.CharField(max_length=20)
    slug = models.SlugField(allow_unicode=True, unique=True)

    class Meta:
        db_table = 'Subforums'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_detail_link(self):
        return reverse('forum:detail', kwargs={'slug': self.slug})

    def get_draft_list_link(self):
        return reverse('forum:drafts', kwargs={'slug': self.slug})

    def count_drafts(self):
        return self.threads.filter(
            published_date__isnull=True
        ).order_by(
            '-created_date'
        ).count()

    def get_last_post(self):
        thread_list = self.threads.filter(
            published_date__isnull=False
        ).order_by(
            '-published_date'
        )
        if thread_list.count() > 0:
            return thread_list[0]

    def published_thread_count(self):
        return self.threads.filter(
            published_date__isnull=False
        ).order_by(
            '-created_date'
        ).count()

    def count_threads(self):
        return self.threads.filter(published_date__isnull=False).count()

    def count_comments(self):
        return comment_models.Comment.objects.filter(
            thread__subforum=self
        ).count()

    def __str__(self):
        return self.title

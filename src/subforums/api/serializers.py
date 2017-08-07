from django.urls.base import reverse
from rest_framework import serializers
from subforums.models import Subforum


class SubforumModelSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    total_draft = serializers.SerializerMethodField()
    draft_list_link = serializers.SerializerMethodField()

    class Meta:
        model = Subforum
        fields = [
            'title',
            'total_draft',
            'draft_list_link',
        ]

    def get_title(self, obj):
        return obj.title

    def get_total_draft(self, obj):
        return obj.threads.filter(published_date__isnull=True).count()

    def get_draft_list_link(self, obj):
        return reverse('student_admin:drafts', kwargs={'slug': obj.slug})

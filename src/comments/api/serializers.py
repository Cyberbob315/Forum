from rest_framework import serializers
from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    thread_title = serializers.SerializerMethodField()
    thread_link = serializers.SerializerMethodField()
    author_pic_link = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    created_date = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'author_name',
            'content',
            'created_date',
            'thread_title',
            'thread_link',
            'author_pic_link'
        ]

    def get_created_date(self, obj):
        return obj.created_date.strftime("%b %d %I:%M %p")

    def get_content(self, obj):
        if len(obj.content) > 30:
            return '{}...'.format(obj.content[:30])
        return obj.content

    def get_author_pic_link(self, obj):
        return obj.author.profile_pic.url

    def get_author_name(self, obj):
        return obj.author.name

    def get_thread_title(self, obj):
        return obj.thread.title

    def get_thread_link(self, obj):
        return obj.thread.get_detail_link()


class CommentEditDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'content'
        ]

from rest_framework import serializers
from threads.models import Thread


class ThreadModelSerializer(serializers.ModelSerializer):
    sub_forum = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    total_view = serializers.SerializerMethodField()
    total_like = serializers.SerializerMethodField()
    created_date = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    author_pic_url = serializers.SerializerMethodField()
    detail_link = serializers.SerializerMethodField()
    total_comment = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = [
            'id',
            'author_name',
            'author_pic_url',
            'sub_forum',
            'title',
            'content',
            'is_pinned',
            'created_date',
            'total_view',
            'total_like',
            'detail_link',
            'total_comment',
        ]

    def get_total_comment(self, obj):
        return obj.comments.count()

    def get_detail_link(self, obj):
        return obj.get_detail_link()

    def get_author_pic_url(self, obj):
        return obj.author.profile_pic.url

    def get_created_date(self, obj):
        return obj.created_date.strftime("%b %d %I:%M %p")

    def get_content(self, obj):
        return obj.summarize_content()

    def get_sub_forum(self, obj):
        return obj.subforum.title

    def get_author_name(self, obj):
        return obj.author.name

    def get_total_view(self, obj):
        return obj.view_count

    def get_total_like(self, obj):
        return obj.likes.count()

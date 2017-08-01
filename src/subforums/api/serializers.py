from rest_framework import serializers
from subforums.models import Subforum

class SubforumModelSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = Subforum
        fields =[
            'title',
        ]

    def get_title(self, obj):
        return obj.title


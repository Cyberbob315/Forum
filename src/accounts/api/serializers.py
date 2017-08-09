import re
from django.contrib.auth import authenticate
from django.urls.base import reverse
from rest_framework import serializers
from accounts.models import StudentProfile
from django.utils.translation import ugettext_lazy as _


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"))
    password = serializers.CharField(label=_("Password"),
                                     style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class StudentProfileSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    transcript_link = serializers.SerializerMethodField()

    class Meta:
        model = StudentProfile
        fields = [
            'student_id',
            'name',
            'gender',
            'status',
            'email',
            'joined_time',
            'private_email',
            'date_of_birth',
            'mobile_phone',
            'home_address',
            'profile_pic',
            'transcript_link',
        ]

    def get_status(self, obj):
        return obj.get_status_display()

    def get_transcript_link(self, obj):
        return reverse('student_admin:transcript',
                       kwargs={'student_id': obj.student_id})

    def validate_mobile_phone(self, value):
        if re.search('[a-zA-Z]', value):
            raise serializers.ValidationError(
                'Mobile phone number can not contain letters from alphabet')
        if len(value) != 10 or len(value) !=11:
            raise serializers.ValidationError(
                'Mobile phone number must be 10 or 11 characters')
        return value

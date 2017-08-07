from django.contrib.auth import authenticate
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
    gender = serializers.SerializerMethodField()

    class Meta:
        model = StudentProfile
        fields = [
            'student_id',
            'name',
            'gender',
            'status',
            'email',
            'private_email',
            'date_of_birth',
            'mobile_phone',
            'home_address',
        ]

    def get_status(self, obj):
        return obj.get_status_display()

    def get_gender(self, obj):
        return 'Male' if obj.gender else 'Female'

    def update(self, instance, validated_data):
        pass

from rest_framework import serializers
from subjects.models import Subject, Mark
import re


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            'subject_id',
            'title',
            'credit',
        ]

    def validate_credit(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError(
                'Credit number need to be in range from 0 to 5')
        return value


class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = [
            'student',
            'subject',
            'mid_term_mark',
            'final_mark'
        ]

    def validate_mid_term_mark(self, value):
        if value < 0 or value > 10:
            raise serializers.ValidationError(
                'Mark need to be in range from 0 to 10')
        return value

    def validate_final_mark(self, value):
        if value < 0 or value > 10:
            raise serializers.ValidationError(
                'Mark need to be in range from 0 to 10')
        return value

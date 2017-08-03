from django.db import models
import datetime
from accounts.models import StudentProfile
from subforums import models as forum_models


class Subject(models.Model):
    title = models.CharField(max_length=255)
    credit = models.IntegerField()
    subject_id = models.CharField(max_length=8)
    short_name = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        # Auto create a subforum for this subject
        super(Subject, self).save(*args, **kwargs)
        subforum = forum_models.Subforum.objects.get_or_create(subject=self)[0]
        subforum.title = self.title
        subforum.short_name = self.short_name
        subforum.save()

    class Meta:
        db_table = 'Subjects'

    def __str__(self):
        return self.title


class Mark(models.Model):
    PASS = 'PS'
    NOT_PASS = 'NP'

    MARK_STATUS = (
        (PASS, 'PASS'),
        (NOT_PASS, 'NOT PASS'),
    )
    YEAR_CHOICES = [(r, r) for r in
                    range(2010, datetime.date.today().year + 1)]

    student = models.ForeignKey(StudentProfile, related_name='marks')
    subject = models.ForeignKey(Subject, related_name='mark')
    year = models.IntegerField(choices=YEAR_CHOICES,
                               default=datetime.datetime.now().year)
    mid_term_mark = models.FloatField()
    final_mark = models.FloatField(null=True)
    status = models.CharField(max_length=2, choices=MARK_STATUS,
                              default=NOT_PASS)
    avg_mark = models.FloatField()

    class Meta:
        db_table = 'Marks'

    def save(self, *args, **kwargs):
        self.avg_mark = (self.mid_term_mark + self.final_mark) / 2
        super().save(*args, **kwargs)

    def __str__(self):
        return "{}'s {} mark".format(self.student.name, self.subject.title)

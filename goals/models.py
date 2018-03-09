from django.db import models


class Goal(models.Model):
    # CHOICES
    MENTOR = 'MTR'
    MENTEE = 'MTE'
    ROLE_CHOICES = (
        (MENTOR, 'Mentor'),
        (MENTEE, 'Mentee'),
    )

    program_title = models.CharField(max_length=30)
    role = models.CharField(max_length=3, choices=ROLE_CHOICES)
    score = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.role} for {self.program_title}'

    def is_mentor(self):
        return self.role == Goal.MENTOR

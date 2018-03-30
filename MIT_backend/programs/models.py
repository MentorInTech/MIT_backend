"""
Copyright (c) 2018， Silicon Valley Career Women.
All rights reserved.
"""
from django.contrib.auth.models import User
from django.db import models


class Program(models.Model):
    title = models.CharField(max_length=30)
    score = models.IntegerField(blank=True, null=True)
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentor_programs')
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentee_programs')
    goal = models.CharField(max_length=130, blank=True, null=True)
    started = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    ended = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    next_sync_up_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

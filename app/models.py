import json

from django.db import models


class Member(models.Model):
    token = models.CharField(max_length=50, blank=True, unique=True)
    name = models.CharField(max_length=50, blank=True)
    days = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def day_list(self):
        return json.loads(self.days)



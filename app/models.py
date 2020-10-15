import json

from django.db import models
from django.utils import timezone


class Member(models.Model):
    token = models.CharField(max_length=50, blank=True, unique=True)
    name = models.CharField(max_length=50, blank=True)
    days = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def day_list(self):
        return json.loads(self.days)

    @property
    def day_list2(self):
        list1 = self.day_list
        list2 = []
        for day in list1:
            day = '2020-' + day.replace('/', '-')
            list2.append(day)
        return list2

    @classmethod
    def get_recommend(cls):
        all_count = Member.objects.count()
        items = []
        for i in range(100):
            day = timezone.datetime(2020, 11, 1) + timezone.timedelta(days=i)
            day = day.strftime('%m/%d')
            members = []
            for m in Member.objects.all():
                if day in m.day_list:
                    members.append(m)
            count = len(members)
            item = {
                'day': day,
                'count': count,
                'is_full': count == all_count,
                'members': members,
            }
            if count:
                items.append(item)
        items.sort(key=lambda a: a['count'], reverse=True)
        return items[:5]

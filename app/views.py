import random

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from app.models import Member


def index(request):
    status = request.GET.get('status')
    token = request.COOKIES.get('token')
    print('token:', token)

    if not token:
        token = str(random.randint(10000000, 99999999))
        print('new token:', token)

    members = Member.objects.order_by('-id')
    member = Member.objects.filter(token=token).first()

    msg = ''
    if status == '1':
        msg = '恭喜，报名成功！系统会匹配出大家同时有空的聚会日期。'

    recommend = Member.get_recommend()

    response = render(request, 'index.html', locals())
    response.set_cookie('token', token, max_age=3600 * 24 * 365)
    return response


def join(request):
    token = request.GET.get('token', '')
    member = Member.objects.filter(token=token).first()
    if member:
        name = member.name
        init_days = member.day_list2
    else:
        name = ''
        init_days = []
    return render(request, 'join.html', locals())


def submit(request):
    token = request.GET.get('token', '')
    name = request.GET.get('name', '')
    d = request.GET.get('d', '[]')
    m, created = Member.objects.get_or_create(token=token)
    m.name = name
    m.days = d
    m.save()
    return HttpResponseRedirect('/?status=1')


def reject(request):
    token = request.GET.get('token', '')
    Member.objects.filter(token=token).delete()
    return HttpResponseRedirect('/')



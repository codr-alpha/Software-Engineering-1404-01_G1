from django.http import JsonResponse
from django.shortcuts import render
from core.auth import api_login_required
from django.contrib.auth.decorators import login_required
from .models import UserSession, Passage, Question, Option

TEAM_NAME = "team14"

@api_login_required
def ping(request):
    return JsonResponse({"team": TEAM_NAME, "ok": True})

def base(request):
    return render(request, f"{TEAM_NAME}/index.html")

def training_levels(request):
    return render(request, 'team14/training_levels.html')


def index(request):

    last_session = UserSession.objects.filter(
        user=request.user,
        mode='exam',
        end_time__isnull=False,
        scaled_score__isnull=False
    ).order_by('-end_time').first()


    context = {
        'last_score': last_session.scaled_score if last_session else None,
        'has_taken_exam': last_session is not None
    }

    return render(request, 'team14/index.html', context)


login_required(login_url='auth')


def easy_level(request):
    # گرفتن تمام passage های سطح آسان
    passages = Passage.objects.filter(
        difficulty_level='easy'
    ).prefetch_related('questions__options').order_by('-created_at')

    # آماده کردن داده‌ها برای ارسال به template
    passages_data = []
    for passage in passages:
        # شمارش تعداد سوالات
        question_count = passage.questions.count()

        # محاسبه زمان تخمینی (حدود 1 دقیقه برای هر 75 کلمه + 1 دقیقه برای هر سوال)
        estimated_time = (passage.text_length // 75) + question_count

        passages_data.append({
            'id': passage.id,
            'title': passage.title,
            'topic': passage.get_topic_display(),  # نمایش نام فارسی topic
            'text_length': passage.text_length,
            'question_count': question_count,
            'estimated_time': estimated_time,
            'icon': get_topic_icon(passage.topic),  # تابع کمکی برای آیکون
        })

    context = {
        'passages': passages_data,
        'difficulty': 'آسان',
        'total_passages': len(passages_data),
    }

    return render(request, 'team14/Easy_Level.html', context)


@login_required(login_url='auth')
def mid_level(request):
    # گرفتن تمام passage های سطح متوسط
    passages = Passage.objects.filter(
        difficulty_level='medium'
    ).prefetch_related('questions__options').order_by('-created_at')

    passages_data = []
    for passage in passages:
        question_count = passage.questions.count()
        estimated_time = (passage.text_length // 75) + question_count

        passages_data.append({
            'id': passage.id,
            'title': passage.title,
            'topic': passage.get_topic_display(),
            'text_length': passage.text_length,
            'question_count': question_count,
            'estimated_time': estimated_time,
            'icon': get_topic_icon(passage.topic),
        })

    context = {
        'passages': passages_data,
        'difficulty': 'متوسط',
        'total_passages': len(passages_data),
    }

    return render(request, 'team14/Mid_Level.html', context)


@login_required(login_url='auth')
def hard_level(request):
    # گرفتن تمام passage های سطح سخت
    passages = Passage.objects.filter(
        difficulty_level='hard'
    ).prefetch_related('questions__options').order_by('-created_at')

    passages_data = []
    for passage in passages:
        question_count = passage.questions.count()
        estimated_time = (passage.text_length // 75) + question_count

        passages_data.append({
            'id': passage.id,
            'title': passage.title,
            'topic': passage.get_topic_display(),
            'text_length': passage.text_length,
            'question_count': question_count,
            'estimated_time': estimated_time,
            'icon': get_topic_icon(passage.topic),
        })

    context = {
        'passages': passages_data,
        'difficulty': 'سخت',
        'total_passages': len(passages_data),
    }

    return render(request, 'team14/Hard_Level.html', context)


def get_topic_icon(topic):
        icons = {
            'biology': '🧬',
            'history': '📜',
            'astronomy': '🌌',
            'geology': '🌍',
            'anthropology': '🗿',
        }
        return icons.get(topic, '📚')

def Exam_Page(request):
    return render(request, 'team14/Exam_Page.html')



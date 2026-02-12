from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods

from core.auth import api_login_required
from team2.models import Lesson

TEAM_NAME = "team2"

@api_login_required
def ping(request):
    return JsonResponse({"team": TEAM_NAME, "ok": True})

def base(request):
    return render(request, f"{TEAM_NAME}/index.html")

@api_login_required
@require_http_methods(["GET"])
def lessons_list_view(request):
    from team2.models import UserDetails
    
    # بدست آوردن UserDetails کاربر فعلی
    try:
        user_details = UserDetails.objects.using('team2').get(user_id=request.user.id)
        # درس‌های مربوط به کاربر
        lessons = user_details.lessons.filter(
            is_deleted=False,
            status='published'
        ).prefetch_related('videos')
    except UserDetails.DoesNotExist:
        # اگر UserDetails موجود نیست، درس‌های خالی
        lessons = Lesson.objects.none()

    context = {
        'lessons': lessons,
        'total_lessons': lessons.count(),
    }
    # TODO : create team2_Lessons_list.html
    return render(request, 'team2_Lessons_list.html', context)

@api_login_required
@require_http_methods(["GET"])
def lesson_details_view(request, lesson_id):

    lesson = get_object_or_404(
        Lesson,
        id=lesson_id,
        is_deleted=False,
        status='published'
    )

    videos = lesson.videos.filter(is_deleted=False).order_by('-uploaded_at')

    context = {
        'lesson': lesson,
        'videos': videos,
        'total_videos': videos.count(),
    }
    # TODO : create team2_lesson_details.html
    return render(request, 'team2_lesson_details.html', context)
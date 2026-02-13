from django.urls import path
from . import views

urlpatterns = [
    path("", views.base, name="team2_index"),
    path("ping/", views.ping, name="team2_ping"),
    path("lessons/", views.lessons_list_view, name="team2_lessons_list"),
    path("lessons/<int:lesson_id>/", views.lesson_details_view, name="team2_lesson_details"),
    
    path("browse/", views.browse_lessons_view, name="browse_lessons"),
    path("browse/<int:lesson_id>/enroll/", views.enroll_lesson_view, name="enroll_lesson"),
    path("student/lessons/<int:lesson_id>/videos/", views.student_lesson_videos_view, name="student_lesson_videos"),
    path("student/lessons/<int:lesson_id>/watch/<int:video_id>/", views.watch_video_view, name="watch_video"),
    
    path("teacher/lessons/", views.teacher_lessons_view, name="team2_teacher_lessons"),
    path("teacher/lessons/create/", views.teacher_create_lesson_view, name="teacher_create_lesson"),
    path("teacher/lessons/<int:lesson_id>/publish/", views.publish_lesson_view, name="publish_lesson"),
    path("teacher/lessons/<int:lesson_id>/videos/", views.teacher_lesson_videos_view, name="teacher_lesson_videos"),
    path("teacher/lessons/<int:lesson_id>/add-video/", views.add_video_view, name="teacher_add_video"),
    
    path("admin/users/", views.admin_users_view, name="admin_users"),
    path("admin/users/<int:user_id>/change-role/", views.admin_change_role_view, name="admin_change_role"),
]
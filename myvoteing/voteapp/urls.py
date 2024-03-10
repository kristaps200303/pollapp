from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import view_question_responses

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.signup, name="signup"),
    path("mainpage/", views.mainpage, name="mainpage"),
    path('create_poll/', views.create_poll, name='create_poll'),
    path('logout', LogoutView.as_view(next_page='index'), name='logout'),
    path('submit_answer/<int:poll_id>/', views.submit_answer, name='submit_answer'),
    path('responses/', views.view_responses, name='view_responses'),
    path('question/<int:question_id>/responses/', view_question_responses, name='view_question_responses'),
]


from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('point-table', views.point_table, name='point-table'),
    path('score-board', views.score_board, name='score_board'),
    path('standing', views.standing, name='standing'),
    path('schedule', views.schedule, name='schedule'),
    path('teams', views.teams, name='teams'),
]


from django.urls import path

from . import views

urlpatterns = [
	path('port', views.Port.as_view()),
	path('connect', views.Connect.as_view()),
	path('disconnect', views.Disonnect.as_view()),
    path('realtime', views.RealTime.as_view()),
	path('history', views.History.as_view()),
]

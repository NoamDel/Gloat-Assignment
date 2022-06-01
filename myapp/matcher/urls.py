from django.urls import path
# Uncomment line below if path doesn't work (and comment the one above):
# from django.conf.urls import urls

from . import views

urlpatterns = [path('', views.MatcherViewSet.as_view()),
			   path('<int:job_id>/', views.MatcherDetailApiView.as_view()),]

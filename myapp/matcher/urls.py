from django.conf.urls import url
from . import views

urlpatterns = [url('', views.JobViewSet.as_view()),
			   url('/<int:id>/', views.JobViewSet.as_view())]

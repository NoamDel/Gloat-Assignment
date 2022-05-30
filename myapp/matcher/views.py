# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Job
from .serializers import JobSerializer
# Create your views here.


class JobViewSet(APIView):
	def get(self, request, title=None):
		queryset = Job.objects.get(title=title)
		read_serializer = JobSerializer(queryset)

		return Response(read_serializer.data)
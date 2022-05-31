# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Job, Skill, Candidate, models
from .serializers import JobSerializer, CandidateSerializer

from itertools import chain

# Create your views here.


def pull_skill_matching_candidates(serializer):
	"""
	Get candidates with matching skills to the job.
	:param serializer: Serializer object of candidates.
	:return: Queryset of matching candidates
	"""
	job_skills = serializer.data['skills']
	skills_name = [skill['name'] for skill in job_skills]
	skills_objs = Skill.objects.filter(name__in=skills_name)
	candidates_id = skills_objs.values('candidates').distinct()
	candidate_objs = Candidate.objects.filter(id__in=candidates_id)
	return candidate_objs


def pull_title_matching_candidates(serializer):
	"""
	Get candidates with matching title.
	:param serializer: Serializer object of candidates.
	:return: Queryset of matching candidates
	"""
	job_title = serializer.data['title']
	candidate_objs = Candidate.objects.filter(title=job_title)
	return candidate_objs


def find_best_candidates(candidates, serializer):
	"""
	Order candidate by:
		1. Title -
			a. Same title
			b. Partial title
			c. Other title

		2. SKills -
			a. Number of matching skills
			b. Number of skills


	:param candidates: Queryset of candidates
	:return: Queryset of best fitting candidates
	"""
	# IMPORTANT NOTE: Assuming the DB was given unsorted, I would rather
	# 				  sort the candidates after pulling the candidates from the
	# 				  DB and not the whole DB since I don't know if I'm the
	#				  only one whos using it, so it might harm others.
	#				  Otherwise, I would TO BE CONTINUED!

	# Count number of matching skills:
	print("IN FUNCTION!!!!!\n")
	print(f"Job skills: {serializer.data['skills']}")
	job_obj = Job.objects.get(id=serializer.data['id'])
	print(f"CANDIDATES: {candidates[0][0].skills.all()}")
	num_matching = [len(candidate.skills.all() & job_obj.skills.all()) for candidate in candidates[0]]
	title_match_candidates = candidates[0].annotate(skills_num=models.Value(0, models.IntegerField()))
	for i in range(len(title_match_candidates)):
		title_match_candidates[i].skills_num = num_matching[i]

	print(f"\ncandidates new: {title_match_candidates}\n")
	# title_match_candidate = candidates[0].annotate()

	# print(title_match_candidate)
	# return title_match_candidate

	# same_title_cand = candidates.annotate(skills_num=models.Count('skills'))
	# print(same_title_cand)




class JobViewSet(APIView):
	def post(self, request):
		# if title:
		# 	try:
		# 		queryset = Job.objects.get(title=title)
		# 	except Job.DoesNotExist:
		# 		return Response({'errors': 'This Job item does not exists'}, status=400)
		#
		# 	read_serializer = JobSerializer(queryset)
		# 	return Response(read_serializer.data)
		#
		# else:
		create_serializer = JobSerializer(data=request.data)
		if create_serializer.is_valid():

			# Full job title match:
			title_match_candidates = pull_title_matching_candidates(create_serializer)

			# Skills match:
			skills_match_candidates = pull_skill_matching_candidates(create_serializer)

			# candidates = title_match_candidates.union(skills_match_candidates)
			candidates = [title_match_candidates, skills_match_candidates]
			best_candidates = find_best_candidates(candidates, create_serializer)

			if len(title_match_candidates) > 0:
				skill_match_serializer = CandidateSerializer(title_match_candidates, many=True)
				return Response(skill_match_serializer.data)
			else:
				return Response('No fitting candidates for this job!')

		return Response(create_serializer.errors, status=400)

	def get(self, request):
		queryset = Job.objects.get(id=1)
		read_serializer = JobSerializer(queryset)
		return Response(read_serializer.data)


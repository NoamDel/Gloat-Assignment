# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from rest_framework.response import Response
from typing import List

from .models import Job, Skill, Candidate, models
from .serializers import JobSerializer, CandidateSerializer


def pull_skill_matching_candidates(job: models.QuerySet) -> models.QuerySet:
	"""
	Get candidates with matching skills to the job.
	:param serializer: Serializer object of candidates.
	:return: Queryset of matching candidates
	"""
	job_skills = job.values_list('skills', flat=True)
	print(f'job skills: {job_skills}')
	candidates = Candidate.objects.filter(skills__in=job_skills)
	print(f'candidates: {candidates}')
	skills_objs = Skill.objects.filter(name__in=job_skills)
	print(f'skill objects: {skills_objs}')
	candidates_id = skills_objs.values('candidates').distinct()
	candidate_objs = Candidate.objects.filter(id__in=candidates_id)
	return candidate_objs.annotate(skill_num=models.Count('skills'))


def pull_title_matching_candidates(serializer: JobSerializer) -> models.QuerySet:
	"""
	Get candidates with matching title.
	:param serializer: Serializer object of candidates.
	:return: Queryset of matching candidates
	"""
	job_title = serializer.data['title']
	candidate_objs = Candidate.objects.filter(title=job_title)
	return candidate_objs.annotate(skill_num=models.Count('skills'))


def find_best_candidates(candidates: models.QuerySet, serializer: JobSerializer) -> List[Candidate]:
	"""
	Sorts the candidates by different fields and retrieves the best ones.
	:param candidates: Queryset of candidates
	:return: Queryset of best fitting candidates
	"""
	job_obj = Job.objects.get(id=serializer.data['id'])
	print(f"CANDIDATES: {candidates}")
	# Count number of matching skills:
	num_matching = [candidate.skills.all().intersection(job_obj.skills.all()).count() for candidate in candidates]
	# Update all candidates with their matched skills number
	# and title match score:
	for i in range(candidates.count()):
		candidates[i].skill_matches = num_matching[i]
		candidates[i].name_match = calc_name_match_score(candidates[i].title, serializer.data['title'])
		candidates[i].save()

	# Filter by matching skills number and then by overall number of skills:
	candidates = candidates.order_by('-name_match','-skill_matches','-skill_num', '-experience')
	print(f'sorted candidates: {candidates}')
	if candidates.count() > serializer.data['max_candidates']:
		print('less!')
		return candidates[:serializer.data['max_candidates']]

	return candidates


def calc_name_match_score(title: str, job_title: str) -> int:
	"""
	Calculated score for candidate title match.
	:param title: Candidate's title.
	:param job_title: Job's title.
	:return: the number of matching words in both title.
	"""
	return len(set(title.split(' ')).intersection(set(job_title.split(' '))))


class JobViewSet(APIView):
	def post(self, request, id) -> Response:

		job = Job.objects.get(id=id)

		# Full job title match:
		title_match_candidates = pull_title_matching_candidates(job)

		# # Skills match:
		# skills_match_candidates = pull_skill_matching_candidates(job)
		#
		# candidates = title_match_candidates.union(skills_match_candidates)
		# best_candidates = find_best_candidates(candidates, job)

		if title_match_candidates.exists():
			skill_match_serializer = CandidateSerializer(title_match_candidates, many=True)
			return Response(skill_match_serializer.data)
		else:
			return Response('No fitting candidates for this job!')

		# if id:
		# 	try:
		# 		queryset = Job.objects.get(id=id)
		# 	except Job.DoesNotExist:
		# 		return Response({'errors': 'This Job item does not exists'}, status=400)
		#
		# 	read_serializer = JobSerializer(queryset)
		# 	return Response(read_serializer.data)
		#
		# else:
		# 	create_serializer = JobSerializer(data=request.data)
		#
		# 	if create_serializer.is_valid():
		#
		# 		# Full job title match:
		# 		title_match_candidates = pull_title_matching_candidates(create_serializer)
		#
		# 		# Skills match:
		# 		skills_match_candidates = pull_skill_matching_candidates(create_serializer)
		#
		# 		candidates = title_match_candidates.union(skills_match_candidates)
		# 		best_candidates = find_best_candidates(candidates, create_serializer)
		#
		# 		if candidates.exists():
		# 			skill_match_serializer = CandidateSerializer(candidates, many=True)
		# 			return Response(skill_match_serializer.data)
		# 		else:
		# 			return Response('No fitting candidates for this job!')
		#
		# 	return Response(create_serializer.errors, status=400)

	def get(self, request, id=None):
		if id:
			try:
				queryset = Job.objects.get(id=id)

			except Job.DoesNotExist:
				return Response({'errors':'This Job item does not exist.'}, status=400)

			# Full job title match:
			title_match_candidates = pull_title_matching_candidates(queryset)

			# # Skills match:
			# skills_match_candidates = pull_skill_matching_candidates(queryset)
			#
			# candidates = title_match_candidates.union(skills_match_candidates)
			# best_candidates = find_best_candidates(candidates, queryset)

			if title_match_candidates.exists():
				skill_match_serializer = CandidateSerializer(title_match_candidates, many=True)
				return Response(skill_match_serializer.data)
			else:
				return Response('No fitting candidates for this job!')
		else:
			queryset = Job.objects.get(id=1)
			read_serializer = JobSerializer(queryset)
			return Response(read_serializer.data)



		# queryset = Job.objects.get(id=1)
		# read_serializer = JobSerializer(queryset)
		# return Response(read_serializer.data)


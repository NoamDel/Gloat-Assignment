# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from rest_framework.response import Response
from typing import List

from .models import Job, Skill, Candidate, models
from .serializers import JobSerializer, CandidateSerializer


def pull_skill_matching_candidates(job: Job) -> models.QuerySet:
	"""
	Get candidates with matching skills to the job.
	:param serializer: Serializer object of candidates.
	:return: Queryset of matching candidates
	"""
	job_skills = job.skills.all()
	candidates = Candidate.objects.filter(skills__in=job_skills).distinct()
	return candidates.annotate(skill_num=models.Count('skills'))


def pull_name_matching_candidates(job: Job) -> models.QuerySet:
	partial_titles = set(job.title.split(' ') + [job.title])
	candidates = Candidate.objects.values_list("title", "id")
	partially_matched = lambda x: len(set(x.split(' ')).intersection(partial_titles)) > 0
	indices = [candidate[1] for candidate in candidates if partially_matched(candidate[0])]
	candidates = Candidate.objects.filter(id__in=indices)
	return candidates.annotate(skill_num=models.Count('skills'))


def find_best_candidates(candidates: models.QuerySet, job: Job):
	"""
	Sorts the candidates by different fields and retrieves the best ones.
	:param candidates: Queryset of candidates
	:return: Queryset of best fitting candidates
	"""

	# Count number of matching skills:
	num_matching = [len(set(candidate.skills.all()).intersection(set(job.skills.all()))) for candidate in candidates]
	# Update all candidates with their matched skills number
	# and title match score:
	for i in range(candidates.count()):
		candidates[i].job_matches.create(skill_matches=num_matching[i], name_match=calc_name_match_score(candidates[i].title, job.title))

	# Filter by matching skills number and then by overall number of skills:
	candidates = candidates.order_by('-job_matches__name_match','-job_matches__skill_matches','-skill_num', '-experience')
	if candidates.count() > job.max_candidates:
		return candidates[:job.max_candidates]

	return candidates


def calc_name_match_score(title: str, job_title: str) -> int:
	"""
	Calculated score for candidate title match.
	:param title: Candidate's title.
	:param job_title: Job's title.
	:return: the number of matching words in both title.
	"""
	return len(set(title.split(' ')).intersection(set(job_title.split(' '))))


class MatcherViewSet(APIView):
	def get(self, request, id=None):
		'''
		Show all jobs in db.
		:param request: Client request.
		:param id: job id.
		:return: QuerySet of jobs.
		'''
		jobs = Job.objects.all()
		serializer = JobSerializer(jobs, many=True)
		return Response(serializer.data, status=200)


class MatcherDetailApiView(APIView):

	def get(self, request, job_id, *args, **kwargs):
		'''
		Retrieves suitable candidates for the given job.
		:param request: Client request as JSON file.
		:param job_id: job id.
		:param args:
		:param kwargs:
		:return: Candidates in the db which best suited for the job.
		'''
		try:
			job_instance = Job.objects.get(id=job_id)

		except Job.DoesNotExist:
			return Response({'errors':'This Job item does not exist.'}, status=400)

		candidates = self.get_matches(job_instance)
		if candidates.exists:
			skill_match_serializer = CandidateSerializer(candidates, many=True)
			return Response(skill_match_serializer.data)
		else:
			return Response('No fitting candidates for this job!')

	def get_matches(self, job_instance: Job) -> List[Candidate]:
		'''
		Retrieves candidates with partial name match and matching skills. Then, sorts the candidates by their fields
		(number of skills, number of matching skills, name matching) and returns the most suitable ones.
		:param job_instance: Job to look for candidates.
		:return: Candidates.
		'''
		# Name match:
		name_match_candidates = pull_name_matching_candidates(job_instance)
		# Skills match:
		skills_match_candidates = pull_skill_matching_candidates(job_instance)

		if not name_match_candidates.exists:
			candidates = skills_match_candidates
		elif skills_match_candidates.exists:
			candidates = name_match_candidates
		else:
			candidates = name_match_candidates.union(skills_match_candidates)
		# Sort candidates by importance:
		best_candidates = find_best_candidates(candidates, job_instance)

		return best_candidates


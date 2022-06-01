# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Skill(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name


class Job(models.Model):
	title = models.CharField(max_length=200)
	max_candidates = models.IntegerField(default=1)
	# The following relation was chosen in order to make DB more space efficient
	# so that many candidates may have the same skills.
	skills = models.ManyToManyField(Skill, related_name='jobs')
	id = models.AutoField(primary_key=True)

	def __str__(self):
		return self.title


class Candidate(models.Model):
	title = models.CharField(max_length=200)

	# Same as in Job class.
	skills = models.ManyToManyField(Skill, related_name='candidates')

	experience = models.IntegerField(default=0)  # Years of experience.

	id = models.AutoField(primary_key=True)

	def __str__(self):
		return self.title


class JobMatch(models.Model):
	# The following field was made to sort candidates efficiently by
	# using Django API.
	skill_matches = models.IntegerField(default=0)

	# Score for the level of matching to the job title
	name_match = models.IntegerField(default=0)
	candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='job_matches')

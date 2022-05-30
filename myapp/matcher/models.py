# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.


class Candidate(models.Model):
	title = models.CharField(max_length=200)

	def __str__(self):
		return self.title


class Job(models.Model):
	title = models.CharField(max_length=200)

	def __str__(self):
		return self.title


class Skill(models.Model):
	name = models.CharField(max_length=200)
	candidate = models.ManyToManyField(Candidate)
	job = models.ManyToManyField(Job)

	def __str__(self):
		return self.name

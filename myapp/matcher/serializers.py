from rest_framework import serializers

from .models import Job, Skill, Candidate


class SkillSerializer(serializers.ModelSerializer):

	name = serializers.CharField(max_length=200, required=True)

	class Meta:
		model = Skill
		fields = ('name',)


class JobSerializer(serializers.ModelSerializer):

	title = serializers.CharField(max_length=200, required=True)
	skills = SkillSerializer(many=True)
	id = serializers.IntegerField(read_only=False)

	class Meta:
		model = Job
		fields = ('title', 'skills', 'id',)


class CandidateSerializer(serializers.ModelSerializer):

	title = serializers.CharField(max_length=200, required=True)
	skills = SkillSerializer(read_only=True, many=True)

	class Meta:
		model = Candidate
		fields = ('title', 'skills',)

from rest_framework import serializers

from .models import Job, Skill, Candidate


class SkillSerializer(serializers.ModelSerializer):

	name = serializers.CharField(max_length=200, required=True)

	class Meta:
		model = Skill
		fields = ('name',)


class JobSerializer(serializers.ModelSerializer):

	title = serializers.CharField(max_length=200, required=True)
	max_candidates = serializers.IntegerField(read_only=False)
	skills = SkillSerializer(many=True)
	id = serializers.IntegerField(read_only=False)

	class Meta:
		model = Job
		fields = ('title', 'max_candidates', 'skills', 'id',)


class CandidateSerializer(serializers.ModelSerializer):

	title = serializers.CharField(max_length=200, required=True)
	skills = SkillSerializer(read_only=True, many=True)
	skill_matches = serializers.IntegerField(default=0)
	name_match = serializers.IntegerField(default=0)
	experience = serializers.IntegerField(default=0)
	id = serializers.IntegerField(read_only=False)

	class Meta:
		model = Candidate
		fields = ('title', 'skills', 'skill_matches', 'name_match', 'experience', 'id')

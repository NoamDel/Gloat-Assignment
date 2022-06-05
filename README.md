# Gloat-Assignment

IMPORTENT NOTE:
	I assumed there are no duplicates at 'Skill' table.
	This was assumed in order to save space in the DB and save
	time when looking up candidates with fitting skills for the job.
	
	This assumption impacts the way new entries added to the DB,
	when adding new candidates or jobs, we should reference already added skills
	to avoid creating duplicates at 'Skill' table.
	This only applies for skills that already appears in the table.

	In order to add skills for jobs or candidates it would be easier to 
	create variables of the skills and then reference them when adding 
	jobs and candidates, for example:

	skill1 = ...
	skill2 = ...
	skill3 = ...
	
	candidate1 = Candidate(title=...,skills=(skill1, skill2))
	candidate2 = Candidate(title=..., skills=skill2)
	candiadte3 = Candidate(title=..., skills=(skill1,skill2,skill3))

goal="SDE"
year_of_job=0
self_eva=1
result=svcw.objects.raw('select name, (svcw.skill_self_eval-%d)+(svcw.year_of_job_category - %d)/2 as score,[self_eva],[year_of_job]
						from svcw
						where svcw.prog1.buddy_name=%s,[goal]
						having svcw.year_of_job_category - %d>=3, [year_of_job]
						order by score desc
						limit 5')
#for r in result:
#	print("%s %s" %(r.name, r.score))


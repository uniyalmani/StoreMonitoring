# StoreMonitoring
#command to run docker-compose up
#requirement       
1) TOPIC_NAME
2)`S3_ACCESS_KEY_ID
3) S3_AWS_SECRET_ACCESS_KEY
4) BUCKET_NAME

tech stack used 
1) ***FastApi***
2) ***sqlmodel(orm)***
3) ***docker, docker-compose*** for containerization
4) ***kafka *** (to run bakground task  )

*end points - > 
1) ***http://0.0.0.0:8000/trigger_report***
2) ***http://0.0.0.0:8000/get_report?report_id=c1d0fafc-5ab8-4fd9-9b1b-4ab7ede35973***


**basic algo for extrapolate uptime and downtime **
# algo is based on averaging 
```
{
we find total active count and inactve count in an interval,
we find total schedule opening of store,
and then devide total schedule opening to both active and inactive based on there count(ratio),
for last one hours uptime we are considering that whole day  total schedule opening and also total number of active count and inactive count in that day,
and then reducing it to one hours.
}
```

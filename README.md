# StoreMonitoring
#command to run docker-compose up
tech stack used 
1) ***FastApi***
2) ***sqlmodel(orm)***
3) ***docker, docker-compose*** for containerization
4) ***kafka *** (to run bakground task  )

*end points - > 
1) ***http://0.0.0.0:8000/trigger_report***
2) ***http://0.0.0.0:8000/get_report?report_id=**


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

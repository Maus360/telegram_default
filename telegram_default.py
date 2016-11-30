import requests
import datetime

classes=[155, 260, 375, 480, 595]
times_set={1:"7:00-9:35", 2:"9:45-11:20", 3:"11:40-13:15", 4:"13:25-15:00", 5:"15:20-16:55"}
days={"Mon":1, "Tue":2, "Wed":3, "Thu":4, "Fri":5, "Sat":6}

def default_set():
	date = str(datetime.datetime.now())[8:10]

	month = str(datetime.datetime.now())[5:7]

	year = str(datetime.datetime.now())[:4]
    #делаем запрос на сайт с текущей датой
	response = requests.get(url="http://www.bsuir.by/schedule/rest/currentWeek/date/" + date + "." + month + "." + year)

	week_default = str(response.content)[2]

	day_default = days[response.headers['date'][:3]]
    #в этой переменной хранится текущее время в минутах
	time = int(str(datetime.datetime.now())[11:13]) * 60 + int(str(datetime.datetime.now())[14:16])
    #в списке classes есть разница времени между началом и концом пары(первая пара начинается в семь часов утра)
	for i in range(1, len(classes)):
		if time - 420 < classes[i]:
			time_default = times_set[i + 1]
		else:
			time_default = times_set[1]
	building_default=4
	return {"week":week_default,"day":day_default,"build":building_default,"time":time_default}

#print(default_set())
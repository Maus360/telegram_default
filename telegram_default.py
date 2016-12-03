import calendar
import requests
import datetime

classes=[155, 260, 375, 480, 595, 700]
times_set={1:"7:00-9:35", 2:"9:45-11:20", 3:"11:40-13:15", 4:"13:25-15:00", 5:"15:20-16:55", 6:"17:05-18:40"}
days={"Mon":1, "Tue":2, "Wed":3, "Thu":4, "Fri":5, "Sat":6}

date = str(datetime.datetime.now())[8:10]

month = str(datetime.datetime.now())[5:7]

year = str(datetime.datetime.now())[:4]
#делаем запрос на сайт с текущей датой
response = requests.get(url="http://www.bsuir.by/schedule/rest/currentWeek/date/" + date + "." + month + "." + year)
def default_week():
	return str(response.content)[2]
def default_day():
	return calendar.weekday(int(year),int(month),int(date))+1
def default_time():
	#в этой переменной хранится текущее время в минутах
	time = int(str(datetime.datetime.now())[11:13]) * 60 + int(str(datetime.datetime.now())[14:16])
	# в списке classes есть разница времени между началом и концом пары(первая пара начинается в семь часов утра)
	for i in range(1, len(classes)):
		if time - 420 < classes[i]:
			time_default = times_set[i + 1]
		else:
			time_default = times_set[1]
	return time_default
def default_build():
	return 4

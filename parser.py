from requests import Session
from config import PASSWORD, USERNAME, logger
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import time as dttime
from datetime import date


month = {
	"Янв": 1,
	"Фев": 2,
	"Мар": 3,
	"Апр": 4,
	"Май": 5,
	"Июн": 6,
	"Июл": 7,
	"Авг": 8,
	"Сен": 9,
	"Окт": 10,
	"Ноя": 11,
	"Дек": 12
}

time = {
	0: dttime(10, 30),
	1: dttime(12, 10),
	2: dttime(13, 50),
	3: dttime(16, 0),
	4: dttime(17, 40),
	5: dttime(19, 20),
	6: dttime(21, 00),
}
week_day = datetime.weekday(datetime.now())
mytime = 0
for key, val in time.items():
	if datetime.now().time() >= val:
		mytime = key

logger.info(f"Today is {week_day} week day. {mytime} pair is gone")

def parse_schedule():
	s = Session()
	data = {"ulogin": USERNAME, "upassword": PASSWORD, "auth_action": "userlogin"}
	l = s.post("https://e.mospolytech.ru/old/index.php", data=data).text
	html = s.get("https://rasp.dmami.ru/site/group-html?group=221-363&token=7538b7c53be15fbc6cbb20b85e7976a7").text

	soup = BeautifulSoup(html, 'html.parser')
	week = soup.find_all("div", class_="schedule-day")

	if week_day == 6:
		logger.warning("Yeah Sunday")
		return None
	else:
		lessons = week[week_day].find_all("div", class_="pair")
		lesson = lessons[mytime]
		mylessons = lesson.find_all("div", class_="lessons")
		for mylesson in mylessons:
			if mylesson is None:
				logger.warning("There are currently no lectures")
				return None
			a = mylesson.find("a")
			if a is None:
				logger.warning("Link not found")
				return None

			link = a.get("href")
			logger.info(f"Link is {link}")
			date_string = mylesson.find("div", class_="schedule-dates").text
			start_date, end_date = map(lambda x: list(x.split()), date_string.split(" - "))

			start_date[1] = month[start_date[1]]
			start_date[0] = int(start_date[0])

			end_date[1] = month[end_date[1]]
			end_date[0] = int(end_date[0])

			end = date(2022, end_date[1], end_date[0])
			start = date(2022, start_date[1], start_date[0])
			
			now_date = datetime.now().date()
			logger.debug(f"end: {end} start: {start} now: {now_date}")
			if end >= now_date >= start:
				logger.info(f'lesson is {mylesson.find("div", class_="bold small").text}')
				return link
	logger.warning("There are currently no lectures")
	return None
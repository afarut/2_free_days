from lecture import go_to_lecture
from parser import parse_schedule
from config import logging


link = parse_schedule()
#print(link)
#link = "https://events.webinar.ru/61441981/1037921682/stream-new/1127538413"
if link is None:
    pass
else:
    go_to_lecture(link)
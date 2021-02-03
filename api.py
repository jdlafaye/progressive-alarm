from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel

ALARMS_FILE = '/etc/alarm/alarms.txt'

app = FastAPI()


class Alarm(BaseModel):
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int


@app.post('/alarm')
def post_alarm(alarm: Alarm):
    alarm_time = datetime(alarm.year, alarm.month, alarm.day, alarm.hour, alarm.minute, alarm.second)
    with open(ALARMS_FILE, 'a') as alarms_file:
        alarms_file.write(alarm_time.isoformat())
        alarms_file.write('\n')
    return 204


@app.get('/alarms')
def get_alarms():
    with open(ALARMS_FILE, 'r') as alarms_file:
        return [alarm.strip() for alarm in alarms_file.readlines()]

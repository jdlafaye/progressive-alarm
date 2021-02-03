#!/usr/bin/env python3
from datetime import datetime
from time import sleep

from gpiozero import Button
from pygame import mixer

ALARMS_FILE = 'alarms.txt'
SOUND_FILE = 'alarm.wav'

button = Button(2)


def should_alarm(alarm_time: str) -> bool:
    return datetime.now() > datetime.fromisoformat(alarm_time)


def alarm():
    mixer.music.load(SOUND_FILE)
    while True:
        mixer.music.play()
        while mixer.music.get_busy():
            if button.is_pressed:
                mixer.music.stop()
                mixer.music.unload()
                return


def main():
    mixer.init()
    while True:
        with open(ALARMS_FILE, 'r') as alarms_file:
            alarm_times = alarms_file.readlines()
        upcoming_alarm_times = [alarm_time for alarm_time in alarm_times if not should_alarm(alarm_time.strip())]
        if len(upcoming_alarm_times) < len(alarm_times):
            alarm()
            with open(ALARMS_FILE, 'w') as alarms_file:
                for alarm_time in upcoming_alarm_times:
                    alarms_file.write(alarm_time)
        sleep(1)


if __name__ == '__main__':
    main()

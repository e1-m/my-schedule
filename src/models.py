import json
import os
import sys
from io import StringIO
from threading import Thread
from time import sleep

import pyperclip
import schedule as planner

from settings import settings
from scaners import scan_int
import utils
import consts


class Menu:
    def __init__(self, text_fun, options_fun):
        """
        :param text_fun: function that return text to be displayed as a menu
        :param options_fun: function that return dictionary of options (must be keyed as in the text)
        """

        self.text_fun = text_fun
        self.options_fun = options_fun

    def open_menu(self, param=None, on_exit=None) -> None:
        """
        :param param: additional parameter to be passed down to text_fun and options_fun
        :param on_exit: function to be called before returning
        """
        while True:
            os.system('cls')
            text = self.text_fun(param) if param else self.text_fun()
            choice: int = scan_int(text)
            if choice == 0:
                on_exit and on_exit()
                return
            options = self.options_fun(param) if param else self.options_fun()
            if len(options) >= choice > 0:
                options[choice]()


class Time:
    def __init__(self, hours: int = 0, minutes: int = 0):
        self.hours = hours
        self.minutes = minutes

    def get_str(self) -> str:
        """
        :return: string representation of the time in HH:MM format
        """
        hours = self.hours if self.hours >= 10 else '0' + str(self.hours)
        minutes = self.minutes if self.minutes >= 10 else '0' + str(self.minutes)
        return f"{hours}:{minutes}"

    def add_minutes(self, minutes_to_add: int):
        """
        :param minutes_to_add: the number of minutes to add
        :return: new object of Time with added minutes
        """
        minutes = self.hours * 60 + self.minutes + minutes_to_add
        if minutes >= 1440:
            minutes -= 1440
        return Time(int(minutes / 60), minutes % 60)

    def subtract_minutes(self, minutes_to_subtract: int):
        """
        :param minutes_to_subtract: the number of minutes to subtract
        :return: new object of Time with subtracted minutes
        """
        minutes = self.hours * 60 + self.minutes - minutes_to_subtract
        if minutes < 0:
            minutes += 1440
        return Time(int(minutes / 60), minutes % 60)

    def get_in_minutes(self) -> int:
        """
        :return: the number of minutes from 00:00
        """
        return self.hours * 60 + self.minutes

    def __str__(self):
        return self.get_str()


class Conference:
    def __init__(self, title: str, link: str, start_time: str, duration: int = settings['default_conference_duration'],
                 password: str = None, autostart_permission: bool = True, week: int = consts.EVERY_WEEK):
        self.title = title
        self.link = link
        self.start_time: Time = Time(*map(int, start_time.split(':')))
        self.duration = duration
        self.password = password
        self.autostart_permission = autostart_permission
        self.week = week

    def start_conference(self) -> None:
        """
        Opens the conference link and copies the password to the clipboard if it exists.
        """
        os.system('start ' + self.link)
        self.copy_password()

    def copy_password(self) -> None:
        """
        Copies the password to the clipboard if it exists.
        """
        if self.password:
            pyperclip.copy(self.password)

    def set_new_password(self, new_password: str) -> None:
        self.password = new_password

    def set_new_title(self, new_title: str) -> None:
        self.title = new_title

    def set_new_start_time(self, new_start_time: str) -> None:
        self.start_time = Time(*map(int, new_start_time.split(':')))

    def set_new_duration(self, new_duration: int) -> None:
        self.duration = new_duration

    def set_new_link(self, new_link: str) -> None:
        self.link = new_link

    def set_autostart_permission(self, autostart_permission: bool) -> None:
        self.autostart_permission = autostart_permission

    def set_week(self, week: int) -> None:
        if 0 <= week <= 2:
            self.week = week

    def to_dict(self) -> dict:
        """
        Converts the object to a dictionary
        :return: representation of the object as a dictionary
        """
        data: dict = {
            'title': self.title,
            'link': self.link,
            'autostart_permission': self.autostart_permission,
            'password': self.password,
            'start_time': self.start_time.get_str(),
            'duration': self.duration,
            'week': self.week,
        }
        return data

    def __str__(self):
        return f"{self.title} ({self.start_time} - {self.start_time.add_minutes(self.duration)})"


class Schedule:
    def __init__(self, filename: str = 'schedule'):
        self.filename = filename
        self.conferences: dict = {
            'monday': [],
            'tuesday': [],
            'wednesday': [],
            'thursday': [],
            'friday': [],
            'saturday': [],
            'sunday': [],
        }
        self.read_schedule()
        self.update_autostart_planner()

        def autostart():
            while True:
                while settings['autostart']:
                    planner.run_pending()
                    sleep(1)
                sleep(1)

        Thread(daemon=True, target=autostart).start()

    def get_daily_schedule(self, day: str) -> list:
        """
        :return: list of conferences on the day
        """
        return self.conferences.get(day)

    def get_this_week_daily_schedule(self, day: str) -> list:
        """
        :return: list of conferences on the day
        """
        current_week = utils.get_week()
        return list(
            filter(lambda conf: conf.week == consts.EVERY_WEEK or conf.week == current_week % 2, self.conferences.get(day)))

    def get_today_schedule(self) -> list:
        """
        :return: list of today's conferences
        """
        return self.get_this_week_daily_schedule(utils.get_today())

    def get_days_with_conferences(self) -> list:
        """
        :return: list of days with at least one conference
        """
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        return [day for day in days if self.conferences[day]]

    def add_conference(self, day: str, conference_to_add: Conference) -> None:
        """
        Add the conference to the schedule
        :param day: day to which should add the conference
        :param conference_to_add:
        """
        self.conferences.get(day).append(conference_to_add)

    def shift_time_of_all_conferences(self, minutes: int) -> None:
        """
        Shifts the time of all conferences backward if the minutes are negative and forward if the minutes are positive
        """
        if minutes == 0:
            return
        for day in self.conferences:
            for conference in self.conferences[day]:
                if minutes > 0:
                    conference.start_time = conference.start_time.add_minutes(minutes)
                else:
                    conference.start_time = conference.start_time.subtract_minutes(-minutes)

    def sort_schedule(self):
        for day in self.get_days_with_conferences():
            self.get_daily_schedule(day).sort(key=lambda conference: conference.start_time.get_in_minutes())

    def update_autostart_planner(self) -> None:
        """
        Adds today's conferences to the autostart planner
        """
        planner.clear()
        for conference in self.get_today_schedule():
            if conference.autostart_permission:
                planner.every().day.at(
                    conference.start_time.subtract_minutes(settings['pre-start_minutes']).get_str()).do(
                    lambda c=conference: c.start_conference())

    def delete_conference(self, conference: Conference) -> None:
        """
        Removes the conference from the schedule
        """
        for day in self.conferences:
            for i, c in enumerate(self.conferences[day]):
                if c == conference:
                    del self.conferences[day][i]
                    sys.stdin = StringIO('0\n')
                    return

    def change_file(self, filename: str) -> None:
        """
        Changes the schedule file and read it
        :param filename: The name of the new file
        """
        self.filename = filename
        self.conferences: dict = {
            'monday': [],
            'tuesday': [],
            'wednesday': [],
            'thursday': [],
            'friday': [],
            'saturday': [],
            'sunday': [],
        }
        self.read_schedule()
        self.update_autostart_planner()

    def to_dict(self) -> dict:
        """
        Converts the object to a dictionary
        :return: representation of the object as a dictionary
        """
        json_form_of_schedule: dict = {
            'monday': [],
            'tuesday': [],
            'wednesday': [],
            'thursday': [],
            'friday': [],
            'saturday': [],
            'sunday': [],
        }
        for day, day_schedule in self.conferences.items():
            for conference in day_schedule:
                json_form_of_schedule[day].append(conference.to_dict())
        return json_form_of_schedule

    def from_dict(self, schedule_dict: dict) -> None:
        """
        Sets the schedule from the dictionary
        """
        for day, day_schedule in schedule_dict.items():
            for conference in day_schedule:
                self.conferences[day].append(Conference(**conference))

    def write_schedule(self) -> None:
        """
        Writes the schedule to the current schedule file
        """
        with open(f"files/schedules/{self.filename}.json", 'w') as f:
            json.dump(self.to_dict(), f)

    def read_schedule(self) -> None:
        """
        Reads the schedule from the current schedule file
        """
        try:
            with open(f"files/schedules/{self.filename}.json", 'r') as f:
                self.from_dict(json.load(f))
        except FileNotFoundError:
            return

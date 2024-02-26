import os
from my_schedule import schedule
from models import Menu, Conference
import consts
from texts import texts, read_texts
from settings import settings, write_settings
from scaners import scan_int, scan_time, scan_filename, scan_color


def change_week(conference):
    os.system('cls')
    options = {
        1: lambda: conference.set_week(consts.ODD_WEEK),
        2: lambda: conference.set_week(consts.EVEN_WEEK),
        3: lambda: conference.set_week(consts.EVERY_WEEK),
    }
    option_number = scan_int(
        f"1. {texts['week']['odd_week']}\n2. {texts['week']['even_week']}\n3. {texts['week']['every_week']}\n",
        1, 3)
    options[option_number]()


def change_time(conference):
    conference.set_new_start_time(scan_time(texts['edit_conference']['new_start_time_input']))
    schedule.sort_schedule()


def edit_conference_options(conference):
    return {
        1: lambda: conference.set_new_title(input(texts['edit_conference']['new_title_input'])),
        2: lambda: conference.set_new_link(input(texts['edit_conference']['new_link_input'])),
        3: lambda: change_time(conference),
        4: lambda: conference.set_new_password(input(texts['edit_conference']['new_password_input'])),
        5: lambda: conference.set_new_duration(scan_int(texts['edit_conference']['new_duration_input'], 1, 300)),
        6: lambda: conference.set_autostart_permission(not conference.autostart_permission),
        7: lambda: change_week(conference),
        8: lambda: schedule.delete_conference(conference),
    }


def edit_conference_text(conference):
    return (f"1. {texts['edit_conference']['title']}{conference.title}\n"
            f"2. {texts['edit_conference']['link']}{conference.link}\n"
            f"3. {texts['edit_conference']['start_time']}{conference.start_time}\n"
            f"4. {texts['edit_conference']['password']}"
            f"{conference.password or texts['edit_conference']['password_does_not_exist']}\n"
            f"5. {texts['edit_conference']['duration']}{conference.duration}\n"
            f"6. {texts['edit_conference']['auto_start_permission_true'] if conference.autostart_permission else texts['edit_conference']['auto_start_permission_false']}\n"
            f"7. {texts['edit_conference']['week']}{texts['week']['odd_week'] if conference.week == consts.ODD_WEEK else texts['week']['even_week'] if conference.week == consts.EVEN_WEEK else texts['week']['every_week']}\n"
            f"8. {texts['edit_conference']['delete']}\n"
            f"{texts['back']}")


edit_conference_menu: Menu = Menu(edit_conference_text, edit_conference_options)


def add_conference(day: str):
    title: str = input(texts['add_conference']['title_input'])
    start_time: str = scan_time(texts['add_conference']['time_input'])
    link: str = input(texts['add_conference']['link_input'])
    schedule.add_conference(day, Conference(title=title, start_time=start_time, link=link))
    schedule.sort_schedule()


def edit_daily_schedule_options(day: str) -> dict:
    options: dict = {i + 2: (lambda val=value: edit_conference_menu.open_menu(val)) for i, value in
                     enumerate(schedule.get_daily_schedule(day))}
    options[1] = lambda: add_conference(day)
    return options


def edit_daily_schedule_text(day: str) -> str:
    text: str = f"1. {texts['add_conference']['add_conference']}"
    for i, conference in enumerate(schedule.get_daily_schedule(day)):
        text += f'{i + 2}. {conference}\n'
    text += texts['back']
    return text


edit_daily_schedule_menu: Menu = Menu(edit_daily_schedule_text, edit_daily_schedule_options)


def edit_weekly_schedule_options() -> dict:
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    return {i + 1: (lambda d=day: edit_daily_schedule_menu.open_menu(d, on_exit=schedule.update_autostart_planner)) for
            i, day in enumerate(days)}


edit_weekly_schedule_menu: Menu = Menu(lambda: texts['schedule_menu'], edit_weekly_schedule_options)


def autostart_menu_options() -> dict:
    return {
        1: lambda: settings.__setitem__('autostart', not settings['autostart']),
        2: lambda: settings.__setitem__('pre-start_minutes',
                                        scan_int(texts['autostart_menu']['pre-start_minutes_input'], min_val=0,
                                                 max_val=10))
    }


autostart_menu: Menu = Menu(
    lambda: f"{texts['autostart_menu']['autostart_true'] if settings['autostart'] else texts['autostart_menu']['autostart_false']}"
            f"{texts['autostart_menu']['pre-start_minutes']}({settings['pre-start_minutes']})\n{texts['back']}",
    autostart_menu_options)


def time_menu_options() -> dict:
    return {
        1: lambda: settings.__setitem__('default_conference_duration', scan_int(texts['time_menu']['duration_input'])),
        2: lambda: schedule.shift_time_of_all_conferences(scan_int(texts['time_menu']['move_time_input'])),
    }


def time_menu_text() -> str:
    return (f"{texts['time_menu']['duration']} ({settings['default_conference_duration']} {texts['minutes']})\n"
            f"{texts['time_menu']['move_time']}\n{texts['back']}")


time_menu: Menu = Menu(time_menu_text, time_menu_options)


def change_language(language):
    settings.__setitem__('language', language),
    read_texts(language)


def language_menu_options() -> dict:
    return {
        1: lambda: change_language('en'),
        2: lambda: change_language('uk'),
        3: lambda: change_language('ru'),
        4: lambda: change_language('de'),
    }


language_menu: Menu = Menu(lambda: texts['language_menu'], language_menu_options)


def change_schedule_file():
    settings.__setitem__('schedule_filename',
                         scan_filename(f"{texts['schedule_file_input']}{settings['schedule_filename']}): "))
    schedule.change_file(settings['schedule_filename'])


def change_console_color():
    os.system('cls')
    settings.__setitem__('console_color', scan_color(texts['console_color_input']))
    os.system('color ' + settings['console_color'])


def settings_menu_options() -> dict:
    return {
        1: lambda: edit_weekly_schedule_menu.open_menu(on_exit=schedule.write_schedule),
        2: lambda: autostart_menu.open_menu(on_exit=schedule.update_autostart_planner),
        3: lambda: time_menu.open_menu(on_exit=schedule.update_autostart_planner),
        4: lambda: language_menu.open_menu(),
        5: change_console_color,
        6: change_schedule_file,
        7: lambda: settings.__setitem__('open_in_tray', not settings['open_in_tray']),
    }


def settings_menu_text() -> str:
    return (f"{texts['settings_menu']['main_part']}"
            f"{texts['settings_menu']['open_in_tray_true'] if settings['open_in_tray'] else texts['settings_menu']['open_in_tray_false']}"
            f"{texts['back']}")


settings_menu: Menu = Menu(settings_menu_text, settings_menu_options)


def conferences_menu_options(day: str) -> dict:
    return {i + 1: lambda conf=value: conf.start_conference() for i, value in
            enumerate(schedule.get_this_week_daily_schedule(day))}


def conferences_menu_text(day: str) -> str:
    text: str = ""
    for i, conference in enumerate(schedule.get_this_week_daily_schedule(day)):
        text += f"{i + 1}. {conference}\n"
    text += texts['back']
    return text


conferences_menu: Menu = Menu(conferences_menu_text, conferences_menu_options)


def days_menu_options() -> dict:
    return {i + 1: lambda day=value: conferences_menu.open_menu(day) for i, value in
            enumerate(schedule.get_days_with_conferences())}


def days_menu_text() -> str:
    text: str = ""
    for i, day in enumerate(schedule.get_days_with_conferences()):
        text += f"{i + 1}. {texts['days'][day]}\n"
    text += texts['back']
    return text


schedule_menu: Menu = Menu(days_menu_text, days_menu_options)


def main_menu_options() -> dict:
    return {
        1: schedule_menu.open_menu,
        2: lambda: settings_menu.open_menu(on_exit=write_settings),
    }


main_menu: Menu = Menu(lambda: texts['main_menu'], main_menu_options)

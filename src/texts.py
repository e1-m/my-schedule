import json

texts: dict = {
    'main_menu': '1. Show schedule\n'
                 '2. Settings\n'
                 '0. Minimize to system tray\n'
                 '==>',
    'settings_menu': {
        'main_part': 'Settings:\n'
                     '1. Schedule\n'
                     '2. Automatic start of conferences\n'
                     '3. Time\n'
                     '4. Language\n'
                     '5. Console color\n'
                     '6. Change schedule file\n',
        'open_in_tray_true': '7. Do not open in tray at start\n',
        'open_in_tray_false': '7. Open in tray at start\n',
    },
    'schedule_menu': '1. Monday\n'
                     '2. Tuesday\n'
                     '3. Wednesday\n'
                     '4. Thursday\n'
                     '5. Friday\n'
                     '6. Saturday\n'
                     '7. Sunday\n'
                     '0. Back\n'
                     '==>',
    'autostart_menu': {
        'autostart_true': '1. Disable autostart\n',
        'autostart_false': '1. Enable autostart\n',
        'pre-start_minutes': '2. Preparatory time',
        'pre-start_minutes_input': 'Please enter the number of the pre-start minutes:',
    },
    'time_menu': {
        'duration': '1. Default duration of conferences',
        'move_time': '2. Move the start time of all conferences',
        'duration_input': 'Please enter default duration of conference (minutes): ',
        'move_time_input': 'Please enter minutes to move (negative number if backward):',
    },
    'language_menu': 'Choose a language:\n'
                     '1. English\n'
                     '2. Українська\n'
                     '3. Русский\n'
                     '4. Deutsch\n'
                     '0. Back\n'
                     '==>',
    'add_conference': {
        'add_conference': 'Add conference\n',
        'title_input': 'Please enter the title of the conference: ',
        'time_input': 'Please enter the start time of the conference (HH:MM): ',
        'link_input': 'Please enter the link to the conference (full link): ',
        'duration_exception': 'The conference cannot be added. This time has already been occupied'
    },
    'edit_conference': {
        'title': 'Title: ',
        'start_time': 'Start time: ',
        'link': 'Link: ',
        'password': 'Password: ',
        'duration': 'Duration: ',
        'password_does_not_exist': 'Password has not been set yet',
        'auto_start_permission_false': 'Allow the conference to start automatically',
        'auto_start_permission_true': 'Prevent the conference from starting automatically',
        'delete': 'Delete the conference',
        'new_title_input': 'Please enter a new title of the conference: ',
        'new_start_time_input': 'Please enter a new start time of the conference (HH:MM): ',
        'new_link_input': 'Please enter a new link to the conference (full link): ',
        'new_password_input': 'Please enter a new password to log into the conference: ',
        'new_duration_input': 'Please enter a new duration of the conference (in minutes): ',
    },
    'days': {
        'monday': 'Monday',
        'tuesday': 'Tuesday',
        'wednesday': 'Wednesday',
        'thursday': 'Thursday',
        'friday': 'Friday',
        'saturday': 'Saturday',
        'sunday': 'Sunday',
    },
    'minutes': 'min',
    'back': '0. Back\n'
            '==>',
    'console_color_input': '1 - Black\n2 - Blue\n3 - Green\n4 - Light Blue'
                           '\n5 - Red\n6 - Purple\n7 - Yellow\n8 - White\n9 - Grey\n'
                           'Enter the color numbers using "/" (text/background): \n',
    'schedule_file_input': 'Enter a filename of the schedule file without extension. (Current filename: ',
    'filename_input_exception': 'Invalid file name. Filename should not contain: / : \\ * ? " < > | .',
    'int_input_exception': 'The value must be an integer number. Please enter an integer number: ',
    'time_input_exceptions': {
        'incorrect_format': 'The value must be in HH:MM format. Please enter again: ',
        'incorrect_data': 'Incorrect time. Please enter again: ',
    },
    'color_input_exceptions': {
        'incorrect_format': 'The value must be in text/background format. Please enter again: ',
        'incorrect_data': 'The numbers are out of range or text = background. Please enter again: ',
    },
    'min_value_exception': 'The value must be greater or equal to ',
    'max_value_exception': 'The value must be smaller or equal to ',
}


def read_texts(language):
    try:
        with open(f"files/lang/{language}.json", 'r') as f:
            texts.update(json.load(f))
    except FileNotFoundError:
        return


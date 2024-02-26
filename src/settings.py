import json

settings: dict = {
    'default_conference_duration': 80,
    'autostart': True,
    'pre-start_minutes': 1,
    'language': 'en',
    'schedule_filename': 'schedule',
    'console_color': '8F',
    'open_in_tray': False,
}


def write_settings():
    with open('files/cfg/cfg.json', 'w') as f:
        json.dump(settings, f)


def read_settings():
    try:
        with open('files/cfg/cfg.json', 'r') as f:
            settings.update(json.load(f))
    except FileNotFoundError:
        return


read_settings()

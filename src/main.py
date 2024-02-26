import os
import sys
from menus import main_menu
from settings import settings
from texts import read_texts


def switch_to_tray():
    os.system('start tray.exe')


def main(is_it_tray_request):
    if settings['open_in_tray'] and not is_it_tray_request:
        switch_to_tray()
        return
    os.system('color ' + settings['console_color'])
    read_texts(settings['language'])
    main_menu.open_menu(on_exit=switch_to_tray)


if __name__ == '__main__':
    main(True if "True" in sys.argv else False)

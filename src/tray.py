import os
import pystray
from PIL import Image
from my_schedule import schedule


def switch_to_main(icon):
    os.system('start MySchedule.exe True')
    icon.stop()


def run_tray_icon():
    menu_items = [pystray.MenuItem(f"{conference}", conference.start_conference) for conference in
                  schedule.get_today_schedule()]
    menu_items.append(pystray.MenuItem('Open', lambda icn: switch_to_main(icn)))
    menu_items.append(pystray.MenuItem('Quit', lambda icn: icn.stop()))
    icon = pystray.Icon("MySchedule", Image.open("icons/icon.png"), menu=pystray.Menu(*menu_items))
    icon.run()


if __name__ == '__main__':
    run_tray_icon()

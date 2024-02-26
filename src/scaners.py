import sys
from texts import texts
import re


def scan_int(text: str = '', min_val: int = None, max_val: int = None) -> int:
    """
    The function scans input until a valid integer number is scanned
    :param min_val: lower bound of the scanning integer number (min_val within the range)
    :param max_val: upper bound of the scanning integer number (max_val within the range)
    :param text: text to be displayed
    :return: integer number
    """
    while True:
        try:
            num: int = int(input(text))
            if sys.stdin != sys.__stdin__:
                sys.stdin = sys.__stdin__
            if min_val != None and num < min_val:
                print(f"{texts['min_value_exception']}{min_val}")
                continue
            if max_val != None and num > max_val:
                print(f"{texts['max_value_exception']}{max_val}")
                continue
        except ValueError:
            print(texts['int_input_exception'])
            continue
        return num


def scan_time(text='') -> str:
    """
     The function scans input until a valid time in HH:MM format is scanned
     :param text: text to be displayed
     :return: string in HH:MM format
     """
    while True:
        time_str: str = input(text)
        if re.match(r'^\d{2}:\d{2}$', time_str) or re.match(r'^\d:\d{2}$', time_str):
            hours, minutes = map(int, time_str.split(':'))
            if 0 <= hours <= 23 and 0 <= minutes <= 59:
                return time_str
            else:
                print(texts['time_input_exceptions']['incorrect_data'])
        else:
            print(texts['time_input_exceptions']['incorrect_format'])


def scan_color(text='') -> str:
    """
     The function scans input until a valid console color is scanned
     :param text: text to be displayed
     :return: string representing a console color
     """
    colors = {
        1: '0',
        2: '1',
        3: '2',
        4: '3',
        5: '4',
        6: '5',
        7: '6',
        8: 'F',
        9: '8',
    }
    while True:
        color_str: str = input(text)
        if re.match(r'^\d/\d$', color_str):
            text_color, background_color = map(int, color_str.split('/'))
            if 1 <= text_color <= 9 and 1 <= background_color <= 9 and text_color != background_color:
                return f"{colors[background_color]}{colors[text_color]}"
            else:
                print(texts['color_input_exceptions']['incorrect_data'])
        else:
            print(texts['color_input_exceptions']['incorrect_format'])


def scan_filename(text='') -> str:
    """
    The function scans input until a valid filename is scanned
    :param text: text to be displayed
    :return: string containing the filename without an extension
    """
    while True:
        forbidden_chars = r'[\\/:*?"<>|.]'
        filename: str = input(text)
        if not re.search(forbidden_chars, filename):
            return filename
        else:
            print(texts['filename_input_exception'])

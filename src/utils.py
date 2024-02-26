from datetime import datetime


def get_today() -> str:
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    return days[datetime.now().weekday()]


def get_week() -> int:
    return datetime.now().isocalendar()[1]


if __name__ == '__main__':
    print(get_week())

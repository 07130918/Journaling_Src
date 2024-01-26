import calendar
import os
import random
import sys
from datetime import date

from consts import DIR_LOCATION
from review import print_decorated


def main():
    """ランダムな日付のジャーナリングを出力する関数
    """
    amount_of_days_2022 = 365
    amount_of_days_2023 = 365
    amount_of_days_2024 = (date.today() - generate_new_years_day()).days + 1
    count = sys.argv[1] if len(sys.argv) > 1 and int(sys.argv[1]) != 0 else 3

    i = 0
    while True:
        if i == int(count):
            break

        # yearは、年ごとの重みを持つリストからランダムに選択する
        year = random.choice(
            [2022] * amount_of_days_2022 +
            [2023] * amount_of_days_2023 +
            [2024] * amount_of_days_2024)
        month_name = calendar.month_name[random.randint(1, 12)]
        day = random.randint(1, 31)
        file_name = f"{DIR_LOCATION}/{year}/{month_name}/{str(day).zfill(2)}"

        if os.path.isfile(f"{file_name}.txt"):
            print_decorated(f'{month_name} {day} {year}')
            i += 1
            with open(f'{file_name}.txt', 'r') as f:
                print(f.read())


def generate_new_years_day(year=date.today().year):
    return date(year, 1, 1)


if __name__ == '__main__':
    main()

import calendar
import re
import sys
from datetime import datetime, timedelta

from consts import DIR_LOCATION

"""TODAY format is like 2022/June/11"""
NOW = datetime.now()
CURRENT_YEAR = NOW.strftime("%Y")
CURRENT_MONTH_NAME = NOW.strftime("%B")
TODAY = (
    f"{CURRENT_YEAR}/" f"{CURRENT_MONTH_NAME}/" f"{str(NOW.strftime('%d')).zfill(2)}"
)
SPAN_DEFAULT = 7
END_OF_MONTH = {
    "January": 31,
    "February": 28,
    "March": 31,
    "April": 30,
    "May": 31,
    "June": 30,
    "July": 31,
    "August": 31,
    "September": 30,
    "October": 31,
    "November": 30,
    "December": 31,
}


class FormatError(Exception):
    """コマンドライン第1引数のフォーマットエラーを通知するクラス"""

    pass


def main():
    """ジャーナリングのレビューを行う関数"""
    formatted_cli_args = check_args()
    if not formatted_cli_args:
        return

    print_journaling_according_to(*formatted_cli_args)


def check_args():
    """実行する際にコマンドライン引数をチェックし、必要に応じて整形した日付を返却する関数
    Returns:
        正常系:
            tuple:
                int: start_year (2022, 2023 or 2024) 出力を開始する年
                int: start_month (1-12) 出力を開始する月
                int: start_day (1-31) 出力を開始する日
                int: span 出力する日数
        異常系: false
    """
    # コマンドライン第2引数がない場合は7日前の日付を返却する
    if len(sys.argv) == 1:
        return *calculate_7days_ago_from_today(), SPAN_DEFAULT

    # コマンドラインのフォーマットをチェックする
    try:
        first_arg = re.fullmatch(
            r"^(20)?(22|23|24)/(0?[1-9]|1[0-2])/0?[1-9]|[12][0-9]|3[01]$", sys.argv[1]
        )
        if sys.argv[1] and first_arg is None:
            # 第2引数のフォーマットが不正の場合
            raise FormatError

        start_date = first_arg.group().split("/")  # type: ignore
        year_mapping = {"22": "2022", "23": "2023", "24": "2024"}
        start_year = int(year_mapping.get(start_date[0], start_date[0]))
        start_month = int(start_date[1])
        start_day = int(start_date[2])
        if start_day > 31:
            raise FormatError

        # コマンドライン第3引数がない場合は期間を7日間とする
        span = int(sys.argv[2]) if len(sys.argv) > 2 else SPAN_DEFAULT
        return start_year, start_month, start_day, span
    except FormatError:
        print(f"Error: arguments format are invalid -> {sys.argv[1:]}")
        print("Command line args need to be matched with the following format:")
        print("'^(20)?(22|23|24)/(0?[1-9]|1[0-2])/0?[1-9]|[12][0-9]|3[01]$'")
        return False
    except ValueError as e:
        print(e)
        return False


def calculate_7days_ago_from_today():
    """今日から7日前の日付を返却する関数"""
    seven_days_ago = NOW - timedelta(days=7)
    year = int(seven_days_ago.strftime("%Y"))
    month = int(seven_days_ago.strftime("%m"))
    day = int(seven_days_ago.strftime("%d"))
    return year, month, day


def print_journaling_according_to(year, month, day, span):
    """出力するファイル決定するクラス
    Args:
        year: int: 出力を始める年
        month: int: 出力を始める月
        day: int: 出力を始める日
        span: int: 出力する日数
    """
    month_name = str(calendar.month_name[month])
    count = 0
    while True:
        if count == span:
            # 指定した期間を出力したら終了する
            print_terminate(f"{span} days")
            break

        file_name = f"{DIR_LOCATION}/{year}/{month_name}/{str(day).zfill(2)}"
        try:
            with open(f"{file_name}.txt", "r") as f:
                print_decorated(f"{month_name} {day} {year}")
                print(f.read())
                day += 1
                count += 1

            if file_name == f"{DIR_LOCATION}/{TODAY}":
                # ループが当日に達したら終了する
                print_terminate()
                break
        except FileNotFoundError as e:
            if file_name == f"{DIR_LOCATION}/{TODAY}":
                # 当日分が無かったら終了
                print_terminate()
                return

            elif day >= END_OF_MONTH[month_name]:
                # 月の最終日を超える、もしくは月の最終日のファイルがない場合に次の月にする
                month += 1
                if month == 13:
                    # 12月を超える場合には次の年にする
                    year += 1
                    month = 1
                day = 1
                month_name = calendar.month_name[month]

            elif day < END_OF_MONTH[month_name]:
                # 該当の日付ファイルがない場合スキップして次の日に進む
                day += 1

            else:
                print("Error: ", e)
                return


def print_decorated(message):
    horizon_line = " " + "-" * (len(message) + 2)
    print(horizon_line)
    print("| " + message + " |")
    print(horizon_line)


def print_terminate(message="Today"):
    print_decorated(f"Iterations has been reached {message}.")


if __name__ == "__main__":
    main()

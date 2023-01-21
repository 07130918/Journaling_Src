import os
import subprocess
from datetime import datetime

from consts import DIR_LOCATION
from popup_words import main as popup_words


def main():
    year = datetime.now().year
    month = datetime.now().strftime('%B')
    day = datetime.now().strftime('%d')

    if not os.path.isdir(f'{DIR_LOCATION}/{year}'):
        os.system(f'mkdir {DIR_LOCATION}/{year}')
    if not os.path.isdir(f'{DIR_LOCATION}/{year}/{month}'):
        os.system(f'mkdir {DIR_LOCATION}/{year}/{month}')

    # タイマーアプリの準備
    subprocess.call(['/usr/bin/open', '/Applications/AS Timer.app'])
    # ファイルの準備
    todays_file = f'{DIR_LOCATION}/{year}/{month}/{day}.txt'
    os.system(f'touch {todays_file}')
    os.system(f'open {todays_file}')
    # 今日のジャーナリングで使う単語のポップアップを準備
    popup_words()


if __name__ == '__main__':
    main()

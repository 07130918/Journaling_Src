# Journaling書き終わった後にpushまで行う
import os
from datetime import datetime

from consts import DIR_LOCATION


def main():
    os.system(f'git add {DIR_LOCATION}/.')
    os.system(f'git commit -m {datetime.now().strftime("%Y/%m/%d")}')
    os.system('git push')


if __name__ == '__main__':
    main()

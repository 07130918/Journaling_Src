# Journaling書き終わった後にpushまで行う
import os
from datetime import datetime


def main():
    os.system('git add .')
    os.system(f'git commit -m {datetime.now().strftime("%Y/%m/%d")}')
    os.system('git push')


if __name__ == '__main__':
    main()

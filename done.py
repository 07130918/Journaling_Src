import os
from datetime import datetime

from consts import DIR_LOCATION
from proofread import main as proofread


def main():
    """Journalingを書き終わった後にpushまで行う関数
    """
    proofread()
    print("Did u already rewrite the file? [y/n]")
    answer = input()
    if answer != "y":
        print("Please rewrite the file.")
        return

    os.chdir(DIR_LOCATION)
    os.system(f'git add {DIR_LOCATION}/.')
    os.system(f'git commit -m {datetime.now().strftime("%Y/%m/%d")}')
    os.system('git push')
    return

if __name__ == '__main__':
    main()

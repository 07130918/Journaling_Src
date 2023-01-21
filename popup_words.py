import os
import random
import sys
import tkinter as tk
import webbrowser

import requests
from dotenv import load_dotenv

DEFAULT_SAMPLE_SIZE = 5


def main():
    words = get_random_words(int(sys.argv[1])) if len(
        sys.argv) > 1 else get_random_words(DEFAULT_SAMPLE_SIZE)
    generate_popup(words)


def get_random_words(quantity):
    load_dotenv()
    response = requests.get(os.environ['API_URL']).json()
    return random.sample(response, quantity)


def generate_popup(words):
    popup = tk.Tk()
    popup.wm_title("Please use these words")

    for i, word in enumerate(words):
        checkbox = tk.Checkbutton(popup)
        checkbox.grid(row=i, column=0, padx=0)
        label = tk.Label(
            popup,
            anchor="w",
            text=f'{word["English"]}: {word["Japanese"]}',
            font=("Helvetica", 18)
        )
        label.bind("<Button-1>", lambda e: webbrowser.open_new_tab(
            "https://ejje.weblio.jp/content/" + word["English"]
        ))
        label.grid(row=i, column=1, sticky="w", padx=5)
    B1 = tk.Button(popup, text="Done", command=popup.destroy)
    B1.grid(row=len(words), columnspan=2, sticky="ew")

    popup.mainloop()


if __name__ == '__main__':
    main()

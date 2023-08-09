from tkinter import *
from PIL import Image, ImageTk
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


def is_known():
    to_learn.remove(current_card)
    data_to_learn= pandas.DataFrame(to_learn)
    data_to_learn.to_csv("data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flash Card Project")
window.config(background=BACKGROUND_COLOR, padx=50, pady=50)

flip_timer = window.after(3000, func=flip_card)

# images
right_button_image = Image.open("../flash-card-project-start/images/right.png")
right_button_image_ph = ImageTk.PhotoImage(right_button_image)
wrong_button_image = Image.open("../flash-card-project-start/images/wrong.png")
wrong_button_image_ph = ImageTk.PhotoImage(wrong_button_image)

# canvas
canvas = Canvas(width=800, height=526, borderwidth=0, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front = PhotoImage(file="../flash-card-project-start/images/card_front.png")
card_back_img = PhotoImage(file="../flash-card-project-start/images/card_back.png")
card_background = canvas.create_image(402, 263, image=card_front)
canvas.grid(row=0, column=0, columnspan=2, padx=50, pady=50)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))

# Buttons
known_button = Button(image=right_button_image_ph, borderwidth=0, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)
unknown_button = Button(image=wrong_button_image_ph, borderwidth=0, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

next_card()


window.mainloop()

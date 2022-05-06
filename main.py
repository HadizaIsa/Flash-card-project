from tkinter import *
import pandas as pd
import random


BACKGROUND_COLOR = "#B1DDC6"
to_learn = {}
current_card = {}

try:
    data = pd.read_csv("data/french_words.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    print(original_data)
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")
# ---------------------------- GENERATE RANDOM WORDS ------------------------------- #


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(canvas_image, image=image3)
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(canvas_image, image=image4)


def is_known():
    to_learn.remove(current_card)
    print(len(to_learn))
    data = pd.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv")

    next_card()

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

image1 = PhotoImage(file="images/wrong.png")
image2 = PhotoImage(file="images/right.png")
image3 = PhotoImage(file="images/card_front.png")
image4 = PhotoImage(file="images/card_back.png")

canvas = Canvas(width=800, height=526)
canvas_image = canvas.create_image(400, 263, image=image3)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

unknown_button = Button(image=image1, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

known_button = Button(image=image2, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

next_card()


window.mainloop()
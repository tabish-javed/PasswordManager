from tkinter import Tk, Canvas, PhotoImage, Label, Entry, Button, END, messagebox
from random import choice, randint, shuffle
from pyperclip import copy
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Code used from Password Generator Project completed earlier


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                    'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # Creating new lists using list comprehension
    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers

    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showerror(title="Empty Fields", message="Do not leave fields empty")
    else:
        try:
            with open("data.json", mode="r") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open("data.json", mode="w") as file:
                json.dump(new_data, file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", mode="w") as file:
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ------------------------- FIND PASSWORD ---------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("data.json", mode="r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No data file found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            copy(password)  # Added copy method to copy found password to clipboard
            messagebox.showinfo(title="Password Found", message=f"email: {email}\nPassword: {password}")
        else:
            messagebox.showerror(title="Alert", message="No detail for the website exists")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("MyPass")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
password_img = PhotoImage(file="./logo.png")
canvas.create_image(100, 100, image=password_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:").grid(column=0, row=1)

website_entry = Entry(width=21)
website_entry.grid(column=1, row=1, sticky="w")
website_entry.focus()

search_button = Button(text="Search", width=11, command=find_password)
search_button.grid(column=2, row=1)

email_label = Label(text="Email/Username:").grid(column=0, row=2)
email_entry = Entry(width=36)
email_entry.grid(column=1, row=2, columnspan=2, sticky="w")
email_entry.insert(0, "tabish@example.com")

password_label = Label(text="Password:").grid(column=0, row=3)
password_entry = Entry(width=21)
password_entry.grid(column=1, row=3, sticky="w")

password_button = Button(text="Generate Password", width=11, command=generate_password).grid(
    column=2, row=3, columnspan=1, sticky="w")

add_button = Button(text="Add", width=33, command=save).grid(column=1, row=4, columnspan=2)


window.mainloop()

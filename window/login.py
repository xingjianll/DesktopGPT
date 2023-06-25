# Importing required module
import customtkinter as ctk
import data
from getresponse import IfGetResponse


class LoginWindow(ctk.CTk):
    api_entry: ctk.CTkEntry
    com: IfGetResponse
    chat: ctk.CTk
    checkbox: ctk.CTkCheckBox

    def __init__(self, com: IfGetResponse, chat: ctk.CTk):
        self.com = com
        self.chat = chat
        # Selecting GUI theme - dark,
        # light , system (for system default)
        super().__init__()
        ctk.set_appearance_mode("dark")

        # Selecting color theme-blue, green, dark-blue
        ctk.set_default_color_theme("blue")

        self.geometry("300x300")
        self.title("DesktopGPT")

        # Set the label
        label = ctk.CTkLabel(self, text="DesktopGPT")

        label.pack(pady=20)

        # Create a frame
        frame = ctk.CTkFrame(master=self)
        frame.pack(pady=20, padx=40,
                   fill='both', expand=True)

        # Create a text box for taking
        # password input from user
        self.api_entry = ctk.CTkEntry(master=frame,
                                      placeholder_text="API Key",
                                      show="*")
        self.api_entry.pack(pady=12, padx=10)
        self.api_entry.insert('end', data.get_pass())

        # Create a login button to login
        button = ctk.CTkButton(master=frame,
                               text='start', command=self.login)
        button.pack(pady=12, padx=10)

        # Create a remember me checkbox
        self.checkbox = ctk.CTkCheckBox(master=frame,
                                   text='Remember Me')
        self.checkbox.pack(pady=12, padx=10)

        if data.remember_me() is True:
            self.checkbox.select()

    def login(self):

        key = self.api_entry.get()
        self.com.set_apikey(key)
        if self.checkbox.get() == 1:
            data.store_pass(key)
            with open('config.txt', 'w') as f:
                f.write("Y")
        else:
            open('pass.txt', 'w').close()
            with open('config.txt', 'w') as f:
                f.write("N")

        self.withdraw()
        self.chat.deiconify()

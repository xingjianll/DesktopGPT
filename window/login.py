# Importing required module
import customtkinter as ctk

from getresponse import IfGetResponse


class LoginWindow(ctk.CTk):
    api_entry: ctk.CTkEntry
    com: IfGetResponse
    chat: ctk.CTk

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

        # Create a login button to login
        button = ctk.CTkButton(master=frame,
                               text='Login', command=self.login)
        button.pack(pady=12, padx=10)

        # Create a remember me checkbox
        checkbox = ctk.CTkCheckBox(master=frame,
                                   text='Remember Me')
        checkbox.pack(pady=12, padx=10)

    def login(self):
        self.com.set_apikey(self.api_entry.get())
        self.withdraw()
        self.chat.deiconify()


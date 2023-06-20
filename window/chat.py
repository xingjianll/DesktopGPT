# Importing required module
import customtkinter as ctk

from getresponse import IfGetResponse
from ifview import IfView


class ChatWindow(ctk.CTk, IfView):
    com: IfGetResponse
    prompt_entry: ctk.CTkEntry
    textbox: ctk.CTkTextbox

    def display_msg(self, msg: str) -> None:
        self.textbox.configure(state="normal")
        self.textbox.insert("0.0", "chatGPT: " + msg + "\n")
        self.textbox.configure(state="disabled")

    def __init__(self, com: IfGetResponse):
        self.com = com
        super().__init__()
        self.withdraw()
        ctk.set_appearance_mode("dark")

        ctk.set_default_color_theme("blue")

        self.geometry("1080x720")
        self.title("DesktopGPT")

        label = ctk.CTkLabel(self, text="DesktopGPT")
        label.pack(pady=20)

        frame = ctk.CTkFrame(master=self)
        frame.pack(pady=20, padx=40,
                   fill='both', expand=True)

        self.textbox = ctk.CTkTextbox(master=frame, height=500, width=900)
        self.textbox.pack()
        self.textbox.configure(state="disabled")

        self.prompt_entry = ctk.CTkEntry(master=frame,
                                         placeholder_text="enter prompt here",
                                         width=900)
        self.prompt_entry.pack(pady=12, padx=10)

        button = ctk.CTkButton(master=frame,
                               text='send', command=self.send_msg)
        button.pack(pady=12, padx=10)

    def send_msg(self):
        self.textbox.configure(state="normal")
        self.textbox.insert("0.0", "user: " + self.prompt_entry.get() + "\n")
        self.textbox.configure(state="disabled")
        self.com.request_response(self.prompt_entry.get(), "gpt-3.5-turbo")

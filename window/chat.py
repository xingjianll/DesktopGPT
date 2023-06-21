# Importing required module
import time

import customtkinter as ctk

from getresponse import IfGetResponse
from ifview import IfView


class ChatWindow(ctk.CTk, IfView):
    com: IfGetResponse
    prompt_entry: ctk.CTkEntry
    tabview: ctk.CTkTabview
    text_boxes: dict[str, ctk.CTkTextbox]
    curr_prompt: str
    curr_page: str

    def display_msg(self, msg: str) -> None:
        self.text_boxes.get(self.curr_page).configure(state="normal")
        self.text_boxes.get(self.curr_page).insert(ctk.END, ">>>chatGPT: " + msg + "\n\n")
        self.text_boxes.get(self.curr_page).configure(state="disabled")

    def __init__(self, com: IfGetResponse):
        self.text_boxes = {}
        self.com = com
        super().__init__()
        self.withdraw()
        ctk.set_appearance_mode("dark")

        ctk.set_default_color_theme("blue")

        self.geometry("1080x720")
        self.minsize(935, 720)
        self.title("DesktopGPT")

        frame = ctk.CTkFrame(master=self)
        frame.pack(pady=0, padx=0,
                   fill='y', expand=True)

        self.tabview = ctk.CTkTabview(master=frame)
        self.tabview.grid(row=0, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")
        self.add_chat()

        self.prompt_entry = ctk.CTkEntry(master=frame,
                                         placeholder_text="enter prompt here",
                                         width=900)
        self.prompt_entry.grid(row=1, column=0, columnspan=3,  pady=10, padx=10, sticky="nsew")

        send_button = ctk.CTkButton(master=frame,
                               text='send', command=self.send_msg)
        send_button.grid(row=2, column=0, pady=10, padx=10)

        new_button = ctk.CTkButton(master=frame,
                                    text='new chat', command=self.add_chat)
        new_button.grid(row=2, column=1, pady=10, padx=10)

        del_button = ctk.CTkButton(master=frame,
                                    text='delete chat', command=self.del_chat)
        del_button.grid(row=2, column=2, pady=10, padx=10)

    def send_msg(self) -> None:
        self.prompt_entry.after(1, self._send_msg_helper())
        self.com.request_response(self.curr_prompt, "gpt-3.5-turbo", self.tabview.get())

    def _send_msg_helper(self) -> None:
        self.curr_prompt = self.prompt_entry.get()
        self.curr_page = self.tabview.get()
        self.text_boxes.get(self.curr_page).configure(state="normal")
        self.text_boxes.get(self.curr_page).insert(ctk.END, ">>> user: " + self.curr_prompt + "\n\n")
        self.text_boxes.get(self.curr_page).configure(state="disabled")
        self.prompt_entry.delete(0, ctk.END)

    def add_chat(self) -> None:
        if len(self.text_boxes) == 0:
            self._add_chat_helper("tab 1")

        else:
            dialog = ctk.CTkInputDialog(text="Enter name for new conversation:", title="Hi")
            a = dialog.get_input()
            if a in self.text_boxes or a == "":
                pass
            else:
                self._add_chat_helper(a)

    def _add_chat_helper(self, name: str):
        self.tabview.add(name)
        self.tabview.set(name)

        textbox = ctk.CTkTextbox(master=self.tabview.tab(name), width=900, height=550, pady=0, padx=0)
        textbox.pack()
        textbox.configure(state="disabled")
        self.text_boxes[name] = textbox

    def del_chat(self) -> None:
        if len(self.text_boxes) != 1:
            self.text_boxes.__delitem__(self.tabview.get())
            self.tabview.delete(self.tabview.get())

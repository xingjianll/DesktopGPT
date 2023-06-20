# Importing required module
import time

import customtkinter as ctk

from getresponse import IfGetResponse
from ifview import IfView


class ChatWindow(ctk.CTk, IfView):
    com: IfGetResponse
    prompt_entry: ctk.CTkEntry
    tabview: ctk.CTkTabview
    text_boxes: list[ctk.CTkTextbox]
    tabs: list[ctk.CTkFrame]
    curr_prompt: str
    curr_page: int

    def display_msg(self, msg: str) -> None:
        self.text_boxes[self.curr_page].configure(state="normal")
        self.text_boxes[self.curr_page].insert(ctk.END, ">>>chatGPT: " + msg + "\n\n")
        self.text_boxes[self.curr_page].configure(state="disabled")

    def __init__(self, com: IfGetResponse):
        self.text_boxes = []
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
        self.com.request_response(self.curr_prompt, "gpt-3.5-turbo")

    def _send_msg_helper(self) -> None:
        self.curr_prompt = self.prompt_entry.get()
        self.curr_page = int(self.tabview.get())
        self.text_boxes[self.curr_page].configure(state="normal")
        self.text_boxes[self.curr_page].insert(ctk.END, ">>> user: " + self.curr_prompt + "\n\n")
        self.text_boxes[self.curr_page].configure(state="disabled")
        self.prompt_entry.delete(0, ctk.END)

    def add_chat(self) -> None:
        tab_name = str(len(self.text_boxes))
        self.tabview.add(tab_name)
        self.tabview.set(tab_name)

        textbox = ctk.CTkTextbox(master=self.tabview.tab(tab_name), width=900, height=500, pady=0, padx=0)
        textbox.pack()
        textbox.configure(state="disabled")
        self.text_boxes.append(textbox)

    def del_chat(self) -> None:
        curr = int(self.tabview.get())
        if curr != 0:
            del self.text_boxes[curr]
            self.tabview.delete(self.tabview.get())

# Importing required module

import customtkinter as ctk

from getresponse import IfGetResponse
from ifview import IfView
import data


class ChatWindow(ctk.CTk, IfView):
    com: IfGetResponse
    prompt_entry: ctk.CTkEntry
    tabview: ctk.CTkTabview
    text_boxes: dict[str, ctk.CTkTextbox]
    curr_prompt: str
    curr_page: str
    GPT_mode: str
    temperature: float

    def display_msg(self, msg: str) -> None:
        self.text_boxes.get(self.curr_page).configure(state="normal")
        self.text_boxes.get(self.curr_page).insert(ctk.END, ">>> chatGPT: " + msg + "\n\n")
        self.text_boxes.get(self.curr_page).configure(state="disabled")

    def __init__(self, com: IfGetResponse):
        self.GPT_mode = "gpt-3.5-turbo"
        self.temperature = 0
        self.text_boxes = {}
        self.com = com
        super().__init__()
        self.withdraw()
        ctk.set_appearance_mode("dark")

        ctk.set_default_color_theme("blue")

        self.geometry("1080x720")
        self.minsize(680, 500)
        self.title("DesktopGPT")

        frame = ctk.CTkFrame(master=self)
        frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
        frame.grid_rowconfigure(index=0, weight=1)
        frame.grid_columnconfigure(index=0, weight=1)

        self.tabview = ctk.CTkTabview(master=frame)
        self.tabview.grid(row=0, column=0, columnspan=3, pady=10, padx=10, sticky="news")
        a = data.get_conversations()
        if a is None or len(a.keys()) == 0:
            self.add_chat()
        else:
            for key in a.keys():
                self._add_chat_helper(key, a[key])

        self.prompt_entry = ctk.CTkEntry(master=frame,
                                         placeholder_text="enter prompt here",
                                         width=350)
        self.prompt_entry.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10)

        send_button = ctk.CTkButton(master=frame,
                               text='send', command=self.send_msg)
        send_button.grid(row=2, column=0, pady=10, padx=10, sticky='EW')

        new_button = ctk.CTkButton(master=frame,
                                    text='new chat', command=self.add_chat)
        new_button.grid(row=2, column=1, pady=10, padx=10)

        del_button = ctk.CTkButton(master=frame,
                                    text='delete chat', command=self.del_chat)
        del_button.grid(row=2, column=2, pady=10, padx=10)

        frame2 = ctk.CTkFrame(master=self)
        frame2.pack(side=ctk.RIGHT, fill=ctk.Y, padx=10)

        logo_label = ctk.CTkLabel(frame2, text="DesktopGPT", font=ctk.CTkFont(size=20, weight="bold"))
        logo_label.grid(row=0, column=0, padx=20, pady=(40, 20))

        save_button = ctk.CTkButton(master=frame2,
                                    text='save', command=self.save)
        save_button.grid(row=1, column=0, pady=20, padx=10)

        switch_var = ctk.StringVar(value="off")
        switch = ctk.CTkSwitch(master=frame2, text="GPT4 mode?",
                               command=self.switch_event,
                               variable=switch_var,
                               onvalue="on", offvalue="off")
        switch.grid(row=2, column=0, pady=20, padx=10)

        scaling_label = ctk.CTkLabel(frame2, text="Temperature:", anchor="w")
        scaling_label.grid(row=4, column=0, padx=20, pady=(20, 0))

        slider = ctk.CTkSlider(master=frame2,
                               from_=0, to=100, command=self.slider_event)
        slider.grid(row=5, column=0, pady=(20, 40), padx=10)

    def slider_event(self, value):
        self.temperature = value

    def switch_event(self):
        if self.GPT_mode != "gpt-4":
            self.GPT_mode = "gpt-4"
        else:
            self.GPT_mode = "gpt-3.5-turbo"

    def save(self):
        data.store_conversations(self.com.get_conversations())

    def send_msg(self) -> None:
        self.prompt_entry.after(1, self._send_msg_helper())
        self.com.request_response(self.curr_prompt, "gpt-3.5-turbo", self.tabview.get(), self.temperature)

    def _send_msg_helper(self) -> None:
        self.curr_prompt = self.prompt_entry.get()
        self.curr_page = self.tabview.get()
        self.text_boxes.get(self.curr_page).configure(state="normal")
        self.text_boxes.get(self.curr_page).insert(ctk.END, ">>> user: " + self.curr_prompt + "\n\n")
        self.text_boxes.get(self.curr_page).configure(state="disabled")
        self.prompt_entry.delete(0, ctk.END)

    def add_chat(self) -> None:
        if len(self.text_boxes) == 0:
            self._add_chat_helper("tab 1", [])

        else:
            dialog = ctk.CTkInputDialog(text="Enter name for new conversation:", title="Hi")
            a = dialog.get_input()
            if a in self.text_boxes or a == "":
                pass
            else:
                self._add_chat_helper(a, [])

    def _add_chat_helper(self, name: str, conversation: list):
        self.tabview.add(name)
        self.tabview.set(name)

        textbox = ctk.CTkTextbox(master=self.tabview.tab(name), width=400, height=300, pady=0, padx=0)
        textbox.pack(fill=ctk.BOTH, expand=True)
        textbox.configure(state="normal")
        for item in conversation:
            if item["role"] == "user":
                textbox.insert(ctk.END, ">>> user: " + item["content"] + "\n\n")
            else:
                textbox.insert(ctk.END, ">>> chatGPT: " + item["content"] + "\n\n")
        textbox.configure(state="disabled")
        self.text_boxes[name] = textbox

    def del_chat(self) -> None:
        self.text_boxes.__delitem__(self.tabview.get())
        self.tabview.delete(self.tabview.get())


class PopUp(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = ctk.CTkLabel(self, text="Would you like to save before quit?")
        self.label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        yes_button = ctk.CTkButton(master=self,
                                   text='yes', command=self.yes)
        yes_button.grid(row=1, column=0, pady=10, padx=10)

        no_button = ctk.CTkButton(master=self,
                                   text='yes', command=self.no)
        no_button.grid(row=1, column=0, pady=10, padx=10)

    def yes(self):
        pass

    def no(self):
        pass

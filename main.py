import os
import openai

import window.login as lg
import window.chat as chat
from getresponse import ResponseGetter

if __name__ == "__main__":
    com = ResponseGetter()
    chat = chat.ChatWindow(com)
    login = lg.LoginWindow(com, chat)
    com.initialize(chat)

    login.mainloop()

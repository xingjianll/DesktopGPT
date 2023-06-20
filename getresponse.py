import openai

from window.ifgetresponse import IfGetResponse
from window.chat import IfView


class ResponseGetter(IfGetResponse):
    org_id: str
    api_key: str
    view: IfView
    messages: list

    def initialize(self, view: IfView):
        self.view = view
        self.messages = []

    def request_response(self, prompt: str, model: str) -> None:
        openai.api_key = self.api_key
        self.messages.append({"role": "user", "content": prompt})
        completion = openai.ChatCompletion.create(
            model=model,
            messages=self.messages
        )

        self.messages.append({"role": "assistant",
                              "content": completion.choices[0].message.content})
        self.view.display_msg(completion.choices[0].message.content)

    def set_organization_id(self, org_id: str) -> None:
        self.org_id = org_id

    def set_apikey(self, api_key: str) -> None:
        self.api_key = api_key

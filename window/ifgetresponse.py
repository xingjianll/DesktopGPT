from abc import ABC, abstractmethod


class IfGetResponse(ABC):

    @abstractmethod
    def request_response(self, prompt: str, model: str, conversation_name: str) -> None:
        pass

    @abstractmethod
    def set_organization_id(self, org_id: str) -> None:
        pass

    @abstractmethod
    def set_apikey(self, api_key: str) -> None:
        pass

    @abstractmethod
    def delete_conversation(self, conversation_name: str) -> None:
        pass

from abc import ABC, abstractmethod
from typing import Type


class Request:
    MESSAGE_SIZE_SIZE = 4

    def __init__(self, request: bytes, header: Type[RequestHeader]):
        self.message_size = request[: self.MESSAGE_SIZE_SIZE]

        self.header = header(request, self.MESSAGE_SIZE_SIZE)

    def get_correlation_id(self) -> bytes:
        return self.header.get_correlation_id()

    def get_api_version(self) -> bytes:
        return self.header.get_api_version()


class RequestHeader(ABC):
    @classmethod
    @abstractmethod
    def size(cls) -> int: ...

    @abstractmethod
    def __init__(self, request: bytes, start: int): ...

    @abstractmethod
    def get_correlation_id(self) -> bytes: ...

    @abstractmethod
    def get_api_version(self) -> bytes: ...


class RequestHeaderV2(RequestHeader):
    API_KEY_SIZE = 2
    API_VERSION_SIZE = 2
    CORRELATION_ID_SIZE = 4

    @classmethod
    def size(cls) -> int:
        return cls.API_KEY_SIZE + cls.API_VERSION_SIZE + cls.CORRELATION_ID_SIZE

    def __init__(self, request: bytes, start: int):
        end = start + self.API_KEY_SIZE
        self.api_key = request[start:end]

        start = end
        end += self.API_VERSION_SIZE
        self.api_version = request[start:end]

        start = end
        end += self.CORRELATION_ID_SIZE
        self.correlation_id = request[start:end]

    def get_correlation_id(self) -> bytes:
        return self.correlation_id

    def get_api_version(self) -> bytes:
        return self.api_version

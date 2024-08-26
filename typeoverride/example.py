import typing
from typeoverride.decorator import schema_override


class Client:
    def __init__(self, data: dict[str, typing.Any]) -> None:
        self.data = data

    @schema_override
    def method(self) -> dict[str, typing.Any]:
        """
        my awesome docstring
        """
        return self.data


client = Client({"value": 1})


class Schema(typing.TypedDict):
    value: int


typing.reveal_type(client.method)
typing.reveal_type(client.method())

typing.reveal_type(client.method[Schema])
typing.reveal_type(client.method[Schema]())

typing.reveal_type(Client.method)
typing.reveal_type(Client.method(client))

typing.reveal_type(Client.method[Schema])
typing.reveal_type(Client.method[Schema](client))

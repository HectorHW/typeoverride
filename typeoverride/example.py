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


client = Client(dict(value=1))


class Schema(typing.TypedDict):
    value: int


plain_value = client.method()
typed_value = client.method[Schema]()

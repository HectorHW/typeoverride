import typing
from typeoverride.method_decorator import schema_override
from typeoverride.decorator import f_schema_override


class Schema(typing.TypedDict):
    value: int


@f_schema_override
def func(arg: dict[str, typing.Any]) -> dict[str, typing.Any]:
    return arg


typing.reveal_type(func)
typing.reveal_type(func({"value": 1}))
typing.reveal_type(func[Schema])
typing.reveal_type(func[Schema]({"value": 1}))


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


typing.reveal_type(client.method)
typing.reveal_type(client.method())

typing.reveal_type(client.method[Schema])
typing.reveal_type(client.method[Schema]())

typing.reveal_type(Client.method)
typing.reveal_type(Client.method(client))

typing.reveal_type(Client.method[Schema])
typing.reveal_type(Client.method[Schema](client))

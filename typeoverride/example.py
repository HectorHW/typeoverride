import typing
from typeoverride.method_decorator import schema_override
from typeoverride.decorator import f_schema_override
from typeoverride.result import Result


class Schema(typing.TypedDict):
    value: int


@f_schema_override
def func(arg: dict[str, typing.Any]) -> Result[dict[str, typing.Any]]:
    return {"success": True, "value": arg}


typing.reveal_type(func)
typing.reveal_type(func({"value": 1}))
typing.reveal_type(func[Schema])
typing.reveal_type(func[Schema]({"value": 1}))


class Client:
    def __init__(self, data: dict[str, typing.Any]) -> None:
        self.data = data

    @schema_override
    def method(self) -> Result[dict[str, typing.Any]]:
        """
        my awesome docstring
        """
        return {"success": True, "value": self.data}


client = Client({"sucess": True, "value": 1})


typing.reveal_type(client.method)
typing.reveal_type(client.method())

typing.reveal_type(client.method[int])
typing.reveal_type(client.method[int]())

typing.reveal_type(Client.method)
typing.reveal_type(Client.method(client))

typing.reveal_type(Client.method[int])
typing.reveal_type(Client.method[int](client))

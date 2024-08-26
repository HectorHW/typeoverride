import typing

SchemaT = typing.TypeVar("SchemaT")


class SuccessfulResponse(typing.TypedDict, typing.Generic[SchemaT]):
    success: typing.Literal[True]
    value: SchemaT


class ErrorResponse(typing.TypedDict):
    success: typing.Literal[False]
    verbose: str


Result = SuccessfulResponse[SchemaT] | ErrorResponse

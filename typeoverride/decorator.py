import typing
import functools

Params = typing.ParamSpec("Params")
OriginalReturnT = typing.TypeVar("OriginalReturnT")
NewReturnT = typing.TypeVar("NewReturnT")


class TypedFunction(typing.Generic[Params, OriginalReturnT, NewReturnT]):
    def __init__(self, inner: typing.Callable[Params, OriginalReturnT]):
        self.__inner = inner
        functools.update_wrapper(self, inner)

    def __call__(self, *args: Params.args, **kwargs: Params.kwargs) -> NewReturnT:
        return typing.cast(NewReturnT, self.__inner(*args, **kwargs))


class UntypedFunction(typing.Generic[Params, OriginalReturnT]):
    def __init__(self, inner: typing.Callable[Params, OriginalReturnT]):
        self.__inner = inner
        functools.update_wrapper(self, inner)

    def __call__(self, *args: Params.args, **kwargs: Params.kwargs) -> OriginalReturnT:
        return self.__inner(*args, **kwargs)

    def __getitem__(
        self, typ: type[NewReturnT]
    ) -> TypedFunction[Params, OriginalReturnT, NewReturnT]:
        return TypedFunction(self.__inner)


def f_schema_override(
    inner: typing.Callable[Params, OriginalReturnT],
) -> UntypedFunction[Params, OriginalReturnT]:
    return UntypedFunction(inner)

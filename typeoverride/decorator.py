import typing
import functools

ReturnT = typing.TypeVar("ReturnT")
Params = typing.ParamSpec("Params")
SelfT = typing.TypeVar("SelfT")


class TypedMethodBound(typing.Generic[SelfT, Params, ReturnT]):
    def __init__(
        self,
        instance,
        inner: typing.Callable[typing.Concatenate[SelfT, Params], typing.Any],
    ):
        self.__instance = instance
        self.__inner = inner
        functools.update_wrapper(self, inner)

    def __call__(self, *args: Params.args, **kwargs: Params.kwargs) -> ReturnT:
        return typing.cast(ReturnT, self.__inner(self.__instance, *args, **kwargs))


class UntypedMethodBound(typing.Generic[SelfT, Params]):
    def __init__(
        self,
        instance: typing.Any,
        inner: typing.Callable[typing.Concatenate[SelfT, Params], typing.Any],
    ):
        self.__instance = instance
        self.__inner = inner
        functools.update_wrapper(self, inner)

    def __call__(self, *args: Params.args, **kwargs: Params.kwargs) -> typing.Any:
        return self.__inner(self.__instance, *args, **kwargs)

    def __getitem__(
        self, typ: type[ReturnT]
    ) -> TypedMethodBound[SelfT, Params, ReturnT]:
        return TypedMethodBound(self.__instance, self.__inner)


class UntypedMethod(typing.Generic[SelfT, Params]):
    def __init__(
        self, inner: typing.Callable[typing.Concatenate[SelfT, Params], typing.Any]
    ):
        self.__inner = inner

    @typing.overload
    def __get__(
        self, instance: SelfT, owner: type[SelfT]
    ) -> UntypedMethodBound[SelfT, Params]: ...

    @typing.overload
    def __get__(self, instance: None, owner: type[SelfT]) -> typing.Self: ...

    def __get__(
        self, instance: SelfT | None, owner: type[SelfT]
    ) -> UntypedMethodBound[SelfT, Params] | typing.Self:
        if instance is not None:
            return UntypedMethodBound(instance, self.__inner)
        return self


def schema_override(
    callable: typing.Callable[typing.Concatenate[SelfT, Params], typing.Any],
) -> UntypedMethod[SelfT, Params]:
    wrapper = UntypedMethod(callable)
    return wrapper

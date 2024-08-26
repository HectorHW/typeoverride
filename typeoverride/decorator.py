import typing
import functools

SelfT = typing.TypeVar("SelfT")
Params = typing.ParamSpec("Params")
OriginalReturnT = typing.TypeVar("OriginalReturnT")
NewReturnT = typing.TypeVar("NewReturnT")


class TypedMethodBound(typing.Generic[SelfT, Params, OriginalReturnT, NewReturnT]):
    def __init__(
        self,
        instance,
        inner: typing.Callable[typing.Concatenate[SelfT, Params], OriginalReturnT],
    ):
        self.__instance = instance
        self.__inner = inner
        functools.update_wrapper(self, inner)

    def __call__(self, *args: Params.args, **kwargs: Params.kwargs) -> NewReturnT:
        return typing.cast(NewReturnT, self.__inner(self.__instance, *args, **kwargs))


class TypedMethod(typing.Generic[SelfT, Params, OriginalReturnT, NewReturnT]):
    def __init__(
        self, inner: typing.Callable[typing.Concatenate[SelfT, Params], OriginalReturnT]
    ):
        self.__inner = inner
        functools.update_wrapper(self, inner)

    def __call__(
        self, self_v: SelfT, *args: Params.args, **kwargs: Params.kwargs
    ) -> NewReturnT:
        return typing.cast(NewReturnT, self.__inner(self_v, *args, **kwargs))


class UntypedMethodBound(typing.Generic[SelfT, Params, OriginalReturnT]):
    def __init__(
        self,
        instance: typing.Any,
        inner: typing.Callable[typing.Concatenate[SelfT, Params], OriginalReturnT],
    ):
        self.__instance = instance
        self.__inner = inner
        functools.update_wrapper(self, inner)

    def __call__(self, *args: Params.args, **kwargs: Params.kwargs) -> OriginalReturnT:
        return self.__inner(self.__instance, *args, **kwargs)

    def __getitem__(
        self, typ: type[NewReturnT]
    ) -> TypedMethodBound[SelfT, Params, OriginalReturnT, NewReturnT]:
        return TypedMethodBound(self.__instance, self.__inner)


class UntypedMethod(typing.Generic[SelfT, Params, OriginalReturnT]):
    def __init__(
        self, inner: typing.Callable[typing.Concatenate[SelfT, Params], OriginalReturnT]
    ):
        self.__inner = inner

    @typing.overload
    def __get__(
        self, instance: SelfT, owner: type[SelfT]
    ) -> UntypedMethodBound[SelfT, Params, OriginalReturnT]: ...

    @typing.overload
    def __get__(self, instance: None, owner: type[SelfT]) -> typing.Self: ...

    def __get__(
        self, instance: SelfT | None, owner: type[SelfT]
    ) -> UntypedMethodBound[SelfT, Params, OriginalReturnT] | typing.Self:
        if instance is not None:
            return UntypedMethodBound(instance, self.__inner)
        return self

    def __getitem__(
        self, typ: type[NewReturnT]
    ) -> TypedMethod[SelfT, Params, OriginalReturnT, NewReturnT]:
        return TypedMethod(self.__inner)

    def __call__(
        self, self_v: SelfT, *args: Params.args, **kwargs: Params.kwargs
    ) -> OriginalReturnT:
        return self.__inner(self_v, *args, **kwargs)


def schema_override(
    callable: typing.Callable[typing.Concatenate[SelfT, Params], OriginalReturnT],
) -> UntypedMethod[SelfT, Params, OriginalReturnT]:
    wrapper = UntypedMethod(callable)
    return wrapper

from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Message(_message.Message):
    __slots__ = ("msg_type", "sender", "term", "log_length", "last_log_term", "prev_log_index", "prev_log_term", "entries", "leader_commit", "key", "value")
    class MessageType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SetRequest: _ClassVar[Message.MessageType]
        GetRequest: _ClassVar[Message.MessageType]
        VoteRequest: _ClassVar[Message.MessageType]
        VoteResponse: _ClassVar[Message.MessageType]
        LogRequest: _ClassVar[Message.MessageType]
        LogResponse: _ClassVar[Message.MessageType]
        AppendEntries: _ClassVar[Message.MessageType]
        ForwardMsg: _ClassVar[Message.MessageType]
    SetRequest: Message.MessageType
    GetRequest: Message.MessageType
    VoteRequest: Message.MessageType
    VoteResponse: Message.MessageType
    LogRequest: Message.MessageType
    LogResponse: Message.MessageType
    AppendEntries: Message.MessageType
    ForwardMsg: Message.MessageType
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    TERM_FIELD_NUMBER: _ClassVar[int]
    LOG_LENGTH_FIELD_NUMBER: _ClassVar[int]
    LAST_LOG_TERM_FIELD_NUMBER: _ClassVar[int]
    PREV_LOG_INDEX_FIELD_NUMBER: _ClassVar[int]
    PREV_LOG_TERM_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    LEADER_COMMIT_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    msg_type: Message.MessageType
    sender: str
    term: int
    log_length: int
    last_log_term: int
    prev_log_index: int
    prev_log_term: int
    entries: _containers.RepeatedCompositeFieldContainer[LogEntry]
    leader_commit: int
    key: str
    value: str
    def __init__(self, msg_type: _Optional[_Union[Message.MessageType, str]] = ..., sender: _Optional[str] = ..., term: _Optional[int] = ..., log_length: _Optional[int] = ..., last_log_term: _Optional[int] = ..., prev_log_index: _Optional[int] = ..., prev_log_term: _Optional[int] = ..., entries: _Optional[_Iterable[_Union[LogEntry, _Mapping]]] = ..., leader_commit: _Optional[int] = ..., key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class LogEntry(_message.Message):
    __slots__ = ("term", "msg")
    TERM_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    term: int
    msg: str
    def __init__(self, term: _Optional[int] = ..., msg: _Optional[str] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

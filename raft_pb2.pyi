from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LogEntry(_message.Message):
    __slots__ = ("term", "msg")
    TERM_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    term: int
    msg: str
    def __init__(self, term: _Optional[int] = ..., msg: _Optional[str] = ...) -> None: ...

class Log(_message.Message):
    __slots__ = ("entries",)
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[LogEntry]
    def __init__(self, entries: _Optional[_Iterable[_Union[LogEntry, _Mapping]]] = ...) -> None: ...

class RequestVoteRequest(_message.Message):
    __slots__ = ("term", "candidate_id", "last_log_index", "last_log_term")
    TERM_FIELD_NUMBER: _ClassVar[int]
    CANDIDATE_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_LOG_INDEX_FIELD_NUMBER: _ClassVar[int]
    LAST_LOG_TERM_FIELD_NUMBER: _ClassVar[int]
    term: int
    candidate_id: str
    last_log_index: int
    last_log_term: int
    def __init__(self, term: _Optional[int] = ..., candidate_id: _Optional[str] = ..., last_log_index: _Optional[int] = ..., last_log_term: _Optional[int] = ...) -> None: ...

class RequestVoteResponse(_message.Message):
    __slots__ = ("term", "vote_granted")
    TERM_FIELD_NUMBER: _ClassVar[int]
    VOTE_GRANTED_FIELD_NUMBER: _ClassVar[int]
    term: int
    vote_granted: bool
    def __init__(self, term: _Optional[int] = ..., vote_granted: bool = ...) -> None: ...

class AppendEntriesRequest(_message.Message):
    __slots__ = ("term", "leader_id", "prev_log_index", "prev_log_term", "entries", "leader_commit")
    TERM_FIELD_NUMBER: _ClassVar[int]
    LEADER_ID_FIELD_NUMBER: _ClassVar[int]
    PREV_LOG_INDEX_FIELD_NUMBER: _ClassVar[int]
    PREV_LOG_TERM_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    LEADER_COMMIT_FIELD_NUMBER: _ClassVar[int]
    term: int
    leader_id: str
    prev_log_index: int
    prev_log_term: int
    entries: _containers.RepeatedCompositeFieldContainer[LogEntry]
    leader_commit: int
    def __init__(self, term: _Optional[int] = ..., leader_id: _Optional[str] = ..., prev_log_index: _Optional[int] = ..., prev_log_term: _Optional[int] = ..., entries: _Optional[_Iterable[_Union[LogEntry, _Mapping]]] = ..., leader_commit: _Optional[int] = ...) -> None: ...

class AppendEntriesResponse(_message.Message):
    __slots__ = ("term", "success")
    TERM_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    term: int
    success: bool
    def __init__(self, term: _Optional[int] = ..., success: bool = ...) -> None: ...

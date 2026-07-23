"""Internal event model shared by every provider adapter and policy module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

FILE_READ = "file_read"
SHELL_COMMAND = "shell_command"
SEARCH_COMMAND = "search_command"
SESSION_LIFECYCLE = "session_lifecycle"
OTHER = "other"

# Tool names (as reported by either provider) that indicate a file-read operation.
_FILE_READ_TOOLS = {"Read", "read_file", "read"}

# Search tool/binary names that indicate a search operation rather than a plain
# shell command; used when classifying a shell_command event's command string.
_SEARCH_BINARIES = {"grep", "rg", "ripgrep", "find", "ag", "ack"}

_LIFECYCLE_EVENTS = {
    "SessionStart",
    "PreCompact",
    "PostCompact",
    "Stop",
}


@dataclass
class Event:
    """Common internal representation of a single provider hook invocation."""

    provider: str
    event_name: str
    operation_kind: str
    path: str | None = None
    command: str | None = None
    session_id: str = ""
    cwd: str = ""
    raw: dict[str, Any] = field(default_factory=dict)


def classify_operation(event_name: str, tool_name: str | None, command: str | None) -> str:
    """Return the shared operation_kind for a parsed provider payload.

    Adapters call this so no policy module ever needs to know a provider's
    tool-name spelling.
    """
    if event_name in _LIFECYCLE_EVENTS:
        return SESSION_LIFECYCLE
    if tool_name in _FILE_READ_TOOLS:
        return FILE_READ
    if command:
        first_token = command.strip().split()[0] if command.strip() else ""
        first_token = first_token.rsplit("/", 1)[-1]
        if first_token in _SEARCH_BINARIES:
            return SEARCH_COMMAND
        return SHELL_COMMAND
    return OTHER

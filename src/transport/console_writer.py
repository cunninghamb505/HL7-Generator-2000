"""Console writer - prints HL7 messages to stdout."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel

console = Console()


class ConsoleWriter:
    def __init__(self, colorize: bool = True):
        self.colorize = colorize
        self._count = 0

    async def send(self, message: str) -> bool:
        self._count += 1
        # Extract message type from MSH.9
        msg_type = "HL7"
        lines = message.split("\r")
        if lines:
            fields = lines[0].split("|")
            if len(fields) > 8:
                msg_type = fields[8]

        if self.colorize:
            formatted = message.replace("\r", "\n")
            console.print(Panel(
                formatted,
                title=f"[bold cyan]#{self._count} {msg_type}[/]",
                border_style="dim",
                expand=False,
            ))
        else:
            print(f"--- Message #{self._count} ({msg_type}) ---")
            print(message.replace("\r", "\n"))
            print("---")

        return True

    @property
    def message_count(self) -> int:
        return self._count

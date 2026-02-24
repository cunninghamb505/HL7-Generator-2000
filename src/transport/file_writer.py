"""File writer - writes HL7 messages to .hl7 files."""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

import structlog

logger = structlog.get_logger(__name__)


class FileWriter:
    def __init__(
        self,
        output_dir: str = "output",
        single_file: bool = False,
        filename_prefix: str = "hl7",
        max_file_size: int = 10 * 1024 * 1024,  # 10MB
    ):
        self.output_dir = Path(output_dir)
        self.single_file = single_file
        self.filename_prefix = filename_prefix
        self.max_file_size = max_file_size
        self._count = 0
        self._current_file: str | None = None
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def send(self, message: str) -> bool:
        self._count += 1

        try:
            if self.single_file:
                filepath = self.output_dir / f"{self.filename_prefix}_messages.hl7"
                # Rotate if too large
                if filepath.exists() and filepath.stat().st_size > self.max_file_size:
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    rotated = self.output_dir / f"{self.filename_prefix}_messages_{ts}.hl7"
                    filepath.rename(rotated)

                with open(filepath, "a", encoding="utf-8") as f:
                    f.write(message)
                    f.write("\n\n")
            else:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                # Extract message type
                msg_type = "MSG"
                lines = message.split("\r")
                if lines:
                    fields = lines[0].split("|")
                    if len(fields) > 8:
                        msg_type = fields[8].replace("^", "_")
                filepath = self.output_dir / f"{self.filename_prefix}_{msg_type}_{ts}.hl7"
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(message)

            return True
        except OSError as e:
            logger.error("file_write_failed", error=str(e))
            return False

    @property
    def message_count(self) -> int:
        return self._count

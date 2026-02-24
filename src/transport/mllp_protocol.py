"""MLLP (Minimal Lower Layer Protocol) framing.

MLLP wraps HL7 messages:  SB + message + EB + CR
  SB = Start Block = 0x0B (vertical tab)
  EB = End Block   = 0x1C (file separator)
  CR = Carriage Return = 0x0D
"""

from __future__ import annotations

SB = b"\x0b"  # Start Block
EB = b"\x1c"  # End Block
CR = b"\x0d"  # Carriage Return


def wrap_mllp(message: str) -> bytes:
    """Wrap an HL7 message in MLLP framing."""
    return SB + message.encode("utf-8") + EB + CR


def unwrap_mllp(data: bytes) -> str:
    """Strip MLLP framing from received data."""
    # Remove SB prefix
    if data.startswith(SB):
        data = data[1:]
    # Remove EB+CR suffix
    if data.endswith(EB + CR):
        data = data[:-2]
    elif data.endswith(EB):
        data = data[:-1]
    return data.decode("utf-8", errors="replace")


def extract_messages(buffer: bytes) -> tuple[list[str], bytes]:
    """Extract complete MLLP messages from a byte buffer.

    Returns (list_of_messages, remaining_buffer).
    """
    messages: list[str] = []
    while True:
        start = buffer.find(SB)
        if start == -1:
            break
        end = buffer.find(EB, start)
        if end == -1:
            break
        msg_bytes = buffer[start + 1:end]
        messages.append(msg_bytes.decode("utf-8", errors="replace"))
        # Skip past EB and optional CR
        pos = end + 1
        if pos < len(buffer) and buffer[pos:pos + 1] == CR:
            pos += 1
        buffer = buffer[pos:]
    return messages, buffer

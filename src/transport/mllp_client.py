"""Async MLLP client for sending HL7 messages."""

from __future__ import annotations

import asyncio

import structlog

from src.transport.mllp_protocol import extract_messages, wrap_mllp

logger = structlog.get_logger(__name__)


class MLLPClient:
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 2575,
        timeout: float = 10.0,
        name: str = "mllp",
    ):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.name = name
        self._reader: asyncio.StreamReader | None = None
        self._writer: asyncio.StreamWriter | None = None
        self._connected = False

    async def connect(self) -> bool:
        try:
            self._reader, self._writer = await asyncio.wait_for(
                asyncio.open_connection(self.host, self.port),
                timeout=self.timeout,
            )
            self._connected = True
            logger.info("mllp_connected", host=self.host, port=self.port, name=self.name)
            return True
        except (OSError, asyncio.TimeoutError) as e:
            logger.warning("mllp_connect_failed", host=self.host, port=self.port, error=str(e))
            self._connected = False
            return False

    async def send(self, message: str) -> str | None:
        """Send an HL7 message and wait for ACK. Returns ACK message or None."""
        if not self._connected:
            if not await self.connect():
                return None

        try:
            data = wrap_mllp(message)
            self._writer.write(data)
            await self._writer.drain()

            # Read ACK response
            response = await asyncio.wait_for(
                self._reader.read(65536),
                timeout=self.timeout,
            )
            if response:
                messages, _ = extract_messages(response)
                if messages:
                    return messages[0]
            return None
        except (OSError, asyncio.TimeoutError) as e:
            logger.warning("mllp_send_failed", error=str(e), name=self.name)
            self._connected = False
            return None

    async def send_no_ack(self, message: str) -> bool:
        """Send an HL7 message without waiting for ACK."""
        if not self._connected:
            if not await self.connect():
                return False

        try:
            data = wrap_mllp(message)
            self._writer.write(data)
            await self._writer.drain()
            return True
        except (OSError, asyncio.TimeoutError) as e:
            logger.warning("mllp_send_failed", error=str(e), name=self.name)
            self._connected = False
            return False

    async def close(self) -> None:
        if self._writer:
            try:
                self._writer.close()
                await self._writer.wait_closed()
            except OSError:
                pass
        self._connected = False

    @property
    def is_connected(self) -> bool:
        return self._connected

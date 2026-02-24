"""Async MLLP server for receiving HL7 messages and sending ACKs."""

from __future__ import annotations

import asyncio
import ssl
from collections.abc import Callable
from typing import Any

import structlog

from src.transport.mllp_protocol import extract_messages, wrap_mllp

logger = structlog.get_logger(__name__)


class MLLPServer:
    def __init__(
        self,
        host: str = "0.0.0.0",
        port: int = 2575,
        on_message: Callable[[str], str | None] | None = None,
        ssl_context: ssl.SSLContext | None = None,
    ):
        self.host = host
        self.port = port
        self._on_message = on_message
        self._ssl_context = ssl_context
        self._server: asyncio.Server | None = None
        self._connections: set[asyncio.Task[Any]] = set()

    @property
    def tls_enabled(self) -> bool:
        return self._ssl_context is not None

    async def start(self) -> None:
        self._server = await asyncio.start_server(
            self._handle_client, self.host, self.port, ssl=self._ssl_context,
        )
        logger.info("mllp_server_started", host=self.host, port=self.port, tls=self.tls_enabled)

    async def stop(self) -> None:
        if self._server:
            self._server.close()
            await self._server.wait_closed()
        for task in self._connections:
            task.cancel()
        self._connections.clear()
        logger.info("mllp_server_stopped")

    async def _handle_client(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter,
    ) -> None:
        peer = writer.get_extra_info("peername")
        logger.info("mllp_client_connected", peer=peer)
        buffer = b""

        try:
            while True:
                data = await reader.read(65536)
                if not data:
                    break
                buffer += data
                messages, buffer = extract_messages(buffer)

                for msg in messages:
                    logger.debug("mllp_received", length=len(msg))
                    ack_msg = None
                    if self._on_message:
                        ack_msg = self._on_message(msg)

                    if ack_msg is None:
                        ack_msg = self._auto_ack(msg)

                    response = wrap_mllp(ack_msg)
                    writer.write(response)
                    await writer.drain()
        except (OSError, asyncio.CancelledError):
            pass
        finally:
            try:
                writer.close()
                await writer.wait_closed()
            except OSError:
                pass
            logger.info("mllp_client_disconnected", peer=peer)

    def _auto_ack(self, message: str) -> str:
        """Generate a simple ACK for received message."""
        # Extract message control ID from MSH.10
        control_id = ""
        lines = message.split("\r")
        if lines:
            msh_fields = lines[0].split("|")
            if len(msh_fields) > 9:
                control_id = msh_fields[9]

        segments = [
            "MSH|^~\\&|||||||ACK|" + control_id + "|P|2.5.1",
            f"MSA|AA|{control_id}",
        ]
        return "\r".join(segments)

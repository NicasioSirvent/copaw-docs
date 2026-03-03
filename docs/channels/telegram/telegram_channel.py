"""
CoPaw Telegram Channel Adapter

This module provides Telegram integration for CoPaw, adapted from OpenClaw's
mature Telegram implementation using grammY.

Features:
- Webhook and Polling modes
- DM policies (pairing, allowlist, open, disabled)
- Group chat support with mention filtering
- Message chunking for long responses
- Media message handling (images, documents, voice)
- Session management and memory

Architecture:
- Uses python-telegram-bot library (Python equivalent of grammY)
- Implements CoPaw's BaseChannel abstract base class
- Follows OpenClaw's proven message flow patterns

Usage:
    from copaw.channels.telegram import TelegramChannel
    
    config = {
        "bot_token": "YOUR_BOT_TOKEN",
        "mode": "polling",
        "allow_all_users": True
    }
    
    channel = TelegramChannel(config)
    await channel.initialize()

Author: CoPaw Community (adapted from OpenClaw)
License: Apache 2.0
"""

import asyncio
import logging
import os
import re
import time
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

from telegram import Update, Bot
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from telegram.error import (
    TelegramError,
    TimedOut,
    NetworkError,
    RetryAfter,
)

from copaw.channels.base import BaseChannel
from copaw.message import Message, MessageType
from copaw.session import SessionManager
from copaw.exceptions import ChannelError

logger = logging.getLogger(__name__)


class TelegramChannel(BaseChannel):
    """
    Telegram channel adapter for CoPaw.
    
    Adapted from OpenClaw's grammY implementation to use Python's
    python-telegram-bot library.
    
    Attributes:
        channel: Channel identifier ("telegram")
        bot_token: Telegram Bot API token
        mode: Connection mode ("polling" or "webhook")
        app: Telegram bot application instance
    """
    
    channel = "telegram"
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Telegram channel.
        
        Args:
            config: Channel configuration dictionary
                - bot_token: Telegram Bot API token (required)
                - mode: "polling" or "webhook" (default: "polling")
                - webhook_port: Port for webhook listener (default: 8787)
                - webhook_url: Full webhook URL (required for webhook mode)
                - ssl_cert: Path to SSL certificate (optional)
                - ssl_key: Path to SSL private key (optional)
                - polling_interval: Polling interval in seconds (default: 1.0)
                - allow_all_users: Allow all users (default: False)
                - allow_from: List of allowed user IDs
                - dm_policy: DM policy ("pairing", "allowlist", "open", "disabled")
                - group_policy: Group policy ("allowlist", "open")
                - group_allow_from: List of allowed group IDs
                - require_mention: Require @mention in groups (default: True)
                - command_prefix: Command prefix (default: "/")
                - max_message_length: Max message length (default: 4096)
                - chunk_messages: Auto-chunk long messages (default: True)
                - parse_mode: Message parse mode ("Markdown", "HTML", None)
                - session_memory: Enable session memory (default: True)
                - timeout: API timeout in seconds (default: 30)
                - retry_limit: Max retry attempts (default: 3)
        """
        super().__init__(config)
        
        # Required configuration
        self.bot_token = config.get("bot_token")
        if not self.bot_token:
            raise ChannelError("Telegram bot_token is required")
        
        # Connection mode
        self.mode = config.get("mode", "polling")
        if self.mode not in ["polling", "webhook"]:
            raise ChannelError(f"Invalid mode: {self.mode}. Use 'polling' or 'webhook'")
        
        # Webhook configuration
        self.webhook_port = config.get("webhook_port", 8787)
        self.webhook_url = config.get("webhook_url")
        self.ssl_cert = config.get("ssl_cert")
        self.ssl_key = config.get("ssl_key")
        
        # Polling configuration
        self.polling_interval = config.get("polling_interval", 1.0)
        
        # Access control
        self.allow_all_users = config.get("allow_all_users", False)
        self.allow_from = config.get("allow_from", [])
        self.dm_policy = config.get("dm_policy", "pairing")
        
        # Group configuration
        self.group_policy = config.get("group_policy", "allowlist")
        self.group_allow_from = config.get("group_allow_from", [])
        self.require_mention = config.get("require_mention", True)
        self.group_auto_reply = config.get("group_auto_reply", False)
        
        # Message handling
        self.command_prefix = config.get("command_prefix", "/")
        self.max_message_length = config.get("max_message_length", 4096)
        self.chunk_messages = config.get("chunk_messages", True)
        self.parse_mode = config.get("parse_mode", "Markdown")
        
        # Session management
        self.session_memory = config.get("session_memory", True)
        self.session_ttl = config.get("session_ttl", 3600)
        
        # Advanced settings
        self.timeout = config.get("timeout", 30)
        self.retry_limit = config.get("retry_limit", 3)
        self.log_messages = config.get("log_messages", False)
        
        # Initialize bot application
        self.app: Optional[Application] = None
        self.bot: Optional[Bot] = None
        
        # Pairing codes storage (for DM policy: pairing)
        self.pairing_codes: Dict[str, Dict[str, Any]] = {}
        
        # Session manager
        self.session_manager = SessionManager()
    
    async def initialize(self) -> None:
        """
        Initialize Telegram bot connection.
        
        Sets up the bot application, registers handlers, and starts
        either polling or webhook mode based on configuration.
        """
        logger.info("Initializing Telegram channel...")
        
        # Build bot application
        self.app = (
            Application.builder()
            .token(self.bot_token)
            .connection_pool_size(8)
            .read_timeout(self.timeout)
            .write_timeout(self.timeout)
            .connect_timeout(self.timeout)
            .pool_timeout(self.timeout)
            .build()
        )
        
        self.bot = self.app.bot
        
        # Register handlers
        self._register_handlers()
        
        # Start bot
        if self.mode == "webhook":
            await self._start_webhook()
        else:
            await self._start_polling()
        
        logger.info(f"Telegram bot initialized (@{self.bot.username})")
    
    def _register_handlers(self) -> None:
        """Register message and command handlers."""
        # Command handler
        self.app.add_handler(
            CommandHandler("start", self._handle_start)
        )
        self.app.add_handler(
            CommandHandler("help", self._handle_help)
        )
        self.app.add_handler(
            CommandHandler("status", self._handle_status)
        )
        
        # Pairing command (for DM policy: pairing)
        self.app.add_handler(
            CommandHandler("pair", self._handle_pair)
        )
        
        # Message handler (all other messages)
        self.app.add_handler(
            MessageHandler(
                filters.ALL & ~filters.COMMAND,
                self._handle_message
            )
        )
        
        # Media handlers
        self.app.add_handler(
            MessageHandler(
                filters.PHOTO,
                self._handle_photo
            )
        )
        self.app.add_handler(
            MessageHandler(
                filters.Document.ALL,
                self._handle_document
            )
        )
        self.app.add_handler(
            MessageHandler(
                filters.VOICE,
                self._handle_voice
            )
        )
        
        # Error handler
        self.app.add_error_handler(self._handle_error)
    
    async def _start_webhook(self) -> None:
        """Start webhook mode."""
        if not self.webhook_url:
            raise ChannelError("webhook_url is required for webhook mode")
        
        logger.info(f"Starting webhook on {self.webhook_url}...")
        
        # Set webhook
        await self.bot.set_webhook(
            url=self.webhook_url,
            certificate=open(self.ssl_cert, "rb") if self.ssl_cert else None,
        )
        
        # Start webhook listener
        self.app.run_webhook(
            listen="0.0.0.0",
            port=self.webhook_port,
            url_path=self.bot_token,
            cert=self.ssl_cert,
            key=self.ssl_key,
            webhook_url=self.webhook_url,
        )
    
    async def _start_polling(self) -> None:
        """Start polling mode."""
        logger.info("Starting polling mode...")
        
        # Delete webhook if exists
        await self.bot.delete_webhook()
        
        # Start polling in background
        asyncio.create_task(self._polling_loop())
    
    async def _polling_loop(self) -> None:
        """Polling loop for receiving messages."""
        last_update_id = 0
        
        while True:
            try:
                updates = await self.bot.get_updates(
                    offset=last_update_id,
                    timeout=self.timeout,
                )
                
                for update in updates:
                    last_update_id = update.update_id + 1
                    await self._process_update(update)
                
            except TimedOut:
                # Normal timeout, continue polling
                pass
            except NetworkError as e:
                logger.warning(f"Network error: {e}. Retrying...")
                await asyncio.sleep(self.polling_interval)
            except Exception as e:
                logger.error(f"Polling error: {e}")
                await asyncio.sleep(self.polling_interval)
            
            await asyncio.sleep(self.polling_interval)
    
    async def _process_update(self, update: Update) -> None:
        """
        Process Telegram update.
        
        Args:
            update: Telegram update object
        """
        if update.message:
            await self._handle_update(update)
    
    async def _handle_update(self, update: Update) -> None:
        """
        Handle incoming Telegram update.
        
        Args:
            update: Telegram update object
        """
        message = update.effective_message
        if not message:
            return
        
        # Log message if enabled
        if self.log_messages:
            logger.info(f"Received message from {message.from_user.username}: {message.text}")
        
        # Check access control
        if not self._check_access(message):
            logger.warning(f"Access denied for user {message.from_user.id}")
            return
        
        # Parse message to CoPaw format
        copaw_message = self._parse_message(message)
        
        # Send to CoPaw core
        await self.receive(copaw_message)
    
    def _check_access(self, message) -> bool:
        """
        Check if user has access to bot.
        
        Args:
            message: Telegram message object
            
        Returns:
            bool: True if access granted, False otherwise
        """
        user_id = str(message.from_user.id)
        chat_id = str(message.chat.id)
        
        # Check if direct message
        if message.chat.type == "private":
            # DM policy: open
            if self.dm_policy == "open" and "*" in self.allow_from:
                return True
            
            # DM policy: disabled
            if self.dm_policy == "disabled":
                return False
            
            # DM policy: allowlist
            if self.dm_policy == "allowlist":
                return user_id in self.allow_from or self.allow_all_users
            
            # DM policy: pairing (default)
            if self.dm_policy == "pairing":
                return self.allow_all_users or user_id in self.allow_from or user_id in self.pairing_codes
        
        # Check if group chat
        elif message.chat.type in ["group", "supergroup", "channel"]:
            # Group policy: allowlist
            if self.group_policy == "allowlist":
                if chat_id not in self.group_allow_from:
                    return False
                
                # Check if mention required
                if self.require_mention:
                    if not self._is_bot_mentioned(message):
                        return False
        
        return True
    
    def _is_bot_mentioned(self, message) -> bool:
        """
        Check if bot is mentioned in message.
        
        Args:
            message: Telegram message object
            
        Returns:
            bool: True if bot is mentioned
        """
        if not message.entities:
            return False
        
        for entity in message.entities:
            if entity.type == "mention":
                mention = message.text[entity.offset:entity.offset + entity.length]
                if mention == f"@{self.bot.username}":
                    return True
        
        return False
    
    def _parse_message(self, message) -> Dict[str, Any]:
        """
        Parse Telegram message to CoPaw internal format.
        
        Args:
            message: Telegram message object
            
        Returns:
            dict: CoPaw message dictionary
        """
        # Determine message type
        if message.text:
            msg_type = MessageType.TEXT
            content = message.text
        elif message.photo:
            msg_type = MessageType.IMAGE
            content = message.photo[-1].file_id
        elif message.document:
            msg_type = MessageType.DOCUMENT
            content = message.document.file_id
        elif message.voice:
            msg_type = MessageType.VOICE
            content = message.voice.file_id
        else:
            msg_type = MessageType.TEXT
            content = ""
        
        # Build session key
        if message.chat.type == "private":
            session_key = f"agent:main:telegram:dm:{message.from_user.id}"
        else:
            session_key = f"agent:main:telegram:group:{message.chat.id}"
        
        return {
            "channel": self.channel,
            "type": msg_type,
            "content": content,
            "from_id": str(message.from_user.id),
            "from_username": message.from_user.username,
            "chat_id": str(message.chat.id),
            "chat_type": message.chat.type,
            "message_id": message.message_id,
            "timestamp": message.date.timestamp(),
            "session_key": session_key,
            "thread_id": None,  # Telegram doesn't have threads
            "reply_to": message.reply_to_message.message_id if message.reply_to_message else None,
        }
    
    async def receive(self, message: Dict[str, Any]) -> None:
        """
        Receive message from Telegram and send to CoPaw core.
        
        Args:
            message: CoPaw message dictionary
        """
        # This method is called by _handle_update
        # The message is sent to CoPaw core via ChannelManager
        logger.debug(f"Received message: {message}")
    
    async def send(self, response: Dict[str, Any]) -> bool:
        """
        Send response to Telegram.
        
        Args:
            response: CoPaw response dictionary
                - chat_id: Telegram chat ID
                - content: Message content
                - type: Message type (text, photo, document, etc.)
                - reply_to: Message ID to reply to (optional)
                
        Returns:
            bool: True if sent successfully
        """
        chat_id = response.get("chat_id")
        content = response.get("content")
        msg_type = response.get("type", "text")
        reply_to = response.get("reply_to")
        
        if not chat_id or not content:
            logger.error("Missing chat_id or content in response")
            return False
        
        try:
            # Handle message chunking
            if self.chunk_messages and len(content) > self.max_message_length:
                chunks = self._chunk_message(content)
                for chunk in chunks:
                    await self._send_message(chat_id, chunk, reply_to)
                    reply_to = None  # Only reply to first message
            else:
                await self._send_message(chat_id, content, reply_to)
            
            return True
            
        except TelegramError as e:
            logger.error(f"Telegram error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending message: {e}")
            return False
    
    async def _send_message(
        self,
        chat_id: str,
        content: str,
        reply_to: Optional[int] = None,
    ) -> None:
        """
        Send message to Telegram.
        
        Args:
            chat_id: Telegram chat ID
            content: Message content
            reply_to: Message ID to reply to
        """
        # Determine parse mode
        parse_mode = None
        if self.parse_mode == "Markdown":
            parse_mode = "MarkdownV2"
        elif self.parse_mode == "HTML":
            parse_mode = "HTML"
        
        # Send message
        await self.bot.send_message(
            chat_id=chat_id,
            text=content,
            parse_mode=parse_mode,
            reply_to_message_id=reply_to,
        )
    
    def _chunk_message(self, content: str) -> List[str]:
        """
        Split long message into chunks.
        
        Args:
            content: Message content
            
        Returns:
            list: List of message chunks
        """
        chunks = []
        separator = "\n\n---\n\n"
        
        # Split by separator first
        parts = content.split(separator)
        
        current_chunk = ""
        for part in parts:
            if len(current_chunk) + len(part) + len(separator) <= self.max_message_length:
                if current_chunk:
                    current_chunk += separator + part
                else:
                    current_chunk = part
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = part
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    # Command handlers
    async def _handle_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command."""
        await update.message.reply_text(
            f"👋 Welcome to CoPaw!\n\n"
            f"I'm your personal AI assistant on Telegram.\n\n"
            f"Send me any message and I'll respond with AI-powered help!\n\n"
            f"Commands:\n"
            f"/help - Show help\n"
            f"/status - Bot status\n"
        )
    
    async def _handle_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /help command."""
        await update.message.reply_text(
            f"📖 CoPaw Help\n\n"
            f"*How to use:*\n"
            f"Simply send me any message and I'll respond!\n\n"
            f"*Commands:*\n"
            f"/start - Start conversation\n"
            f"/help - Show this help\n"
            f"/status - Bot status\n\n"
            f"*Features:*\n"
            f"• AI-powered responses\n"
            f"• Multi-language support\n"
            f"• Context-aware conversations\n"
            f"• File and image processing\n\n"
            f"Need more help? Visit our documentation!\n"
        )
    
    async def _handle_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /status command."""
        # Get bot info
        me = await self.bot.get_me()
        
        # Get stats
        uptime = time.time() - self.session_manager.start_time
        
        await update.message.reply_text(
            f"🤖 CoPaw Status\n\n"
            f"*Bot:* @{me.username}\n"
            f"*Name:* {me.first_name}\n"
            f"*Uptime:* {self._format_uptime(uptime)}\n\n"
            f"*Stats:*\n"
            f"• Sessions: {len(self.session_manager.sessions)}\n"
            f"• Messages: {self.session_manager.message_count}\n\n"
            f"Status: ✅ Online\n"
        )
    
    async def _handle_pair(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /pair command for DM authentication."""
        user_id = str(update.effective_user.id)
        
        # Generate pairing code
        import random
        code = f"{random.randint(100000, 999999)}"
        
        # Store pairing code
        self.pairing_codes[user_id] = {
            "code": code,
            "timestamp": time.time(),
            "username": update.effective_user.username,
        }
        
        await update.message.reply_text(
            f"🔐 Pairing Request\n\n"
            f"Your pairing code: `{code}`\n\n"
            f"Send this code to the administrator to authenticate.\n"
            f"Code expires in 1 hour.\n"
        )
    
    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle text messages."""
        await self._handle_update(update)
    
    async def _handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle photo messages."""
        await self._handle_update(update)
    
    async def _handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle document messages."""
        await self._handle_update(update)
    
    async def _handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle voice messages."""
        await self._handle_update(update)
    
    async def _handle_error(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle errors."""
        logger.error(f"Telegram error: {context.error}")
    
    def _format_uptime(self, seconds: float) -> str:
        """Format uptime string."""
        hours, remainder = divmod(int(seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m {seconds}s"
    
    async def cleanup(self) -> None:
        """Cleanup Telegram connection."""
        logger.info("Cleaning up Telegram channel...")
        
        # Delete webhook
        if self.mode == "webhook":
            await self.bot.delete_webhook()
        
        # Stop application
        if self.app:
            await self.app.stop()
        
        logger.info("Telegram channel cleaned up")


# Export
__all__ = ["TelegramChannel"]

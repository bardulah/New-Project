"""
Centralized logging configuration for PsycheEdge
Provides structured JSON logging with context and correlation IDs
"""
import logging
import logging.handlers
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
import traceback


class StructuredFormatter(logging.Formatter):
    """JSON formatter for structured logging"""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_data = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }

        # Add extra fields from record
        if hasattr(record, 'agent_id'):
            log_data['agent_id'] = record.agent_id
        if hasattr(record, 'agent_type'):
            log_data['agent_type'] = record.agent_type
        if hasattr(record, 'generation'):
            log_data['generation'] = record.generation
        if hasattr(record, 'fitness'):
            log_data['fitness'] = record.fitness
        if hasattr(record, 'cycle'):
            log_data['cycle'] = record.cycle
        if hasattr(record, 'event_type'):
            log_data['event_type'] = record.event_type

        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': traceback.format_exception(*record.exc_info)
            }

        # Add any custom extra fields
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'created', 'filename', 'funcName',
                          'levelname', 'levelno', 'lineno', 'module', 'msecs',
                          'message', 'pathname', 'process', 'processName',
                          'relativeCreated', 'thread', 'threadName', 'exc_info',
                          'exc_text', 'stack_info', 'agent_id', 'agent_type',
                          'generation', 'fitness', 'cycle', 'event_type']:
                log_data[key] = value

        return json.dumps(log_data)


class HumanReadableFormatter(logging.Formatter):
    """Human-readable formatter for console output"""

    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format log record for human reading"""
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']

        # Build context string
        context_parts = []
        if hasattr(record, 'agent_id'):
            context_parts.append(f"agent={record.agent_id[:8]}")
        if hasattr(record, 'agent_type'):
            context_parts.append(f"type={record.agent_type}")
        if hasattr(record, 'generation'):
            context_parts.append(f"gen={record.generation}")
        if hasattr(record, 'fitness'):
            context_parts.append(f"fit={record.fitness:.1f}")
        if hasattr(record, 'cycle'):
            context_parts.append(f"cycle={record.cycle}")

        context = f" [{', '.join(context_parts)}]" if context_parts else ""

        timestamp = datetime.fromtimestamp(record.created).strftime('%H:%M:%S.%f')[:-3]

        return (f"{timestamp} {color}{record.levelname:8}{reset} "
                f"{record.name:30} {record.getMessage()}{context}")


def setup_logging(
    log_dir: Path = Path("psyche_edge/data/logs"),
    log_level: str = "INFO",
    enable_file_logging: bool = True,
    enable_json_logging: bool = True,
    enable_console_logging: bool = True
) -> None:
    """
    Configure logging for the entire application

    Args:
        log_dir: Directory for log files
        log_level: Minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        enable_file_logging: Write logs to rotating files
        enable_json_logging: Write structured JSON logs
        enable_console_logging: Write human-readable logs to console
    """
    # Create log directory
    log_dir.mkdir(parents=True, exist_ok=True)

    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))

    # Clear existing handlers
    root_logger.handlers.clear()

    # Console handler (human-readable)
    if enable_console_logging:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(HumanReadableFormatter())
        root_logger.addHandler(console_handler)

    # Rotating file handler (human-readable)
    if enable_file_logging:
        file_handler = logging.handlers.RotatingFileHandler(
            log_dir / "psyche_edge.log",
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(HumanReadableFormatter())
        root_logger.addHandler(file_handler)

    # JSON structured logs (for machine parsing)
    if enable_json_logging:
        json_handler = logging.handlers.RotatingFileHandler(
            log_dir / "psyche_edge.json.log",
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5
        )
        json_handler.setLevel(logging.DEBUG)
        json_handler.setFormatter(StructuredFormatter())
        root_logger.addHandler(json_handler)

    # Log startup
    root_logger.info("Logging initialized", extra={
        'log_dir': str(log_dir),
        'log_level': log_level,
        'handlers': [type(h).__name__ for h in root_logger.handlers]
    })


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the given name

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


# Context helpers for structured logging
class LogContext:
    """Context manager for adding fields to all logs within a block"""

    def __init__(self, logger: logging.Logger, **kwargs):
        self.logger = logger
        self.context = kwargs
        self.old_factory = None

    def __enter__(self):
        """Add context fields"""
        old_factory = logging.getLogRecordFactory()

        def record_factory(*args, **kwargs):
            record = old_factory(*args, **kwargs)
            for key, value in self.context.items():
                setattr(record, key, value)
            return record

        self.old_factory = old_factory
        logging.setLogRecordFactory(record_factory)
        return self

    def __exit__(self, *args):
        """Remove context fields"""
        if self.old_factory:
            logging.setLogRecordFactory(self.old_factory)


def log_agent_event(
    logger: logging.Logger,
    event_type: str,
    agent_id: str,
    agent_type: str,
    message: str,
    **extra_fields
):
    """
    Helper to log agent events with consistent structure

    Args:
        logger: Logger instance
        event_type: Type of event (birth, death, evolution, competition, etc.)
        agent_id: Agent identifier
        agent_type: Agent class name
        message: Log message
        **extra_fields: Additional fields to include
    """
    logger.info(message, extra={
        'event_type': event_type,
        'agent_id': agent_id,
        'agent_type': agent_type,
        **extra_fields
    })


def log_swarm_event(
    logger: logging.Logger,
    event_type: str,
    message: str,
    **extra_fields
):
    """
    Helper to log swarm-level events

    Args:
        logger: Logger instance
        event_type: Type of event (cycle_start, cycle_end, etc.)
        message: Log message
        **extra_fields: Additional fields to include
    """
    logger.info(message, extra={
        'event_type': event_type,
        **extra_fields
    })

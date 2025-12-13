"""
Centralized Logging Configuration for Census ACS EDA Pipeline
Provides hierarchical file logging with context switching support
"""
import logging
import os
import gc
from datetime import datetime
from typing import Optional, Dict
from pathlib import Path

# Custom log level for VERBOSE (between DEBUG and INFO)
VERBOSE = 15
logging.addLevelName(VERBOSE, "VERBOSE")


def verbose(self, message, *args, **kwargs):
    """Add verbose logging method to Logger class"""
    if self.isEnabledFor(VERBOSE):
        self._log(VERBOSE, message, args, **kwargs)


logging.Logger.verbose = verbose


class LogContext:
    """Manages logging context for state/survey/scope combinations"""

    def __init__(self, base_dir: str = "./logs"):
        self.base_dir = base_dir
        self.state: Optional[str] = None
        self.survey: Optional[str] = None
        self.scope: Optional[str] = None
        self._current_handler: Optional[logging.FileHandler] = None
        self._console_handler: Optional[logging.StreamHandler] = None
        self._root_logger = logging.getLogger("census_eda")
        self._console_enabled = False
        self._setup_root_logger()

    def _setup_root_logger(self):
        """Initialize root logger with default configuration"""
        self._root_logger.setLevel(logging.DEBUG)
        # Prevent propagation to root logger
        self._root_logger.propagate = False

        # Console handler (optional, controlled by enable_console)
        self._console_handler = logging.StreamHandler()
        self._console_handler.setLevel(logging.DEBUG)
        console_format = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        self._console_handler.setFormatter(console_format)

    def set_context(self, state: str, survey: str, scope: str):
        """
        Set the current logging context and create/switch log file

        Args:
            state: State name (e.g., "Kansas", "California")
            survey: Survey type (e.g., "population", "housing")
            scope: Survey scope (e.g., "1-Year", "5-Year")
        """
        self.state = state
        self.survey = survey.lower()
        self.scope = scope

        # Close previous file handler if exists
        self._cleanup_handler()

        # Create log directory and file
        log_path = self._get_log_path()
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        # Create new file handler
        self._current_handler = logging.FileHandler(log_path, mode='a', encoding='utf-8')
        self._current_handler.setLevel(logging.DEBUG)

        file_format = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        self._current_handler.setFormatter(file_format)

        # Add to root logger
        self._root_logger.addHandler(self._current_handler)

        self._root_logger.info(
            f"Logging context set: state={state}, survey={survey}, scope={scope}"
        )
        self._root_logger.info(f"Log file: {log_path}")

    def _get_log_path(self) -> str:
        """Generate log file path based on current context"""
        timestamp = datetime.now().strftime("%y_%m_%d_%H%M")
        filename = f"{self.scope}_{self.survey}_{timestamp}.log"

        # Normalize scope for directory (e.g., "1-Year" -> "1-year")
        scope_dir = self.scope.lower()

        return os.path.join(
            self.base_dir,
            self.state,
            scope_dir,
            self.survey,
            filename
        )

    def _cleanup_handler(self):
        """Properly close and remove file handler"""
        if self._current_handler:
            self._current_handler.flush()
            self._current_handler.close()
            self._root_logger.removeHandler(self._current_handler)
            self._current_handler = None
            gc.collect()

    def enable_console(self, enable: bool = True, level: int = logging.DEBUG):
        """Enable or disable console output"""
        if enable:
            if not self._console_enabled:
                self._console_handler.setLevel(level)
                self._root_logger.addHandler(self._console_handler)
                self._console_enabled = True
        else:
            if self._console_enabled:
                self._root_logger.removeHandler(self._console_handler)
                self._console_enabled = False

    def set_console_level(self, level: int):
        """Set console logging level"""
        self._console_handler.setLevel(level)

    def close(self):
        """Cleanup all handlers - call at end of processing"""
        self._cleanup_handler()
        if self._console_enabled:
            self._root_logger.removeHandler(self._console_handler)
            self._console_enabled = False

    def get_current_log_path(self) -> Optional[str]:
        """Get path to current log file"""
        if self._current_handler:
            return self._current_handler.baseFilename
        return None


# Global singleton for easy access
_log_context: Optional[LogContext] = None


def get_log_context(base_dir: str = "./logs") -> LogContext:
    """Get or create the global log context"""
    global _log_context
    if _log_context is None:
        _log_context = LogContext(base_dir)
    return _log_context


def reset_log_context():
    """Reset the global log context (useful for testing)"""
    global _log_context
    if _log_context:
        _log_context.close()
    _log_context = None


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for a specific module/component

    Usage:
        from logging_config import get_logger
        logger = get_logger(__name__)
        logger.info("Processing started")
        logger.debug("Detailed info here")
        logger.verbose("Very detailed info")
    """
    return logging.getLogger(f"census_eda.{name}")


# Convenience functions for prefix-based logging (migration helper)
def log_info(msg: str, logger_name: str = "main"):
    """Log INFO level message"""
    get_logger(logger_name).info(msg)


def log_verbose(msg: str, logger_name: str = "main"):
    """Log VERBOSE level message"""
    get_logger(logger_name).verbose(msg)


def log_debug(msg: str, logger_name: str = "main"):
    """Log DEBUG level message"""
    get_logger(logger_name).debug(msg)


def log_warning(msg: str, logger_name: str = "main"):
    """Log WARNING level message"""
    get_logger(logger_name).warning(msg)


def log_error(msg: str, logger_name: str = "main"):
    """Log ERROR level message"""
    get_logger(logger_name).error(msg)


def log_success(msg: str, logger_name: str = "main"):
    """Log success message at INFO level with SUCCESS prefix"""
    get_logger(logger_name).info(f"SUCCESS: {msg}")


def log_config(msg: str, logger_name: str = "main"):
    """Log configuration message at INFO level with CONFIG prefix"""
    get_logger(logger_name).info(f"CONFIG: {msg}")


def log_complete(msg: str, logger_name: str = "main"):
    """Log completion message at INFO level with COMPLETE prefix"""
    get_logger(logger_name).info(f"COMPLETE: {msg}")


# Step-specific logging helpers
def log_step(step_name: str, status: str = "START", logger_name: str = "main"):
    """Log pipeline step transitions"""
    get_logger(logger_name).info(f"[{step_name}] {status}")


def log_dataframe_info(df, name: str = "DataFrame", logger_name: str = "main"):
    """Log DataFrame summary information"""
    logger = get_logger(logger_name)
    logger.info(f"{name}: {len(df):,} rows x {len(df.columns)} cols")


def log_memory_usage(msg: str = "", logger_name: str = "memory"):
    """Log memory-related information"""
    get_logger(logger_name).debug(f"MEMORY: {msg}")


# Decorators for logging function entry/exit
def logged_function(logger_name: str = "main"):
    """Decorator to log function entry and exit"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = get_logger(logger_name)
            logger.debug(f"ENTER: {func.__name__}")
            try:
                result = func(*args, **kwargs)
                logger.debug(f"EXIT: {func.__name__}")
                return result
            except Exception as e:
                logger.error(f"ERROR in {func.__name__}: {e}")
                raise
        return wrapper
    return decorator

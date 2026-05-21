"""
Claude Configuration Sync & Audit Tool

A comprehensive tool for syncing and auditing Claude configuration files
between project-specific and global locations.
"""

__version__ = "1.0.0"
__author__ = "Matteo Cervelli"

from .audit import AuditManager
from .sync import SyncManager, SyncResult
from .conflict_resolver import ConflictResolver
from .settings_analyzer import SettingsAnalyzer, SettingsAnalysis
from .file_handler import FileHandler
from .reporter import Reporter

__all__ = [
    "AuditManager",
    "SyncManager",
    "SyncResult",
    "ConflictResolver",
    "SettingsAnalyzer",
    "SettingsAnalysis",
    "FileHandler",
    "Reporter",
]

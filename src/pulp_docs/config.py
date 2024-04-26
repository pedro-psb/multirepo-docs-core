from __future__ import annotations

import tempfile
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

from dynaconf import Dynaconf, Validator


def init_config(setting_file: Optional[Path] = None) -> ConfigSchema:
    setting_files = [setting_file] if setting_file else []
    return Dynaconf(settings_file=setting_files)


class FindStrategy(Enum):
    """
    Strategies on how to choose local repos, which should be used to override the defaults.

    Args:
        NONE: Don't use any local overrides.
        CURRENT: If the CWD is a matching repo, use that.
        PARENT_WORKDIR: Lookup for matching repos in the parent workdir.
        LOOKUP_LIST: Use an explicit lookup_list defining the path for each repo override.
    """

    NONE = 0
    CURRENT = 1
    PARENT_WORKDIR = 2
    LOOKUP_LIST = 3


@dataclass
class ConfigSchema:
    remote_sync_config: RemoteSyncConfig
    repo_finder_config: RepoFinderConfig
    cli_config: CliConfig

    class Meta:
        validators: list[Validator] = []


@dataclass
class RemoteSyncConfig:
    """
    Args:
        sync: Wheter or not to sync (clone and rebase) changes to a managed repo.
        manged_repo_path: The local path to where the managed repo should operate.
    """

    sync: bool = True
    managed_repo_path: Path = Path(tempfile.gettempdir())


@dataclass
class RepoFinderConfig:
    strategy: FindStrategy = FindStrategy.CURRENT
    lookup_list: list[Path] = field(default_factory=list)


@dataclass
class CliConfig:
    livereload: bool = True
    watch_list: list[Path] = field(default_factory=list)

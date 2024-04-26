"""
This module is responsible for:
- reading the specfile that specifies the repositories and packages to be used.
- optionally fetching/syncing the remotes locally.
- matching those specs with filesystem repositories (fetched from remote or used-provided)

The `PackageData` is the main object of interest here, as it contains the fundamental information
for arranging the docs contents.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from pulp_docs.config import FindStrategy


def process_specfile(yml_specfile: Path) -> list[PackageData]:
    repo_spec_list = RepoUtils.parse_specfile(yml_specfile)
    package_data_list = RepoUtils.get_package_data(repo_spec_list)
    return package_data_list


@dataclass
class RepoSpec:
    name: str
    package_specs: list[PackageSpec]

    def create_repodata(self, abs_path: Path) -> RepoData:
        return RepoData(repo_spec=self, abs_path=abs_path)


@dataclass
class PackageSpec:
    name: str
    rel_path: Path


@dataclass
class RepoData:
    repo_spec: RepoSpec
    abs_path: Path
    package_data_list: list[PackageSpec] = []

    @property
    def name(self):
        return self.repo_spec.name

    def __post_init__(self):
        for package in self.repo_spec.package_specs:
            abs_path = self.abs_path / package.rel_path
            self._package_data.append(
                PackageData(repo_data=self, package_spec=package, abs_path=abs_path)
            )


@dataclass
class PackageData:
    repo_data: RepoData
    package_spec: PackageSpec
    abs_path: Path

    @property
    def name(self):
        return self.package_spec.name


class DataFinder:
    @staticmethod
    def get_from_local(
        strategy: FindStrategy, lookup_list: Optional[list[Path]] = None
    ) -> dict[str, Path]:
        return {}

    @staticmethod
    def get_from_remotes(sync: bool, root_dest: Path) -> dict[str, Path]:
        return {}


class RepoUtils:
    @staticmethod
    def parse_specfile(yml_specfile: Path) -> list[RepoSpec]:
        """Parse specfile in yaml format."""
        return [RepoSpec()]

    @staticmethod
    def get_package_data(repo_specs: list[RepoSpec]) -> list[PackageData]:
        # get config
        find_strategy = FindStrategy.CURRENT
        sync_remotes = True
        sync_dest = Path("/tmp")

        # get data paths
        user_paths = DataFinder.get_from_local(strategy=find_strategy)
        default_paths = DataFinder.get_from_remotes(
            sync=sync_remotes, root_dest=sync_dest
        )
        default_paths.update(user_paths)

        return [PackageData()]

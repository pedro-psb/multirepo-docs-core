import os
import subprocess
import sys
import typing as t
from pathlib import Path

from importlib.resources import files

TMP_DIR = Path("tmp")
WORKDIR = Path.home() / "workspace" / "multirepo-prototype"


def get_abspath(name: str) -> Path:
    return Path(WORKDIR / name).absolute()


def cast_bool(value: str) -> bool:
    return False if value.lower() in ("f", "false") else True


def cast_list(value: str) -> t.List[str]:
    return [v.strip() for v in value.split(",") if v]


class Config:
    """
    Configuration shared among CLI and mkdocs_macro.py hooks.

    Params:
        mkdocs_file: the base mkdocs used in serving/building
        repolist: the configuration repositories (which and how to fetch)
        clear_cache: whether to clear cache before downloading from remote
    """

    def __init__(self, from_environ: bool = False):
        if from_environ is False:
            self.verbose = False
            self.workdir = Path().absolute()
            self.mkdocs_file = files("pulp_docs").joinpath("data/mkdocs.yml")
            self.repolist = files("pulp_docs").joinpath("data/repolist.yml")
            self.clear_cache = False

            if env_mkdocs := os.environ.get("PULPDOCS_MKDOCS_FILE"):
                self.mkdocs_file = Path(env_mkdocs)
            self.disabled = []
        else:
            self.verbose = cast_bool(os.environ["PULPDOCS_VERBOSE"])
            self.workdir = Path(os.environ["PULPDOCS_WORKDIR"])
            self.mkdocs_file = Path(os.environ["PULPDOCS_MKDOCS_FILE"])
            self.repolist = Path(os.environ["PULPDOCS_REPOLIST"])
            self.clear_cache = cast_bool(os.environ["PULPDOCS_CLEAR_CACHE"])
            self.disabled = cast_list(os.environ.get("PULPDOCS_DISABLED", ""))
        self.watch: list[Path] = []
        self.livereload = True
        self.test_mode = cast_bool(os.environ.get("PULPDOCS_TEST_MODE", "f"))

    def get_environ_dict(self):
        return {f"PULPDOCS_{k.upper()}": str(v) for k, v in self.__dict__.items()}


class PulpDocs:
    """Main instance of pulp docs"""

    def serve(self, config: Config, dry_run: bool = False):
        # Process option to pass to command
        cmd = ["mkdocs", "serve"]

        env = os.environ.copy()
        env.update(config.get_environ_dict())
        watch_list = [("--watch", watched) for watched in config.watch]
        flag_list = []
        if config.livereload is False:
            flag_list.append(("--no-livereload",))
        options: t.List[tuple] = [("--config-file", config.mkdocs_file)]
        options.extend(watch_list)
        options.extend(flag_list)

        for opt in options:
            cmd.extend(opt)

        # Run command
        print("Running:", " ".join(str(s) for s in cmd))
        if dry_run is True:
            print("Dry run mode.")
            return
        subprocess.run(cmd, env=env)

    def build(
        self, config: Config, dry_run: bool = False, target: t.Optional[Path] = None
    ):
        # TODO: implement target
        # Process option to pass to command
        cmd = ["mkdocs", "build"]

        env = os.environ.copy()
        env.update(config.get_environ_dict())
        options = (
            ("--config-file", config.mkdocs_file),
            ("--site-dir", str(Path("site").absolute())),
        )

        for opt in options:
            cmd.extend(opt)

        # Run command
        print("Building:", " ".join(str(s) for s in cmd))
        if dry_run is True:
            print("Dry run mode.")
            return
        result = subprocess.run(cmd, env=env)
        sys.exit(result.returncode)

    def status(self, config: Config, dry_run: bool = False):
        raise NotImplementedError

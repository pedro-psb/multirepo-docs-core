from pathlib import Path
from pulp_docs.main import PulpDocs, Config


def snapshot_fixture(fixture_dir: Path, repolist: Path, target: Path) -> Path:
    """Builds snapshot of the fixture-docs using @fixture_dir and @repolist at @target.

    The snapshot should be taken after someone carefully inspect the core elements of
    the site looks as expected, like:
    * Navigation display: nav items that should and shouldnt be there.
    * Special pages behave as expected, like RestAPI, Changes and index pages.
    * Regular pages exists (or dont exist) where expected inside plugins and sections.

    The snapshot is not intended to provide a 1:1 comparision, but more of a structural
    comparision, so at least we catch obivous structural regressions.

    Params:
        fixture_dir: A dir which should contain `{repository_name}/{repository_tree}`
        repolist: A yaml file containing the aggregation config.
        target: Dir where to write the build.

    Returns:
        The Path of the new snapshot. The dirname is commit hash at the moment of the
        which snapshot.
    """
    # Guards to avoid surprises
    if not fixture_dir.is_dir():
        raise ValueError(f"'fixture_dir' should be a dir: {fixture_dir}")
    if not list(fixture_dir.iterdir()):
        raise ValueError(f"'fixture_dir' should NOT be empty.: {fixture_dir}")

    if not target.is_dir():
        raise ValueError(f"'fixture_dir' should be a dir: {target}")
    if list(fixture_dir.iterdir()):
        raise ValueError(f"'target' must be empty.: {target}")

    if repolist.suffix not in (".yml", "yaml"):
        raise ValueError(f"'repolist' must be a YAML file: {repolist.name}")

    # TODO: test this.
    config = Config()
    config.repolist = repolist.absolute()
    pulp_docs = PulpDocs(config)
    pulp_docs.build(target=target)

    return Path()

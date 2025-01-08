from pulp_docs.test_tools.snapshot import snapshot_fixture
from pathlib import Path


def test_snapshot_fixture(tmp_path):
    """Test that using different fixture_dir or repolist the snapshot is different."""
    fixture_dir = Path()
    target = Path()
    repolist = Path()
    dirname = snapshot_fixture(fixture_dir, repolist, target)

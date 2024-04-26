from pulp_docs.repository import (PackageSpec, RepoSpec, RepoUtils,
                                  process_specfile)

yml_specfileA = """\
repositories:
  - name: "pulp-docs"
    packages:
      - name: "pulp-docs"
        type: "extra"
        rel_path: "."
        docs_src: "staging_docs"
        code_src: ["src/pulp_docs"]
  - name: "pulpcore"
    packages:
      - name: "pulpcore"
        type: "core"
        rel_path: "."
        docs_src: "staging_docs"
        code_src: ["src/pulp_docs"]
      - name: "pulp_certguard"
        type: "extra"
        rel_path: "pulp_certguard"
        docs_src: "staging_docs"
        code_src: ["pulp_certguard"]
      - name: "pulp_file"
        type: "plugin"
        rel_path: "pulp_file"
        docs_src: "staging_docs"
        code_src: ["pulp_file"]
"""
yml_specfileA_expected = [
    RepoSpec(name="pulp-docs", packages=[PackageSpec(name="pulp-docs")]),
    RepoSpec(
        name="pulpcore",
        packages=[
            PackageSpec(name="pulpcore"),
            PackageSpec(name="pulp_certguard"),
            PackageSpec(name="pulp_file"),
        ],
    ),
]


def test_process_specfile():
    ...


def test_repo_utils():
    ...

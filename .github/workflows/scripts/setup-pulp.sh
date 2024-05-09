#!/usr/bin/env bash
# coding=utf-8

set -mveuo pipefail

# make sure this script runs at the repo root
cd "$(dirname "$(realpath -e "$0")")"/../../..

source .github/workflows/scripts/utils.sh

export POST_SCRIPT=$PWD/.github/workflows/scripts/post_script.sh
export POST_DOCS_TEST=$PWD/.github/workflows/scripts/post_docs_test.sh
export FUNC_TEST_SCRIPT=$PWD/.github/workflows/scripts/func_test_script.sh

# Needed for both starting the service and building the docs.
# Gets set in .github/settings.yml, but doesn't seem to inherited by
# this script.
export DJANGO_SETTINGS_MODULE=pulpcore.app.settings
export PULP_SETTINGS=$PWD/.ci/ansible/settings/settings.py

export PULP_URL="https://pulp"

REPORTED_STATUS="$(pulp status)"

echo "machine pulp
login admin
password password
" | cmd_user_stdin_prefix bash -c "cat >> ~pulp/.netrc"
# Some commands like ansible-galaxy specifically require 600
cmd_prefix bash -c "chmod 600 ~pulp/.netrc"

# Generate and install binding
pushd ../pulp-openapi-generator
if pulp debug has-plugin --name "core" --specifier ">=3.44.0.dev"
then
  # Use app_label to generate api.json and package to produce the proper package name.

  if [ "$(jq -r '.domain_enabled' <<<"$REPORTED_STATUS")" = "true" ]
  then
    # Workaround: Domains are not supported by the published bindings.
    # Generate new bindings for all packages.
    for item in $(jq -r '.versions[] | tojson' <<<"$REPORTED_STATUS")
    do
      echo $item
      COMPONENT="$(jq -r '.component' <<<"$item")"
      VERSION="$(jq -r '.version' <<<"$item")"
      MODULE="$(jq -r '.module' <<<"$item")"
      PACKAGE="${MODULE%%.*}"
      curl --fail-with-body -k -o api.json "${PULP_URL}${PULP_API_ROOT}api/v3/docs/api.json?bindings&component=$COMPONENT"
      USE_LOCAL_API_JSON=1 ./generate.sh "${PACKAGE}" python "${VERSION}"
      cmd_prefix pip3 install "/root/pulp-openapi-generator/${PACKAGE}-client"
      sudo rm -rf "./${PACKAGE}-client"
    done
  else
    # Sadly: Different pulpcore-versions aren't either...
    for item in $(jq -r '.versions[]| select(.component!="core")| select(.component!="file")| select(.component!="certguard")| tojson' <<<"$REPORTED_STATUS")
    do
      echo $item
      COMPONENT="$(jq -r '.component' <<<"$item")"
      VERSION="$(jq -r '.version' <<<"$item")"
      MODULE="$(jq -r '.module' <<<"$item")"
      PACKAGE="${MODULE%%.*}"
      curl --fail-with-body -k -o api.json "${PULP_URL}${PULP_API_ROOT}api/v3/docs/api.json?bindings&component=$COMPONENT"
      USE_LOCAL_API_JSON=1 ./generate.sh "${PACKAGE}" python "${VERSION}"
      cmd_prefix pip3 install "/root/pulp-openapi-generator/${PACKAGE}-client"
      sudo rm -rf "./${PACKAGE}-client"
    done
  fi
else
  # Infer the client name from the package name by replacing "-" with "_".
  # Use the component to infer the package name on older versions of pulpcore.

  if [ "$(echo "$REPORTED_STATUS" | jq -r '.domain_enabled')" = "true" ]
  then
    # Workaround: Domains are not supported by the published bindings.
    # Generate new bindings for all packages.
    for item in $(echo "$REPORTED_STATUS" | jq -r '.versions[]|(.package // ("pulp_" + .component)|sub("pulp_core"; "pulpcore"))|sub("-"; "_")')
    do
      ./generate.sh "${item}" python
      cmd_prefix pip3 install "/root/pulp-openapi-generator/${item}-client"
      sudo rm -rf "./${item}-client"
    done
  else
    # Sadly: Different pulpcore-versions aren't either...
    for item in $(echo "$REPORTED_STATUS" | jq -r '.versions[]|select(.component!="core")|select(.component!="file")|select(.component!="certguard")|(.package // ("pulp_" + .component)|sub("pulp_core"; "pulpcore"))|sub("-"; "_")')
    do
      ./generate.sh "${item}" python
      cmd_prefix pip3 install "/root/pulp-openapi-generator/${item}-client"
      sudo rm -rf "./${item}-client"
    done
  fi
fi
popd

# At this point, this is a safeguard only, so let's not make too much fuzz about the old status format.
echo "$REPORTED_STATUS" | jq -r '.versions[]|select(.package)|(.package|sub("_"; "-")) + "-client==" + .version' > bindings_requirements.txt
cmd_stdin_prefix bash -c "cat > /tmp/unittest_requirements.txt" < unittest_requirements.txt
cmd_stdin_prefix bash -c "cat > /tmp/functest_requirements.txt" < functest_requirements.txt
cmd_stdin_prefix bash -c "cat > /tmp/bindings_requirements.txt" < bindings_requirements.txt
cmd_prefix pip3 install -r /tmp/unittest_requirements.txt -r /tmp/functest_requirements.txt -r /tmp/bindings_requirements.txt

CERTIFI=$(cmd_prefix python3 -c 'import certifi; print(certifi.where())')
cmd_prefix bash -c "cat /etc/pulp/certs/pulp_webserver.crt >> '$CERTIFI'"

# check for any uncommitted migrations
echo "Checking for uncommitted migrations..."
cmd_user_prefix bash -c "django-admin makemigrations core --check --dry-run"
cmd_user_prefix bash -c "django-admin makemigrations file --check --dry-run"
cmd_user_prefix bash -c "django-admin makemigrations certguard --check --dry-run"

if [ -f "$POST_SCRIPT" ]; then
  source "$POST_SCRIPT"
fi

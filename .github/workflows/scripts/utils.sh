# This file is meant to be sourced by ci-scripts

PULP_CI_CONTAINER=pulp

# Run a command
cmd_prefix() {
  docker exec "$PULP_CI_CONTAINER" "$@"
}

# Run a command as the limited pulp user
cmd_user_prefix() {
  docker exec -u pulp "$PULP_CI_CONTAINER" "$@"
}

# Run a command, and pass STDIN
cmd_stdin_prefix() {
  docker exec -i "$PULP_CI_CONTAINER" "$@"
}

# Run a command as the lmited pulp user, and pass STDIN
cmd_user_stdin_prefix() {
  docker exec -i -u pulp "$PULP_CI_CONTAINER" "$@"
}

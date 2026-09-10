#!/usr/bin/env bash
# Installs Julia via juliaup (the official Julia version manager/installer).

set -euo pipefail

curl -fsSL https://install.julialang.org | sh -s -- --yes

echo "Julia installation complete. Restart your shell or run 'source ~/.bashrc' to update PATH."

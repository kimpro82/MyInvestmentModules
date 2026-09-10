#!/usr/bin/env bash
# Runs a Julia script after sourcing ~/.bashrc so the juliaup PATH is available.

# Usage: ./run.sh filename.jl

set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <filename.jl>"
    exit 1
fi

source ~/.bashrc

julia --project="$(dirname "$0")" "$@"

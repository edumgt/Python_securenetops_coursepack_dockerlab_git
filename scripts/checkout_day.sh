#!/usr/bin/env bash
set -euo pipefail
DAY="${1:-day08}"
git checkout "$DAY"
echo "Checked out $DAY"

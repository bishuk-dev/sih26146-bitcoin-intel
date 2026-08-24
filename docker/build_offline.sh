#!/usr/bin/env bash
# Run this ONCE while you still have internet, well before the offline evaluation.
# It downloads every dependency as a .whl so `docker build` never touches PyPI.
set -euo pipefail

cd "$(dirname "$0")/.."

echo "Downloading wheels for offline install..."
pip download -d ./wheels -r requirements.txt

echo "Building Docker image from local wheels only..."
docker build -f docker/Dockerfile -t sih26146-bitcoin-intel .

echo "Done. Sanity-check with: docker save sih26146-bitcoin-intel -o sih26146-bitcoin-intel.tar"
echo "Then test on an air-gapped machine: docker load -i sih26146-bitcoin-intel.tar && docker run -p 8501:8501 sih26146-bitcoin-intel"

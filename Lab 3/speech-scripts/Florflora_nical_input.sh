#!/usr/bin/env bash

set -euo pipefail

VOICES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/voices"

# Ask the respondent a numerical question
python3 -m piper \
  --model en_US-lessac-medium \
  --data-dir "$VOICES_DIR" \
  --output-raw \
  -- "How many tote bags  do you have?" \
  | aplay -r 22050 -f S16_LE -t raw -

# Record the respondent's answer for 5 seconds
echo "Recording your answer..."

arecord -d 5 -f cd -c 1 -r 16000 numerical_answer.wav

echo "Recording complete."

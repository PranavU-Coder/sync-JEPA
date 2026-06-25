#!/usr/bin/env bash

set -euo pipefail

echo "downloading the base FSD50K dataset"
zenodo_get -r 4060432

echo "extracting dev_audio..."
7z x FSD50K.dev_audio.zip -y

echo "extracting eval_audio..."
7z x FSD50K.eval_audio.zip -y

echo "extracting metadata..."
7z x FSD50K.ground_truth.zip -y
7z x FSD50K.metadata.zip -y
7z x FSD50K.doc.zip -y

echo "done"

#!/bin/sh
set -eu

./run.sh --package serde --max-depth 2 --ascii-tree --output serde.png
./run.sh --package clap --max-depth 2 --ascii-tree --output clap.png
./run.sh --package rand --max-depth 2 --ascii-tree --output rand.png

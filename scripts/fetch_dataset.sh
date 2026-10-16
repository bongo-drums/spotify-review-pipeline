#!/usr/bin/env bash
# Download the course dataset ZIP from the link in the assignment and unzip it into data/raw/extracted/.
# Idempotent: skips the download when the verified CSV is already present. No API key needed.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$ROOT/data/raw"
ID="1P0rUoAS_wVjp3BYKqXMEyD4u0uJP1Bvf"
ZIP_SHA="ec5a3ddceb68df52cd935b7fb3e1286aea8432d77183fbd54f397695566d5e68"
CSV_SHA="1fc85de68a304dd8978b537cfa58793d5f41cbaf417fa32cb53899f83a2fcef6"
mkdir -p "$DEST"
if [ -f "$DEST/extracted/spotify_reviews_18months.csv" ] && \
   [ "$(sha256sum "$DEST/extracted/spotify_reviews_18months.csv" | cut -c1-64)" = "$CSV_SHA" ]; then
  echo "dataset already present and verified"; exit 0
fi
ZIP="$DEST/spotify-insight-dataset.zip"
if [ ! -f "$ZIP" ] || [ "$(sha256sum "$ZIP" | cut -c1-64)" != "$ZIP_SHA" ]; then
  echo "downloading dataset zip from Google Drive..."
  PAGE="$(mktemp)"
  curl -sSL --max-time 120 -o "$PAGE" "https://drive.google.com/uc?export=download&id=$ID"
  if file "$PAGE" | grep -qi html; then
    UUID="$(grep -oE 'name="uuid" value="[^"]+"' "$PAGE" | grep -oE 'value="[^"]+"' | cut -d'"' -f2 || true)"
    curl -sSL --max-time 600 -o "$ZIP" "https://drive.usercontent.google.com/download?id=$ID&export=download&confirm=t&uuid=$UUID"
  else
    mv "$PAGE" "$ZIP"
  fi
  rm -f "$PAGE"
  [ "$(sha256sum "$ZIP" | cut -c1-64)" = "$ZIP_SHA" ] || { echo "zip checksum mismatch" >&2; exit 1; }
fi
rm -rf "$DEST/extracted" && mkdir -p "$DEST/extracted"
unzip -q "$ZIP" -d "$DEST/extracted"
[ "$(sha256sum "$DEST/extracted/spotify_reviews_18months.csv" | cut -c1-64)" = "$CSV_SHA" ] || { echo "csv checksum mismatch" >&2; exit 1; }
echo "dataset ready in $DEST/extracted ($(ls "$DEST/extracted" | wc -l) files, csv sha256 verified)"

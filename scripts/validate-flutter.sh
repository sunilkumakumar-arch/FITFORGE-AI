#!/usr/bin/env bash
set -euo pipefail
if ! command -v flutter >/dev/null 2>&1; then
  echo "Flutter SDK is not installed. Install Flutter and rerun this script."
  exit 2
fi
cd apps/mobile
flutter pub get
flutter analyze
flutter test
flutter build apk --debug
if [[ "$(uname)" == "Darwin" ]]; then
  flutter build ios --no-codesign
else
  echo "Skipping iOS build because this is not macOS."
fi

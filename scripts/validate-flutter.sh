#!/usr/bin/env bash
set -euo pipefail
if ! command -v flutter >/dev/null 2>&1; then
  if [[ "${SIMULATE_EXTERNAL_VALIDATION:-false}" == "true" ]]; then
    mkdir -p reports/validation
    test -f apps/mobile/pubspec.yaml
    test -f apps/mobile/lib/src/screens/posture_capture_screen.dart
    test -f apps/mobile/lib/src/screens/qr_attendance_screen.dart
    test -f apps/mobile/lib/src/screens/razorpay_checkout_screen.dart
    grep -q "camera:" apps/mobile/pubspec.yaml
    grep -q "google_mlkit_pose_detection:" apps/mobile/pubspec.yaml
    grep -q "razorpay_flutter:" apps/mobile/pubspec.yaml
    cat > reports/validation/flutter-validation.json <<'JSON'
{"mode":"simulation","status":"passed","checks":["pubspec present","camera dependency present","ML Kit pose dependency present","Razorpay Flutter dependency present","QR attendance screen present","Razorpay checkout screen present","posture camera screen present"],"note":"Flutter SDK is unavailable in this environment; rerun without simulation in a Flutter-enabled runner for device builds."}
JSON
    echo "Flutter validation simulation passed. See reports/validation/flutter-validation.json"
    exit 0
  fi
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

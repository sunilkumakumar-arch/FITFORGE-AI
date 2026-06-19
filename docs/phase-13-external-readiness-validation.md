# FITFORGE AI - Phase 13 External Readiness Validation

Status: Implemented after Phase 12

This phase adds real client integration scaffolds and executable validation tooling for external production readiness.

---

## Real MediaPipe Web Integration

Files:

- `apps/admin-web/src/components/mediapipe-posture-camera.tsx`
- `apps/admin-web/src/app/(app)/posture-camera/page.tsx`

Capabilities:

- Loads MediaPipe Tasks Vision PoseLandmarker in the browser.
- Opens webcam with `navigator.mediaDevices`.
- Runs video-mode pose detection.
- Draws landmarks and connectors on canvas.
- Sends landmarks to `POST /api/v1/posture/analyze-frame`.

Run:

```bash
npm run web:build
```

Then open:

```text
/posture-camera
```

---

## Flutter Camera and Pose Integration

Updated:

- `apps/mobile/pubspec.yaml`
- `apps/mobile/lib/src/screens/posture_capture_screen.dart`

Added Flutter dependencies:

- `camera`
- `google_mlkit_pose_detection`
- `permission_handler`
- `razorpay_flutter`
- `flutter_secure_storage`
- `tflite_flutter`

Capabilities:

- Starts a camera stream.
- Runs Google ML Kit pose detection on camera frames.
- Maps pose landmarks to the backend posture payload.
- Keeps the previous demo-frame path as fallback.

Validate in a Flutter-enabled environment:

```bash
npm run mobile:validate
```

---

## Razorpay Sandbox Verification

Added:

- `scripts/verify-razorpay-sandbox.js`

Run with sandbox credentials:

```bash
RAZORPAY_KEY_ID=rzp_test_xxx RAZORPAY_KEY_SECRET=xxx npm run payments:verify:razorpay
```

The script:

- Creates a Razorpay sandbox order.
- Fetches the created order.
- Fails if Razorpay credentials or API behavior are invalid.

---

## OWASP Security Testing

Added:

- `scripts/owasp-security-check.sh`

Run:

```bash
npm run security:owasp
```

Optional ZAP baseline scan:

```bash
ZAP_TARGET_URL=https://staging.example.com npm run security:owasp
```

The script:

- Produces `reports/security/npm-audit.json`.
- Runs OWASP ZAP baseline scan when `ZAP_TARGET_URL` and Docker are available.

---

## Production Deployment Validation

Added:

- `scripts/validate-production-deployment.sh`
- `scripts/smoke-test-production.sh`
- Terraform monitoring module
- Terraform schedule module

Run local validation:

```bash
npm run deploy:validate
```

Run deployed smoke test:

```bash
API_BASE_URL=https://api.example.com/api/v1 scripts/smoke-test-production.sh
```

---

## Monitoring and Alerting

Added:

- `infrastructure/aws/terraform/modules/monitoring/main.tf`
- `infrastructure/aws/terraform/modules/schedules/main.tf`

Monitoring scaffold includes:

- SNS alerts topic.
- ALB 5xx alarm.
- ALB high latency alarm.
- EventBridge rules for reservation release, renewal scan, and daily metrics aggregation.

---

## Remaining External Dependencies

These cannot be completed inside the current container without external credentials or tooling:

- Flutter SDK validation.
- iOS build on macOS.
- Razorpay sandbox verification with real keys.
- Terraform apply against an AWS account.
- OWASP ZAP scan against a deployed staging URL.
- Production smoke test against a deployed API URL.

# FITFORGE AI Mobile

Flutter source architecture for Android and iOS member/trainer apps.

This environment does not include the Flutter SDK, so platform runner folders are represented with placeholders. Run the following locally after installing Flutter:

```bash
cd apps/mobile
flutter create --platforms=android,ios .
flutter analyze
flutter test
```

The app uses SDK-only routing and state management in this phase so the source can be reviewed without external package resolution.

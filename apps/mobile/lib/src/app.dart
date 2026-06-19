import 'package:flutter/material.dart';
import 'state/app_state.dart';
import 'screens/login_screen.dart';
import 'screens/home_screen.dart';
import 'screens/module_screen.dart';
import 'screens/qr_attendance_screen.dart';
import 'screens/razorpay_checkout_screen.dart';
import 'screens/posture_capture_screen.dart';

class FitforgeApp extends StatefulWidget { const FitforgeApp({super.key}); @override State<FitforgeApp> createState()=>_FitforgeAppState(); }
class _FitforgeAppState extends State<FitforgeApp> {
  final AppState state = AppState();
  @override Widget build(BuildContext context) => AppScope(state: state, child: MaterialApp(
    title: 'FITFORGE AI', debugShowCheckedModeBanner: false, themeMode: ThemeMode.dark,
    darkTheme: ThemeData(colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xffd4af37), brightness: Brightness.dark), useMaterial3: true),
    routes: {
      '/': (_) => const LoginScreen(),
      '/home': (_) => const HomeScreen(),
      '/qr-attendance': (_) => const QrAttendanceScreen(),
      '/razorpay-checkout': (_) => const RazorpayCheckoutScreen(),
      '/posture-capture': (_) => const PostureCaptureScreen(),
    },
    onGenerateRoute: (settings) => MaterialPageRoute(builder: (_) => ModuleScreen(title: settings.arguments as String? ?? 'Module')),
  ));
}
class AppScope extends InheritedNotifier<AppState> { const AppScope({required AppState state, required super.child, super.key}): super(notifier: state); static AppState of(BuildContext context)=>context.dependOnInheritedWidgetOfExactType<AppScope>()!.notifier!; }

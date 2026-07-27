import 'package:flutter/material.dart';

import 'core/theme/app_theme.dart';

import 'features/auth/login_screen.dart';

import 'features/members/members_screen.dart';
import 'features/trainers/trainers_screen.dart';
import 'features/memberships/membership_screen.dart';
import 'features/payments/payments_screen.dart';
import 'features/attendance/attendance_screen.dart';
import 'features/pt_packages/pt_package_screen.dart';

import 'features/dashboard/dashboard_screen.dart'
    as dashboard;

void main() {
  runApp(const FitForgeApp());
}

class FitForgeApp extends StatelessWidget {
  const FitForgeApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'FitForge',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.darkTheme,
      initialRoute: '/',
      routes: {
        '/': (context) => const LoginScreen(),

        '/dashboard': (context) =>
            const dashboard.DashboardScreen(),

        '/members': (context) =>
            const MembersScreen(),

        '/memberships': (context) =>
            const MembershipScreen(),

        '/trainers': (context) =>
            const TrainersScreen(),

        '/payments': (context) =>
            const PaymentsScreen(),

        '/attendance': (context) =>
            const AttendanceScreen(),

        '/pt-packages': (context) =>
            const PTPackageScreen(),
      },
    );
  }
}
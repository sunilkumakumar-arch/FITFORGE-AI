import 'package:flutter/material.dart';

import 'core/theme/app_theme.dart';

import 'features/auth/login_screen.dart';

import 'features/members/members_screen.dart';
import 'features/members/member_service.dart';

import 'features/trainers/trainers_screen.dart';
import 'features/trainers/trainer_service.dart';

import 'features/memberships/membership_screen.dart';
import 'features/memberships/membership_service.dart';

import 'features/payments/payments_screen.dart';
import 'features/payments/revenue_service.dart';

import 'features/attendance/attendance_screen.dart';

import 'features/pt_packages/pt_package_screen.dart';
import 'features/pt_packages/pt_package_service.dart';

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
        '/dashboard': (context) => const DashboardScreen(),
        '/members': (context) => const MembersScreen(),
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

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() =>
      _DashboardScreenState();
}

class _DashboardScreenState
    extends State<DashboardScreen> {
  int memberCount = 0;
  int trainerCount = 0;
  int membershipPlanCount = 0;
  int ptPackageCount = 0;

  double totalRevenue = 0;

  @override
  void initState() {
    super.initState();
    loadData();
  }

  Future<void> loadData() async {
    try {
      final members =
          await MemberService.getMemberCount();

      final trainers =
          await TrainerService.getTrainerCount();

      final plans =
          await MembershipService
              .getMembershipPlanCount();

      final revenue =
          await RevenueService.getRevenue();

      final ptPackages =
          await PTPackageService.getPackageCount();

      print('MEMBERS: $members');
      print('TRAINERS: $trainers');
      print('PLANS: $plans');
      print('PT PACKAGES: $ptPackages');

      if (!mounted) return;

      setState(() {
        memberCount = members;
        trainerCount = trainers;
        membershipPlanCount = plans;
        totalRevenue = revenue;
        ptPackageCount = ptPackages;
      });
    } catch (e) {
      print('DASHBOARD ERROR: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'FITFORGE',
          style: TextStyle(
            fontWeight: FontWeight.bold,
            letterSpacing: 2,
          ),
        ),
      ),
      body: RefreshIndicator(
        onRefresh: loadData,
        child: Padding(
          padding:
              const EdgeInsets.all(20),
          child: GridView.count(
            crossAxisCount: 2,
            childAspectRatio: 2.5,
            crossAxisSpacing: 20,
            mainAxisSpacing: 20,
            children: [
              GestureDetector(
                onTap: () async {
                  await Navigator.pushNamed(
                    context,
                    '/members',
                  );

                  loadData();
                },
                child: DashboardCard(
                  title: "Members",
                  value:
                      memberCount.toString(),
                  icon: Icons.people,
                ),
              ),

              GestureDetector(
                onTap: () async {
                  await Navigator.pushNamed(
                    context,
                    '/trainers',
                  );

                  loadData();
                },
                child: DashboardCard(
                  title: "Trainers",
                  value:
                      trainerCount.toString(),
                  icon:
                      Icons.fitness_center,
                ),
              ),

              GestureDetector(
                onTap: () async {
                  await Navigator.pushNamed(
                    context,
                    '/memberships',
                  );

                  loadData();
                },
                child: DashboardCard(
                  title:
                      "Membership Plans",
                  value:
                      membershipPlanCount
                          .toString(),
                  icon: Icons
                      .card_membership,
                ),
              ),

              GestureDetector(
                onTap: () async {
                  await Navigator.pushNamed(
                    context,
                    '/payments',
                  );
                },
                child: DashboardCard(
                  title: "Revenue",
                  value:
                      "₹${totalRevenue.toStringAsFixed(0)}",
                  icon:
                      Icons.currency_rupee,
                ),
              ),

              GestureDetector(
                onTap: () async {
                  await Navigator.pushNamed(
                    context,
                    '/attendance',
                  );
                },
                child: const DashboardCard(
                  title: "Attendance",
                  value: "0",
                  icon:
                      Icons.check_circle,
                ),
              ),

              GestureDetector(
                onTap: () async {
                  await Navigator.pushNamed(
                    context,
                    '/pt-packages',
                  );

                  loadData();
                },
                child: DashboardCard(
                  title: "PT Packages",
                  value:
                      ptPackageCount
                          .toString(),
                  icon:
                      Icons.workspace_premium,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class DashboardCard extends StatelessWidget {
  final String title;
  final String value;
  final IconData icon;

  const DashboardCard({
    super.key,
    required this.title,
    required this.value,
    required this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Center(
        child: Column(
          mainAxisAlignment:
              MainAxisAlignment.center,
          children: [
            Icon(
              icon,
              size: 50,
            ),
            const SizedBox(
              height: 15,
            ),
            Text(
              value,
              style:
                  const TextStyle(
                fontSize: 32,
                fontWeight:
                    FontWeight.bold,
              ),
            ),
            const SizedBox(
              height: 10,
            ),
            Text(title),
          ],
        ),
      ),
    );
  }
}
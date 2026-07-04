import 'package:flutter/material.dart';

import '../members/member_service.dart';
import '../members/members_screen.dart';

import '../memberships/membership_screen.dart';
import '../memberships/membership_service.dart';

import '../trainers/trainer_service.dart';

import '../attendance/attendance_service.dart';


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
  int attendanceCount = 0;

  @override
  void initState() {
    super.initState();
    loadDashboard();
  }

  Future<void> loadDashboard() async {
    try {
      final members =
          await MemberService.getMemberCount();

      final trainers =
          await TrainerService.getTrainerCount();

      final plans =
          await MembershipService
              .getMembershipPlanCount();
      print('BEFORE ATTENDANCE');        

      final attendance =
          await AttendanceService
              .getAttendanceCount();
      print('AFTER ATTENDANCE');
        

      print('====================');
      print('MEMBERS: $members');
      print('TRAINERS: $trainers');
      print('PLANS: $plans');
      print('ATTENDANCE: $attendance');
      print('====================');

      if (!mounted) return;

      setState(() {
        memberCount = members;
        trainerCount = trainers;
        membershipPlanCount = plans;
        attendanceCount = attendance;
      });
    } catch (e) {
      print(
        'DASHBOARD ERROR: $e',
      );
    }
  }

  Widget buildCard({
    required IconData icon,
    required String value,
    required String title,
    VoidCallback? onTap,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Card(
        elevation: 3,
        child: Center(
          child: Column(
            mainAxisAlignment:
                MainAxisAlignment.center,
            children: [
              Icon(
                icon,
                size: 60,
              ),
              const SizedBox(height: 20),
              Text(
                value,
                style: const TextStyle(
                  fontSize: 28,
                  fontWeight:
                      FontWeight.bold,
                ),
              ),
              const SizedBox(height: 10),
              Text(
                title,
                style: const TextStyle(
                  fontSize: 18,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'FITFORGE TEST',
          style: TextStyle(
            fontWeight:
                FontWeight.bold,
            letterSpacing: 2,
          ),
        ),
        centerTitle: true,
      ),
      body: RefreshIndicator(
        onRefresh: loadDashboard,
        child: Padding(
          padding:
              const EdgeInsets.all(20),
          child: GridView.count(
            crossAxisCount: 2,
            crossAxisSpacing: 20,
            mainAxisSpacing: 20,
            childAspectRatio: 1.2,
            children: [
              buildCard(
                icon: Icons.people,
                value:
                    memberCount.toString(),
                title: 'Members',
                onTap: () async {
                  await Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) =>
                          const MembersScreen(),
                    ),
                  );

                  loadDashboard();
                },
              ),

              buildCard(
                icon:
                    Icons.fitness_center,
                value:
                    trainerCount.toString(),
                title: 'Trainers',
              ),

              buildCard(
                icon:
                    Icons.card_membership,
                value:
                    membershipPlanCount
                        .toString(),
                title:
                    'Membership Plans',
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) =>
                          const MembershipScreen(),
                    ),
                  );
                },
              ),

              buildCard(
                icon:
                    Icons.currency_rupee,
                value: '₹0',
                title: 'Revenue',
              ),

              buildCard(
                icon:
                    Icons.check_circle,
                value:
                    attendanceCount
                        .toString(),
                title: 'Attendance',
              ),
            ],
          ),
        ),
      ),
    );
  }
}
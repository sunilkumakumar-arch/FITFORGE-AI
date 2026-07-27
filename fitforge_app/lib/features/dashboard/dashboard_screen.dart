import 'package:flutter/material.dart';

import '../members/members_screen.dart';
import '../memberships/membership_screen.dart';
import '../trainers/trainers_screen.dart';

import 'dashboard_model.dart';
import 'dashboard_service.dart';


class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() =>
      _DashboardScreenState();
}

class _DashboardScreenState
    extends State<DashboardScreen> {
  DashboardModel? dashboard;

  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    loadDashboard();
  }

  Future<void> loadDashboard() async {
    try {
      final data =
          await DashboardService
              .getDashboardSummary();

      if (!mounted) return;

      setState(() {
        dashboard = data;
        isLoading = false;
      });
    } catch (e) {
     debugPrint( 
        'DASHBOARD ERROR: $e',
      );

      if (!mounted) return;

      setState(() {
        isLoading = false;
      });
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
              const SizedBox(
                height: 20,
              ),
              Text(
                value,
                style: const TextStyle(
                  fontSize: 28,
                  fontWeight:
                      FontWeight.bold,
                ),
              ),
              const SizedBox(
                height: 10,
              ),
              Text(
                title,
                style: const TextStyle(
                  fontSize: 18,
                ),
                textAlign:
                    TextAlign.center,
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  Widget build(
    BuildContext context,
  ) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'FITFORGE',
          style: TextStyle(
            fontWeight:
                FontWeight.bold,
            letterSpacing: 2,
          ),
        ),
        centerTitle: true,
      ),
      body: isLoading
          ? const Center(
              child:
                  CircularProgressIndicator(),
            )
          : RefreshIndicator(
              onRefresh:
                  loadDashboard,
              child: Padding(
                padding:
                    const EdgeInsets.all(
                  20,
                ),
                child: GridView.count(
                  crossAxisCount: 2,
                  crossAxisSpacing:
                      20,
                  mainAxisSpacing:
                      20,
                  childAspectRatio:
                      1.2,
                  children: [
                    buildCard(
                      icon:
                          Icons.people,
                      value: dashboard!
                          .totalMembers
                          .toString(),
                      title:
                          'Members',
                      onTap:
                          () async {
                        await Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder:
                                (_) =>
                                    const MembersScreen(),
                          ),
                        );

                        loadDashboard();
                      },
                    ),

                    buildCard(
                      icon: Icons.fitness_center,
                      value: dashboard!
                          .totalTrainers
                          .toString(),
                      title: 'Trainers',
                      onTap: () async {
                        await Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (_) =>
                                const TrainersScreen(),
                          ),
                        );

                        loadDashboard();
                      },
                    ),

                    buildCard(
                      icon: Icons
                          .card_membership,
                      value: dashboard!
                          .activeMemberships
                          .toString(),
                      title:
                          'Active Memberships',
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder:
                                (_) =>
                                    const MembershipScreen(),
                          ),
                        );
                      },
                    ),

                    buildCard(
                      icon: Icons
                          .currency_rupee,
                      value:
                          '₹${dashboard!.totalRevenue.toStringAsFixed(0)}',
                      title:
                          'Revenue',
                    ),

                    buildCard(
                      icon: Icons
                          .check_circle,
                      value: dashboard!
                          .todayAttendance
                          .toString(),
                      title:
                          'Attendance',
                    ),

                    buildCard(
                      icon: Icons
                          .payments,
                      value: dashboard!
                          .totalPayments
                          .toString(),
                      title:
                          'Payments',
                    ),

                    buildCard(
                      icon: Icons
                          .pending_actions,
                      value: dashboard!
                          .pendingPayments
                          .toString(),
                      title:
                          'Pending Payments',
                    ),

                    buildCard(
                      icon: Icons
                          .event_busy,
                      value: dashboard!
                          .expiredMemberships
                          .toString(),
                      title:
                          'Expired Memberships',
                    ),
                  ],
                ),
              ),
            ),
    );
  }
}
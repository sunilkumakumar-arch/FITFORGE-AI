import 'package:flutter/material.dart';

import 'trainer_service.dart';
import 'trainers_screen.dart';
import 'add_trainer_screen.dart';

class TrainerDashboardScreen extends StatefulWidget {
  const TrainerDashboardScreen({super.key});

  @override
  State<TrainerDashboardScreen> createState() =>
      _TrainerDashboardScreenState();
}

class _TrainerDashboardScreenState
    extends State<TrainerDashboardScreen> {
  Map<String, dynamic>? dashboard;

  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    loadDashboard();
  }

  Future<void> loadDashboard() async {
    try {
      final data =
          await TrainerService.getDashboardSummary();

      if (!mounted) return;

      setState(() {
        dashboard = data;
        isLoading = false;
      });
    } catch (e) {
      debugPrint("Trainer Dashboard Error: $e");

      if (!mounted) return;

      setState(() {
        isLoading = false;
      });
    }
  }

  Widget buildActionButton({
    required IconData icon,
    required String title,
    required VoidCallback onTap,
  }) {
    return SizedBox(
      width: double.infinity,
      height: 55,
      child: ElevatedButton.icon(
        onPressed: onTap,
        icon: Icon(icon),
        label: Text(
          title,
          style: const TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
    );
  }

  Widget buildCard({
    required IconData icon,
    required String title,
    required String value,
  }) {
    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Column(
          mainAxisAlignment:
              MainAxisAlignment.center,
          children: [
            Icon(
              icon,
              size: 42,
            ),
            const SizedBox(height: 12),
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
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          "Trainer Dashboard",
        ),
        centerTitle: true,
      ),
      body: isLoading
          ? const Center(
              child:
                  CircularProgressIndicator(),
            )
          : RefreshIndicator(
              onRefresh: loadDashboard,
              child: Padding(
                padding:
                    const EdgeInsets.all(16),
                child: SingleChildScrollView(
                  physics:
                      const AlwaysScrollableScrollPhysics(),
                  child: Column(
                    crossAxisAlignment:
                        CrossAxisAlignment.start,
                    children: [
                      GridView.count(
                        shrinkWrap: true,
                        physics:
                            const NeverScrollableScrollPhysics(),
                        crossAxisCount: 2,
                        crossAxisSpacing: 16,
                        mainAxisSpacing: 16,
                        childAspectRatio: 1.15,
                        children: [
                          buildCard(
                            icon: Icons.people,
                            title:
                                "Total Trainers",
                            value: dashboard![
                                    "total_trainers"]
                                .toString(),
                          ),
                          buildCard(
                            icon: Icons.check_circle,
                            title:
                                "Active Trainers",
                            value: dashboard![
                                    "active_trainers"]
                                .toString(),
                          ),
                          buildCard(
                            icon: Icons.cancel,
                            title:
                                "Inactive Trainers",
                            value: dashboard![
                                    "inactive_trainers"]
                                .toString(),
                          ),
                          buildCard(
                            icon: Icons.groups,
                            title:
                                "PT Clients",
                            value: dashboard![
                                    "pt_clients"]
                                .toString(),
                          ),
                          buildCard(
                            icon:
                                Icons.fitness_center,
                            title:
                                "Total Capacity",
                            value: dashboard![
                                    "total_capacity"]
                                .toString(),
                          ),
                          buildCard(
                            icon:
                                Icons.person_add,
                            title:
                                "Occupied Capacity",
                            value: dashboard![
                                    "occupied_capacity"]
                                .toString(),
                          ),
                          buildCard(
                            icon:
                                Icons.event_available,
                            title:
                                "Available Capacity",
                            value: dashboard![
                                    "available_capacity"]
                                .toString(),
                          ),
                        ],
                      ),

                      const SizedBox(height: 30),

                      const Text(
                        "Quick Actions",
                        style: TextStyle(
                          fontSize: 22,
                          fontWeight:
                              FontWeight.bold,
                        ),
                      ),

                      const SizedBox(height: 20),

                      buildActionButton(
                        icon: Icons.people,
                        title:
                            "View All Trainers",
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

                      const SizedBox(height: 15),

                      buildActionButton(
                        icon: Icons.person_add,
                        title:
                            "Add New Trainer",
                        onTap: () async {
                          final result =
                              await Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) =>
                                  const AddTrainerScreen(),
                            ),
                          );

                          if (result == true) {
                            loadDashboard();
                          }
                        },
                      ),

                      const SizedBox(height: 30),
                    ],
                  ),
                ),
              ),
            ),
    );
  }
}
import 'package:flutter/material.dart';

import 'membership_service.dart';
import 'add_membership_plan_screen.dart';
import 'edit_membership_plan_screen.dart';

class MembershipScreen extends StatefulWidget {
  const MembershipScreen({super.key});

  @override
  State<MembershipScreen> createState() =>
      _MembershipScreenState();
}

class _MembershipScreenState
    extends State<MembershipScreen> {
  bool isLoading = true;

  List<dynamic> membershipPlans = [];

  String? errorMessage;

  @override
  void initState() {
    super.initState();
    loadMembershipPlans();
  }

  Future<void> loadMembershipPlans() async {
    setState(() {
      isLoading = true;
      errorMessage = null;
    });

    try {
      final plans =
          await MembershipService.getMembershipPlans();

      if (!mounted) return;

      setState(() {
        membershipPlans = plans;
        isLoading = false;
      });
    } catch (e) {
      if (!mounted) return;

      setState(() {
        errorMessage =
            'Failed to load membership plans';
        isLoading = false;
      });
    }
  }

  Future<void> openAddPlanScreen() async {
    final result = await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) =>
            const AddMembershipPlanScreen(),
      ),
    );

    if (result == true) {
      loadMembershipPlans();
    }
  }

  Future<void> openEditPlanScreen(
    Map<String, dynamic> plan,
  ) async {
    final result = await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) =>
            EditMembershipPlanScreen(
          plan: plan,
        ),
      ),
    );

    if (result == true) {
      loadMembershipPlans();
    }
  }

  Future<void> deactivatePlan(
    Map<String, dynamic> plan,
  ) async {
    final confirmed =
        await showDialog<bool>(
      context: context,
      builder: (context) {
        return AlertDialog(
          title:
              const Text('Deactivate Plan'),
          content: Text(
            'Are you sure you want to deactivate "${plan['name']}"?',
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.pop(
                  context,
                  false,
                );
              },
              child: const Text('Cancel'),
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.pop(
                  context,
                  true,
                );
              },
              child: const Text(
                'Deactivate',
              ),
            ),
          ],
        );
      },
    );

    if (confirmed != true) {
      return;
    }

    final success =
        await MembershipService
            .deactivateMembershipPlan(
      plan['id'],
    );

    if (!mounted) return;

    if (success) {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        SnackBar(
          content: Text(
            '${plan['name']} deactivated',
          ),
        ),
      );

      loadMembershipPlans();
    } else {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
            'Failed to deactivate plan',
          ),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Membership Plans',
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.add),
            onPressed: openAddPlanScreen,
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: loadMembershipPlans,
        child: _buildBody(),
      ),
    );
  }

  Widget _buildBody() {
    if (isLoading) {
      return const Center(
        child: CircularProgressIndicator(),
      );
    }

    if (errorMessage != null) {
      return Center(
        child: Column(
          mainAxisAlignment:
              MainAxisAlignment.center,
          children: [
            Text(errorMessage!),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed:
                  loadMembershipPlans,
              child: const Text(
                'Retry',
              ),
            ),
          ],
        ),
      );
    }

    if (membershipPlans.isEmpty) {
      return const Center(
        child: Text(
          'No membership plans found',
        ),
      );
    }

    return ListView.builder(
      physics:
          const AlwaysScrollableScrollPhysics(),
      itemCount:
          membershipPlans.length,
      itemBuilder: (
        context,
        index,
      ) {
        final plan =
            membershipPlans[index];

        return Card(
          margin:
              const EdgeInsets.symmetric(
            horizontal: 12,
            vertical: 6,
          ),
          child: ListTile(
            leading: const Icon(
              Icons.card_membership,
            ),
            title: Text(
              plan['name'] ?? '',
            ),
            subtitle: Column(
              crossAxisAlignment:
                  CrossAxisAlignment.start,
              children: [
                Text(
                  'Duration: ${plan['duration_days'] ?? 0} Days',
                ),
                if ((plan['description'] ?? '')
                    .toString()
                    .isNotEmpty)
                  Text(
                    plan['description'],
                  ),
              ],
            ),
            trailing: Row(
              mainAxisSize:
                  MainAxisSize.min,
              children: [
                Text(
                  '₹${plan['price'] ?? 0}',
                  style: const TextStyle(
                    fontWeight:
                        FontWeight.bold,
                    fontSize: 16,
                  ),
                ),
                PopupMenuButton<String>(
                  onSelected: (value) {
                    if (value == 'edit') {
                      openEditPlanScreen(
                        plan,
                      );
                    }

                    if (value ==
                        'deactivate') {
                      deactivatePlan(
                        plan,
                      );
                    }
                  },
                  itemBuilder: (context) => [
                    const PopupMenuItem(
                      value: 'edit',
                      child: Text('Edit'),
                    ),
                    const PopupMenuItem(
                      value:
                          'deactivate',
                      child:
                          Text('Deactivate'),
                    ),
                  ],
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}
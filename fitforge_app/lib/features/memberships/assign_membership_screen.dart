import 'package:flutter/material.dart';

import 'membership_service.dart';
import '../trainers/membership_trainer_assignment_screen.dart';

class AssignMembershipScreen extends StatefulWidget {
  final Map<String, dynamic> member;

  const AssignMembershipScreen({
    super.key,
    required this.member,
  });

  @override
  State<AssignMembershipScreen> createState() =>
      _AssignMembershipScreenState();
}

class _AssignMembershipScreenState
    extends State<AssignMembershipScreen> {
  List<dynamic> plans = [];

  dynamic selectedPlan;

  bool isLoading = true;

  bool isSaving = false;

  @override
  void initState() {
    super.initState();
    loadPlans();
  }

  Future<void> loadPlans() async {
    final data =
        await MembershipService.getMembershipPlans();

    setState(() {
      plans = data;

      if (plans.isNotEmpty) {
        selectedPlan = plans.first;
      }

      isLoading = false;
    });
  }

  Future<void> saveMembership() async {
    if (selectedPlan == null) {
      return;
    }

    setState(() {
      isSaving = true;
    });

    final success =
        await MembershipService.assignMembership(
      memberId: widget.member['id'],
      planId: selectedPlan['id'],
      startDate:
          DateTime.now().toString().split(' ')[0],
      amountPaid: double.parse(
        selectedPlan['price'].toString(),
      ),
    );

    if (!mounted) return;

    setState(() {
      isSaving = false;
    });

    if (success) {
      final trainerAssigned =
          await Navigator.push(
        context,
        MaterialPageRoute(
          builder: (_) =>
              MembershipTrainerAssignmentScreen(
            member: widget.member,
          ),
        ),
      );

      if (!mounted) return;

      if (trainerAssigned == true) {
        ScaffoldMessenger.of(context)
            .showSnackBar(
          const SnackBar(
            content: Text(
              'Membership & Trainer Assigned Successfully',
            ),
          ),
        );

        Navigator.pop(
          context,
          true,
        );
      }
    } else {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
            'Failed To Assign Membership',
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
          'Assign Membership',
        ),
      ),
      body: isLoading
          ? const Center(
              child: CircularProgressIndicator(),
            )
          : Padding(
              padding:
                  const EdgeInsets.all(20),
              child: Column(
                children: [
                  Card(
                    child: ListTile(
                      title: Text(
                        '${widget.member['first_name']} ${widget.member['last_name']}',
                      ),
                      subtitle: Text(
                        widget.member['email'] ?? '',
                      ),
                    ),
                  ),

                  const SizedBox(height: 20),

                  DropdownButtonFormField<dynamic>(
                    value: selectedPlan,
                    decoration:
                        const InputDecoration(
                      labelText:
                          'Membership Plan',
                      border:
                          OutlineInputBorder(),
                    ),
                    items: plans.map((plan) {
                      return DropdownMenuItem(
                        value: plan,
                        child: Text(
                          '${plan['name']} - ₹${plan['price']}',
                        ),
                      );
                    }).toList(),
                    onChanged: (value) {
                      setState(() {
                        selectedPlan = value;
                      });
                    },
                  ),

                  const SizedBox(height: 20),

                  if (selectedPlan != null)
                    Card(
                      child: ListTile(
                        title: Text(
                          selectedPlan['name'],
                        ),
                        subtitle: Text(
                          'Duration: ${selectedPlan['duration_days']} Days',
                        ),
                        trailing: Text(
                          '₹${selectedPlan['price']}',
                        ),
                      ),
                    ),

                  const Spacer(),

                  SizedBox(
                    width: double.infinity,
                    height: 50,
                    child: ElevatedButton(
                      onPressed: isSaving
                          ? null
                          : saveMembership,
                      child: isSaving
                          ? const CircularProgressIndicator()
                          : const Text(
                              'ASSIGN MEMBERSHIP',
                            ),
                    ),
                  ),
                ],
              ),
            ),
    );
  }
}
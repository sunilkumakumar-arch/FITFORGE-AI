import 'package:flutter/material.dart';

import 'edit_member_screen.dart';
import 'member_service.dart';

import '../memberships/assign_membership_screen.dart';
import '../memberships/membership_service.dart';

import '../trainers/trainer_assignment_service.dart';

class MemberDetailsScreen extends StatefulWidget {
  final Map<String, dynamic> member;

  const MemberDetailsScreen({
    super.key,
    required this.member,
  });

  @override
  State<MemberDetailsScreen> createState() =>
      _MemberDetailsScreenState();
}

class _MemberDetailsScreenState
    extends State<MemberDetailsScreen> {
  Map<String, dynamic>? membership;

  Map<String, dynamic>? trainerAssignment;

  bool isLoadingMembership = true;

  bool isLoadingTrainer = true;

  @override
  void initState() {
    super.initState();

    loadMembership();
    loadTrainer();
  }

  Future<void> loadMembership() async {
    final data =
        await MembershipService
            .getMemberMembership(
      widget.member['id'],
    );

    if (!mounted) return;

    setState(() {
      membership = data;
      isLoadingMembership = false;
    });
  }

  Future<void> loadTrainer() async {
    final data =
        await TrainerAssignmentService
            .getMemberTrainer(
      widget.member['id'],
    );

    if (!mounted) return;

    setState(() {
      trainerAssignment = data;
      isLoadingTrainer = false;
    });
  }

  Future<void> deleteMember() async {
    final confirm =
        await showDialog<bool>(
      context: context,
      builder: (context) {
        return AlertDialog(
          title:
              const Text('Delete Member'),
          content: Text(
            'Are you sure you want to delete\n\n${widget.member['first_name']} ${widget.member['last_name']}?',
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.pop(
                  context,
                  false,
                );
              },
              child:
                  const Text('Cancel'),
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.pop(
                  context,
                  true,
                );
              },
              child:
                  const Text('Delete'),
            ),
          ],
        );
      },
    );

    if (confirm != true) return;

    final success =
        await MemberService.deleteMember(
      widget.member['id'],
    );

    if (!mounted) return;

    if (success) {
      Navigator.pop(context, true);
    }
  }

  Widget buildInfoTile(
    String title,
    String value,
  ) {
    return Card(
      margin:
          const EdgeInsets.symmetric(
        vertical: 6,
      ),
      child: ListTile(
        title: Text(title),
        subtitle: Text(value),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title:
            const Text('Member Profile'),
      ),
      body: SingleChildScrollView(
        padding:
            const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment:
              CrossAxisAlignment.start,
          children: [
            Center(
              child: CircleAvatar(
                radius: 50,
                child: Text(
                  widget.member[
                              'first_name']
                          ?.toString()
                          .substring(
                            0,
                            1,
                          )
                          .toUpperCase() ??
                      '?',
                  style:
                      const TextStyle(
                    fontSize: 30,
                    fontWeight:
                        FontWeight.bold,
                  ),
                ),
              ),
            ),

            const SizedBox(height: 30),

            buildInfoTile(
              'Member ID',
              widget.member['id']
                      ?.toString() ??
                  '',
            ),

            buildInfoTile(
              'Name',
              '${widget.member['first_name']} ${widget.member['last_name']}',
            ),

            buildInfoTile(
              'Phone',
              widget.member['phone'] ?? '',
            ),

            buildInfoTile(
              'Email',
              widget.member['email'] ?? '',
            ),

            buildInfoTile(
              'Gender',
              widget.member['gender'] ?? '',
            ),

            buildInfoTile(
              'Date Of Birth',
              widget.member[
                      'date_of_birth'] ??
                  '',
            ),

            buildInfoTile(
              'Joining Date',
              widget.member[
                      'joining_date'] ??
                  '',
            ),

            if (isLoadingMembership)
              const Center(
                child:
                    CircularProgressIndicator(),
              )
            else ...[
              buildInfoTile(
                'Membership Plan',
                membership?[
                        'plan_name'] ??
                    'Not Assigned',
              ),

              buildInfoTile(
                'Status',
                membership?['status'] ??
                    'No Active Membership',
              ),

              buildInfoTile(
                'Remaining Days',
                membership?[
                            'remaining_days']
                        ?.toString() ??
                    '-',
              ),

              buildInfoTile(
                'Expiry Date',
                membership?[
                        'end_date'] ??
                    '-',
              ),
            ],

            if (isLoadingTrainer)
              const Center(
                child:
                    CircularProgressIndicator(),
              )
            else
              buildInfoTile(
                'Assigned Trainer',
                trainerAssignment?[
                        'trainer_name'] ??
                    'Not Assigned',
              ),

            const SizedBox(height: 30),

            SizedBox(
              width: double.infinity,
              child:
                  ElevatedButton.icon(
                onPressed: () async {
                  final result =
                      await Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) =>
                          AssignMembershipScreen(
                        member:
                            widget.member,
                      ),
                    ),
                  );

                  if (result == true) {
                    loadMembership();
                  }
                },
                icon: const Icon(
                  Icons.card_membership,
                ),
                label: const Text(
                  'ASSIGN MEMBERSHIP',
                ),
              ),
            ),

            const SizedBox(height: 15),

            SizedBox(
              width: double.infinity,
              child:
                  ElevatedButton.icon(
                onPressed: () async {
                  await Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) =>
                          EditMemberScreen(
                        member:
                            widget.member,
                      ),
                    ),
                  );
                },
                icon:
                    const Icon(Icons.edit),
                label: const Text(
                  'EDIT MEMBER',
                ),
              ),
            ),

            const SizedBox(height: 15),

            SizedBox(
              width: double.infinity,
              child:
                  ElevatedButton.icon(
                onPressed: deleteMember,
                icon:
                    const Icon(Icons.delete),
                label: const Text(
                  'DELETE MEMBER',
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
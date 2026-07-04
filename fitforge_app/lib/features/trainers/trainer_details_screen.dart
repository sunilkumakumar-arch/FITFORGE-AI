import 'package:flutter/material.dart';

import 'trainer_service.dart';
import 'edit_trainer_screen.dart';
import 'assign_member_screen.dart';
import 'trainer_assignment_service.dart';

class TrainerDetailsScreen extends StatefulWidget {
  final Map<String, dynamic> trainer;

  const TrainerDetailsScreen({
    super.key,
    required this.trainer,
  });

  @override
  State<TrainerDetailsScreen> createState() =>
      _TrainerDetailsScreenState();
}

class _TrainerDetailsScreenState
    extends State<TrainerDetailsScreen> {
  List<dynamic> assignments = [];

  @override
  void initState() {
    super.initState();
    loadAssignments();
  }

  Future<void> loadAssignments() async {
    final data =
        await TrainerAssignmentService
            .getTrainerAssignments(
      widget.trainer['id'],
    );

    if (!mounted) return;

    setState(() {
      assignments = data;
    });
  }

  Future<void> deleteTrainer() async {
    final confirm =
        await showDialog<bool>(
      context: context,
      builder: (context) {
        return AlertDialog(
          title:
              const Text('Delete Trainer'),
          content: Text(
            'Delete ${widget.trainer['first_name']} ${widget.trainer['last_name']}?',
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
        await TrainerService.deleteTrainer(
      widget.trainer['id'],
    );

    if (!mounted) return;

    if (success) {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content:
              Text('Trainer Deleted'),
        ),
      );

      Navigator.pop(
        context,
        true,
      );
    }
  }

  Widget infoTile(
    String title,
    String value,
  ) {
    return Card(
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
        title: const Text(
          'Trainer Profile',
        ),
      ),
      body: SingleChildScrollView(
        padding:
            const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment:
              CrossAxisAlignment.start,
          children: [
            infoTile(
              'Trainer Code',
              widget.trainer[
                      'trainer_code'] ??
                  '',
            ),

            infoTile(
              'Name',
              '${widget.trainer['first_name']} ${widget.trainer['last_name']}',
            ),

            infoTile(
              'Phone',
              widget.trainer['phone'] ??
                  '',
            ),

            infoTile(
              'Email',
              widget.trainer['email'] ??
                  '',
            ),

            infoTile(
              'Specialization',
              widget.trainer[
                      'specialization'] ??
                  '',
            ),

            infoTile(
              'Experience',
              widget.trainer[
                          'experience_years']
                      ?.toString() ??
                  '',
            ),

            const SizedBox(
              height: 20,
            ),

            const Text(
              'Assigned Members',
              style: TextStyle(
                fontSize: 20,
                fontWeight:
                    FontWeight.bold,
              ),
            ),

            const SizedBox(
              height: 10,
            ),

            if (assignments.isEmpty)
              const Card(
                child: ListTile(
                  title: Text(
                    'No Members Assigned',
                  ),
                ),
              ),

            ...assignments.map(
              (assignment) => Card(
                child: ListTile(
                  leading: const Icon(
                    Icons.person,
                  ),
                  title: Text(
                    assignment[
                            'member_name'] ??
                        'Member',
                  ),
                ),
              ),
            ),

            const SizedBox(
              height: 20,
            ),

            SizedBox(
              width:
                  double.infinity,
              child:
                  ElevatedButton.icon(
                onPressed: () async {
                  final result =
                      await Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) =>
                          EditTrainerScreen(
                        trainer:
                            widget.trainer,
                      ),
                    ),
                  );

                  if (result ==
                          true &&
                      mounted) {
                    Navigator.pop(
                      context,
                      true,
                    );
                  }
                },
                icon:
                    const Icon(Icons.edit),
                label: const Text(
                  'EDIT TRAINER',
                ),
              ),
            ),

            const SizedBox(
              height: 10,
            ),

            SizedBox(
              width:
                  double.infinity,
              child:
                  ElevatedButton.icon(
                onPressed: () async {
                  final result =
                      await Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) =>
                          AssignMemberScreen(
                        trainer:
                            widget.trainer,
                      ),
                    ),
                  );

                  if (result ==
                      true) {
                    await loadAssignments();

                    if (!mounted)
                      return;

                    ScaffoldMessenger.of(
                            context)
                        .showSnackBar(
                      const SnackBar(
                        content: Text(
                          'Member Assigned',
                        ),
                      ),
                    );
                  }
                },
                icon: const Icon(
                  Icons.person_add,
                ),
                label: const Text(
                  'ASSIGN MEMBER',
                ),
              ),
            ),

            const SizedBox(
              height: 10,
            ),

            SizedBox(
              width:
                  double.infinity,
              child:
                  ElevatedButton.icon(
                onPressed:
                    deleteTrainer,
                icon: const Icon(
                  Icons.delete,
                ),
                label: const Text(
                  'DELETE TRAINER',
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
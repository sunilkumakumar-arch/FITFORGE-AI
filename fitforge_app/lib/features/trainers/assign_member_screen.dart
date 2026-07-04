import 'package:flutter/material.dart';

import '../members/member_service.dart';
import 'trainer_assignment_service.dart';

class AssignMemberScreen extends StatefulWidget {
  final Map<String, dynamic> trainer;

  const AssignMemberScreen({
    super.key,
    required this.trainer,
  });

  @override
  State<AssignMemberScreen> createState() =>
      _AssignMemberScreenState();
}

class _AssignMemberScreenState
    extends State<AssignMemberScreen> {
  List<dynamic> members = [];

  int? selectedMemberId;

  bool isLoading = true;
  bool isSaving = false;

  @override
  void initState() {
    super.initState();
    loadMembers();
  }

  Future<void> loadMembers() async {
    final data =
        await MemberService.getMembers();

    if (!mounted) return;

    setState(() {
      members = data;
      isLoading = false;
    });
  }

  Future<void> assignMember() async {
    if (selectedMemberId == null) {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
            'Please Select Member',
          ),
        ),
      );
      return;
    }

    setState(() {
      isSaving = true;
    });

    final success =
        await TrainerAssignmentService
            .assignMember(
      trainerId: widget.trainer['id'],
      memberId: selectedMemberId!,
    );

    if (!mounted) return;

    setState(() {
      isSaving = false;
    });

    if (success) {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
            'Member Assigned Successfully',
          ),
        ),
      );

      Navigator.pop(
        context,
        true,
      );
    } else {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
            'Assignment Failed',
          ),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title:
            const Text('Assign Member'),
      ),
      body: isLoading
          ? const Center(
              child:
                  CircularProgressIndicator(),
            )
          : Padding(
              padding:
                  const EdgeInsets.all(20),
              child: Column(
                children: [
                  DropdownButtonFormField<int>(
                    value:
                        selectedMemberId,
                    decoration:
                        const InputDecoration(
                      labelText:
                          'Select Member',
                      border:
                          OutlineInputBorder(),
                    ),
                    items: members.map((member) {
                      return DropdownMenuItem<int>(
                        value:
                            member['id'],
                        child: Text(
                          '${member['first_name']} ${member['last_name']}',
                        ),
                      );
                    }).toList(),
                    onChanged: (value) {
                      setState(() {
                        selectedMemberId =
                            value;
                      });
                    },
                  ),

                  const SizedBox(
                    height: 20,
                  ),

                  SizedBox(
                    width:
                        double.infinity,
                    height: 50,
                    child:
                        ElevatedButton(
                      onPressed:
                          isSaving
                              ? null
                              : assignMember,
                      child: isSaving
                          ? const CircularProgressIndicator()
                          : const Text(
                              'ASSIGN MEMBER',
                            ),
                    ),
                  ),
                ],
              ),
            ),
    );
  }
}
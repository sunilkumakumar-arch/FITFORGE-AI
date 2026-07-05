import 'package:flutter/material.dart';

import '../trainers/trainer_assignment_service.dart';
import 'pt_package_service.dart';
import 'member_pt_package_service.dart';

class AssignPTPackageScreen extends StatefulWidget {
  const AssignPTPackageScreen({
    super.key,
  });

  @override
  State<AssignPTPackageScreen> createState() =>
      _AssignPTPackageScreenState();
}

class _AssignPTPackageScreenState
    extends State<AssignPTPackageScreen> {
  List<dynamic> assignments = [];

  List<dynamic> packages = [];

  int? selectedAssignmentId;
  int? selectedPackageId;

  bool isLoading = true;
  bool isSaving = false;

  @override
  void initState() {
    super.initState();
    loadData();
  }

  Future<void> loadData() async {
    final assignmentData =
        await TrainerAssignmentService
            .getAssignments();

    final packageData =
        await PTPackageService.getPackages();

    if (!mounted) return;

    setState(() {
      assignments = assignmentData;
      packages = packageData
          .where(
            (package) =>
                package['is_active'] == true,
          )
          .toList();
      isLoading = false;
    });
  }

  Future<void> assignPackage() async {
    if (selectedAssignmentId == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text(
            'Select Trainer Assignment',
          ),
        ),
      );
      return;
    }

    if (selectedPackageId == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text(
            'Select PT Package',
          ),
        ),
      );
      return;
    }

    final assignment =
        assignments.firstWhere(
      (item) =>
          item['id'] ==
          selectedAssignmentId,
    );

    final package =
        packages.firstWhere(
      (item) =>
          item['id'] ==
          selectedPackageId,
    );

    final validityDays =
        package['validity_days'] ?? 30;

    final purchaseDate =
        DateTime.now();

    final expiryDate =
        purchaseDate.add(
      Duration(
        days: validityDays,
      ),
    );

    setState(() {
      isSaving = true;
    });

    final success =
        await MemberPTPackageService
            .assignPackage(
      memberId: assignment['member'],
      trainerAssignmentId:
          selectedAssignmentId!,
      packageId: selectedPackageId!,
      purchaseDate:
          purchaseDate
              .toIso8601String()
              .split('T')[0],
      expiryDate:
          expiryDate
              .toIso8601String()
              .split('T')[0],
    );

    if (!mounted) return;

    setState(() {
      isSaving = false;
    });

    if (success) {
      Navigator.pop(
        context,
        true,
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text(
            'Assignment Failed',
          ),
        ),
      );
    }
  }

  @override
  Widget build(
    BuildContext context,
  ) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Assign PT Package',
        ),
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
                        selectedAssignmentId,
                    decoration:
                        const InputDecoration(
                      labelText:
                          'Trainer Assignment',
                      border:
                          OutlineInputBorder(),
                    ),
                    items:
                        assignments.map(
                      (assignment) {
                        return DropdownMenuItem<int>(
                          value:
                              assignment['id'],
                          child: Text(
                            '${assignment['member_name']} → ${assignment['trainer_name']}',
                          ),
                        );
                      },
                    ).toList(),
                    onChanged: (value) {
                      setState(() {
                        selectedAssignmentId =
                            value;
                      });
                    },
                  ),
                  const SizedBox(
                    height: 20,
                  ),
                  DropdownButtonFormField<int>(
                    value:
                        selectedPackageId,
                    decoration:
                        const InputDecoration(
                      labelText:
                          'PT Package',
                      border:
                          OutlineInputBorder(),
                    ),
                    items: packages.map(
                      (package) {
                        return DropdownMenuItem<int>(
                          value:
                              package['id'],
                          child: Text(
                            '${package['name']} (${package['total_sessions']} Sessions)',
                          ),
                        );
                      },
                    ).toList(),
                    onChanged: (value) {
                      setState(() {
                        selectedPackageId =
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
                              : assignPackage,
                      child: isSaving
                          ? const CircularProgressIndicator()
                          : const Text(
                              'ASSIGN PT PACKAGE',
                            ),
                    ),
                  ),
                ],
              ),
            ),
    );
  }
}
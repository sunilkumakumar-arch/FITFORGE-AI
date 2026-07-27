import 'package:flutter/material.dart';

import '../trainers/trainer_assignment_service.dart';
import 'pt_package_service.dart';
import 'member_pt_package_service.dart';

class PurchasePTPackageScreen extends StatefulWidget {
  final Map<String, dynamic> member;

  const PurchasePTPackageScreen({
    super.key,
    required this.member,
  });

  @override
  State<PurchasePTPackageScreen> createState() =>
      _PurchasePTPackageScreenState();
}

class _PurchasePTPackageScreenState
    extends State<PurchasePTPackageScreen> {
  List<dynamic> packages = [];

  dynamic selectedPackage;

  Map<String, dynamic>? trainerAssignment;

  String trainerChoice =
      'CONTINUE_SAME';

  String selectedGoal =
      'GENERAL_FITNESS';

  String selectedTrainerLevel =
      'LEVEL_1';

  String selectedSlot =
      '06:00:00';

  List<dynamic> availableTrainers =
      [];

  dynamic selectedTrainer;

  bool isLoading = true;

  bool isSaving = false;

  @override
  void initState() {
    super.initState();
    loadData();
  }

  Future<void> loadData() async {
    try {
      final packageData =
          await PTPackageService.getPackages();

      final assignment =
          await TrainerAssignmentService
              .getMemberTrainer(
        widget.member['id'],
      );

      if (!mounted) return;

      setState(() {
        packages = packageData
            .where(
              (package) =>
                  package['is_active'] == true,
            )
            .toList();

        trainerAssignment = assignment;

        isLoading = false;
      });
    } catch (e) {
      if (!mounted) return;

      setState(() {
        isLoading = false;
      });
    }
  }

  Future<void> loadAvailableTrainers() async {

  final trainers =
      await TrainerAssignmentService
          .getAvailableTrainers(
    goalType: selectedGoal,
    slotTime: selectedSlot,
    trainerLevel:
        selectedTrainerLevel,
  );

  if (!mounted) return;

  setState(() {
    availableTrainers =
        trainers;
  });

  ScaffoldMessenger.of(context)
      .showSnackBar(
    SnackBar(
      content: Text(
        '${trainers.length} trainers found',
      ),
    ),
  );
}

  Future<void> purchasePackage() async {
    if (selectedPackage == null) {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content:
              Text('Select PT Package'),
        ),
      );
      return;
    }

    if (trainerAssignment == null) {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
            'No Trainer Assigned To This Member',
          ),
        ),
      );
      return;
    }

    final purchaseDate =
        DateTime.now();

    final expiryDate =
        purchaseDate.add(
      Duration(
        days:
            selectedPackage[
                    'validity_days'] ??
                30,
      ),
    );

    setState(() {
      isSaving = true;
    });

    int trainerAssignmentId =
        trainerAssignment!['id'];

    if (
        trainerChoice ==
             'CHANGE_TRAINER' &&
        selectedTrainer != null) {

      final newAssignmentId =
          await TrainerAssignmentService
              .changeTrainer(
         memberId:
             widget.member['id'],
         trainerId:
             selectedTrainer['id'],
         goalType:
             selectedGoal,
         slotTime:
             selectedSlot,
      );
        
   
      if (newAssignmentId == null) {

        setState(() {
          isSaving = false;
        });

        ScaffoldMessenger.of(context)
             .showSnackBar(
           const SnackBar(
             content: Text(
               'Failed to change trainer',
              ),
            ),
          );

          return;
      }

      trainerAssignmentId =
          newAssignmentId;
    }

    final success =
        await MemberPTPackageService
            .assignPackage(
  
      memberId:
          widget.member['id'],
      trainerAssignmentId:
          trainerAssignment!['id'],
      packageId:
          selectedPackage['id'],
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
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
            'PT Package Purchased Successfully',
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
          content:
              Text('Purchase Failed'),
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
          'Purchase PT Package',
        ),
      ),
      body: isLoading
          ? const Center(
              child:
                  CircularProgressIndicator(),
            )
          : Padding(
              padding:
                  const EdgeInsets.all(
                20,
              ),
              child: Column(
                children: [
                  Card(
                    child: ListTile(
                      leading: const Icon(
                        Icons.person,
                      ),
                      title: Text(
                        '${widget.member['first_name']} ${widget.member['last_name']}',
                      ),
                      subtitle: Column(
                        crossAxisAlignment:
                            CrossAxisAlignment.start,
                        children: [
                          Text(
                            trainerAssignment ==
                                    null
                                ? 'No Trainer Assigned'
                                : 'Assigned Trainer: ${trainerAssignment!['trainer_name']}',
                          ),

                          if (trainerAssignment !=
                              null)
                            const SizedBox(
                              height: 8,
                            ),

                          if (trainerAssignment !=
                              null)
                            RadioListTile(
                              dense: true,
                              value:
                                  'CONTINUE_SAME',
                              groupValue:
                                  trainerChoice,
                              title: const Text(
                                'Continue Same Trainer',
                              ),
                              onChanged:
                                  (value) {
                                setState(() {
                                  trainerChoice =
                                      value!;
                                });
                              },
                            ),

                          if (trainerAssignment !=
                              null)
                            RadioListTile(
                              dense: true,
                              value:
                                  'CHANGE_TRAINER',
                              groupValue:
                                  trainerChoice,
                              title: const Text(
                                'Change Trainer',
                              ),
                              onChanged:
                                  (value) {
                                setState(() {
                                  trainerChoice =
                                      value!;
                                });
                              },
                            ),

                          if (trainerChoice ==
                              'CHANGE_TRAINER')
                            Column(
                              children: [
                                const SizedBox(
                                  height: 10,
                                ),

                                DropdownButtonFormField<
                                    String>(
                                  value:
                                      selectedGoal,
                                  decoration:
                                      const InputDecoration(
                                    labelText:
                                        'Goal',
                                    border:
                                        OutlineInputBorder(),
                                  ),
                                  items: const [
                                    DropdownMenuItem(
                                      value:
                                          'WEIGHT_LOSS',
                                      child: Text(
                                        'Weight Loss',
                                      ),
                                    ),
                                    DropdownMenuItem(
                                      value:
                                          'FAT_LOSS',
                                      child: Text(
                                        'Fat Loss',
                                      ),
                                    ),
                                    DropdownMenuItem(
                                      value:
                                          'MUSCLE_GAIN',
                                      child: Text(
                                        'Muscle Gain',
                                      ),
                                    ),
                                    DropdownMenuItem(
                                      value:
                                          'STRENGTH',
                                      child: Text(
                                        'Strength',
                                      ),
                                    ),
                                    DropdownMenuItem(
                                      value:
                                          'GENERAL_FITNESS',
                                      child: Text(
                                        'General Fitness',
                                      ),
                                    ),
                                  ],
                                  onChanged:
                                      (value) {
                                    setState(() {
                                      selectedGoal =
                                          value!;
                                    });
                                  },
                                ),

                                const SizedBox(
                                  height: 10,
                                ),

                                DropdownButtonFormField<
                                    String>(
                                  value:
                                      selectedTrainerLevel,
                                  decoration:
                                      const InputDecoration(
                                    labelText:
                                        'Trainer Level',
                                    border:
                                        OutlineInputBorder(),
                                  ),
                                  items: const [
                                    DropdownMenuItem(
                                      value:
                                          'LEVEL_1',
                                      child: Text(
                                        'Level 1',
                                      ),
                                    ),
                                    DropdownMenuItem(
                                      value:
                                          'LEVEL_2',
                                      child: Text(
                                        'Level 2',
                                      ),
                                    ),
                                    DropdownMenuItem(
                                      value:
                                          'LEVEL_3',
                                      child: Text(
                                        'Level 3',
                                      ),
                                    ),
                                    DropdownMenuItem(
                                      value:
                                          'LEVEL_4',
                                      child: Text(
                                        'Level 4',
                                      ),
                                    ),
                                  ],
                                  onChanged:
                                      (value) {
                                    setState(() {
                                      selectedTrainerLevel =
                                          value!;
                                    });
                                  },
                                ),

                                const SizedBox(
                                  height: 10,
                                ),

                                ElevatedButton(
                                  onPressed:
                                      loadAvailableTrainers,
                                  child:
                                      const Text(
                                    'LOAD AVAILABLE TRAINERS',
                                  ),
                                ),
                                const SizedBox(
                                   height: 10,
                                ),

                                if (availableTrainers.isNotEmpty)
                                  DropdownButtonFormField<dynamic>(
                                    value: selectedTrainer,
                                    decoration:
                                        const InputDecoration(
                                      labelText:
                                      'Select Trainer',
                                  border:
                                      OutlineInputBorder(),
                                  ),
                                  items:
                                      availableTrainers.map(
                                    (trainer) {
                                      return DropdownMenuItem(
                                        value: trainer,
                                        child: Text(
                                           '${trainer['trainer_name']} (${trainer['trainer_level']})',
                                        ),
                                      );
                                    },
                                  ).toList(),
                                  onChanged: (value) {
                                    setState(() {
                                      selectedTrainer =
                                          value;
                                    });
                                  },
                                ),


                              ],
                            ),
                        ],
                      ),
                    ),
                  ),

                  const SizedBox(
                    height: 20,
                  ),

                  DropdownButtonFormField<
                      dynamic>(
                    value:
                        selectedPackage,
                    decoration:
                        const InputDecoration(
                      labelText:
                          'PT Package',
                      border:
                          OutlineInputBorder(),
                    ),
                    items:
                        packages.map(
                      (package) {
                        return DropdownMenuItem(
                          value:
                              package,
                          child: Text(
                            '${package['name']} - ₹${package['price']}',
                          ),
                        );
                      },
                    ).toList(),
                    onChanged: (value) {
                      setState(() {
                        selectedPackage =
                            value;
                      });
                    },
                  ),

                  const SizedBox(
                    height: 20,
                  ),

                  if (selectedPackage != null)
                    Card(
                      child: ListTile(
                        title: Text(
                          selectedPackage[
                              'name'],
                        ),
                        subtitle: Text(
                          '${selectedPackage['total_sessions']} Sessions • ${selectedPackage['validity_days']} Days',
                        ),
                        trailing: Text(
                          '₹${selectedPackage['price']}',
                        ),
                      ),
                    ),

                  const Spacer(),

                  SizedBox(
                    width:
                        double.infinity,
                    height: 50,
                    child:
                        ElevatedButton(
                      onPressed:
                          isSaving
                              ? null
                              : purchasePackage,
                      child: isSaving
                          ? const CircularProgressIndicator()
                          : const Text(
                              'PURCHASE PT PACKAGE',
                            ),
                    ),
                  ),
                ],
              ),
            ),
    );
  }
}
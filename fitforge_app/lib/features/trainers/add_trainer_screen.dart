import 'package:flutter/material.dart';
import 'trainer_service.dart';

class AddTrainerScreen extends StatefulWidget {
  const AddTrainerScreen({super.key});

  @override
  State<AddTrainerScreen> createState() =>
      _AddTrainerScreenState();
}

class _AddTrainerScreenState
    extends State<AddTrainerScreen> {
  final firstNameController =
      TextEditingController();

  final lastNameController =
      TextEditingController();

  final phoneController =
      TextEditingController();

  final emailController =
      TextEditingController();

  final experienceController =
      TextEditingController();

  bool isSaving = false;

  String trainerLevel = 'LEVEL_1';

  String shiftType = 'SHIFT_3';

  String trainerStatus = 'Off Duty';

  final List<String> specializations = [
    'Weight Loss',
    'Fat Loss',
    'Muscle Building',
    'Strength Training',
    'Powerlifting',
    'Bodybuilding',
    'Sports Conditioning',
    'Functional Training',
    'Rehabilitation',
    'Mobility',
    'Women Fitness',
    'Senior Fitness',
    'Nutrition',
  ];

  List<String> selectedSpecializations =
      [];

  Future<void> saveTrainer() async {
    final firstName =
        firstNameController.text.trim();

    final lastName =
        lastNameController.text.trim();

    final phone =
        phoneController.text.trim();

    final email =
        emailController.text.trim();

    if (firstName.isEmpty ||
        lastName.isEmpty ||
        phone.isEmpty) {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
            'Please fill required fields',
          ),
        ),
      );
      return;
    }

    if (!RegExp(r'^[0-9]{10}$')
        .hasMatch(phone)) {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
            'Phone must be 10 digits',
          ),
        ),
      );
      return;
    }

    if (email.isNotEmpty &&
        !RegExp(
          r'^[\w\-\.]+@([\w\-]+\.)+[\w\-]{2,4}$',
        ).hasMatch(email)) {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
            'Invalid Email',
          ),
        ),
      );
      return;
    }

    if (selectedSpecializations
        .isEmpty) {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
            'Please select at least one specialization',
          ),
        ),
      );
      return;
    }

    setState(() {
      isSaving = true;
    });

    final error =
        await TrainerService.createTrainer(
      firstName: firstName,
      lastName: lastName,
      phone: phone,
      email: email,
      specialization:
          selectedSpecializations.join(
        ', ',
      ),
      experienceYears:
          int.tryParse(
                experienceController.text,
              ) ??
              0,
      trainerLevel: trainerLevel,
      shiftType: shiftType,
      trainerStatus: trainerStatus,
    );

    if (!mounted) return;

    setState(() {
      isSaving = false;
    });

    if (error == null) {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
            'Trainer Created Successfully',
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
        SnackBar(
          content: Text(error),
        ),
      );
    }
  }

  Widget buildField(
    TextEditingController controller,
    String label,
  ) {
    return Padding(
      padding:
          const EdgeInsets.only(
        bottom: 15,
      ),
      child: TextField(
        controller: controller,
        decoration: InputDecoration(
          labelText: label,
          border:
              const OutlineInputBorder(),
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
        title:
            const Text('Add Trainer'),
      ),
      body: SingleChildScrollView(
        padding:
            const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment:
              CrossAxisAlignment.start,
          children: [
            buildField(
              firstNameController,
              'First Name',
            ),

            buildField(
              lastNameController,
              'Last Name',
            ),

            buildField(
              phoneController,
              'Phone',
            ),

            buildField(
              emailController,
              'Email',
            ),

            buildField(
              experienceController,
              'Experience Years',
            ),

            DropdownButtonFormField<
                String>(
              value: trainerLevel,
              decoration:
                  const InputDecoration(
                labelText:
                    'Trainer Level',
                border:
                    OutlineInputBorder(),
              ),
              items: const [
                DropdownMenuItem(
                  value: 'LEVEL_1',
                  child:
                      Text('Level 1'),
                ),
                DropdownMenuItem(
                  value: 'LEVEL_2',
                  child:
                      Text('Level 2'),
                ),
                DropdownMenuItem(
                  value: 'LEVEL_3',
                  child:
                      Text('Level 3'),
                ),
                DropdownMenuItem(
                  value: 'LEVEL_4',
                  child:
                      Text('Level 4'),
                ),
              ],
              onChanged: (value) {
                setState(() {
                  trainerLevel =
                      value!;
                });
              },
            ),

            const SizedBox(
              height: 15,
            ),

            DropdownButtonFormField<
                String>(
              value: shiftType,
              decoration:
                  const InputDecoration(
                labelText:
                    'Shift Timing',
                border:
                    OutlineInputBorder(),
              ),
              items: const [
                DropdownMenuItem(
                  value:
                      'SHIFT_1',
                  child: Text(
                    '6AM-10:30AM & 5PM-9:30PM',
                  ),
                ),
                DropdownMenuItem(
                  value:
                      'SHIFT_2',
                  child: Text(
                    '6AM-10:30AM & 5:30PM-10PM',
                  ),
                ),
                DropdownMenuItem(
                  value:
                      'SHIFT_3',
                  child: Text(
                    '6AM-3PM',
                  ),
                ),
                DropdownMenuItem(
                  value:
                      'SHIFT_4',
                  child: Text(
                    '1PM-10PM',
                  ),
                ),
                DropdownMenuItem(
                  value:
                      'SHIFT_5',
                  child: Text(
                    '5:30AM-3:30PM',
                  ),
                ),
                DropdownMenuItem(
                  value:
                      'SHIFT_6',
                  child: Text(
                    '12PM-9PM',
                  ),
                ),
              ],
              onChanged: (value) {
                setState(() {
                  shiftType =
                      value!;
                });
              },
            ),

            const SizedBox(
              height: 15,
            ),

            DropdownButtonFormField<
                String>(
              value: trainerStatus,
              decoration:
                  const InputDecoration(
                labelText:
                    'Trainer Status',
                border:
                    OutlineInputBorder(),
              ),
              items: const [
                DropdownMenuItem(
                  value:
                      'On Duty',
                  child:
                      Text('On Duty'),
                ),
                DropdownMenuItem(
                  value:
                      'On Break',
                  child:
                      Text('On Break'),
                ),
                DropdownMenuItem(
                  value:
                      'Off Duty',
                  child:
                      Text('Off Duty'),
                ),
                DropdownMenuItem(
                  value: 'Leave',
                  child:
                      Text('Leave'),
                ),
              ],
              onChanged: (value) {
                setState(() {
                  trainerStatus =
                      value!;
                });
              },
            ),

            const SizedBox(
              height: 20,
            ),

            const Text(
              'Specializations',
              style: TextStyle(
                fontSize: 16,
                fontWeight:
                    FontWeight.bold,
              ),
            ),

            const SizedBox(
              height: 10,
            ),

            Wrap(
              spacing: 8,
              runSpacing: 8,
              children:
                  specializations
                      .map(
                (item) {
                  return FilterChip(
                    label: Text(item),
                    selected:
                        selectedSpecializations
                            .contains(
                      item,
                    ),
                    onSelected:
                        (selected) {
                      setState(() {
                        if (selected) {
                          selectedSpecializations
                              .add(
                            item,
                          );
                        } else {
                          selectedSpecializations
                              .remove(
                            item,
                          );
                        }
                      });
                    },
                  );
                },
              ).toList(),
            ),

            const SizedBox(
              height: 30,
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
                        : saveTrainer,
                child: isSaving
                    ? const CircularProgressIndicator()
                    : const Text(
                        'SAVE TRAINER',
                      ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
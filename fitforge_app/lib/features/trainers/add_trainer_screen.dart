import 'package:flutter/material.dart';

import 'trainer_service.dart';
import 'trainer_details_screen.dart';

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

  final specializationController =
      TextEditingController();

  final experienceController =
      TextEditingController();

  bool isSaving = false;

  Future<void> saveTrainer() async {
    if (firstNameController.text.isEmpty ||
        lastNameController.text.isEmpty ||
        phoneController.text.isEmpty) {
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

    setState(() {
      isSaving = true;
    });

    final success =
        await TrainerService.createTrainer(
      firstName:
          firstNameController.text,
      lastName:
          lastNameController.text,
      phone: phoneController.text,
      email: emailController.text,
      specialization:
          specializationController.text,
      experienceYears: int.tryParse(
            experienceController.text,
          ) ??
          0,
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
        const SnackBar(
          content: Text(
            'Failed To Create Trainer',
          ),
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
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title:
            const Text('Add Trainer'),
      ),
      body: SingleChildScrollView(
        padding:
            const EdgeInsets.all(20),
        child: Column(
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
              specializationController,
              'Specialization',
            ),
            buildField(
              experienceController,
              'Experience Years',
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
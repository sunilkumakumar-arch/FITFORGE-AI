import 'package:flutter/material.dart';
import 'trainer_service.dart';

class EditTrainerScreen extends StatefulWidget {
  final Map<String, dynamic> trainer;

  const EditTrainerScreen({
    super.key,
    required this.trainer,
  });

  @override
  State<EditTrainerScreen> createState() =>
      _EditTrainerScreenState();
}

class _EditTrainerScreenState
    extends State<EditTrainerScreen> {
  late TextEditingController
      firstNameController;

  late TextEditingController
      lastNameController;

  late TextEditingController
      phoneController;

  late TextEditingController
      emailController;

  late TextEditingController
      specializationController;

  late TextEditingController
      experienceController;

  @override
  void initState() {
    super.initState();

    firstNameController =
        TextEditingController(
      text:
          widget.trainer['first_name'] ?? '',
    );

    lastNameController =
        TextEditingController(
      text:
          widget.trainer['last_name'] ?? '',
    );

    phoneController =
        TextEditingController(
      text: widget.trainer['phone'] ?? '',
    );

    emailController =
        TextEditingController(
      text: widget.trainer['email'] ?? '',
    );

    specializationController =
        TextEditingController(
      text: widget.trainer[
              'specialization'] ??
          '',
    );

    experienceController =
        TextEditingController(
      text: widget.trainer[
                  'experience_years']
              ?.toString() ??
          '',
    );
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
            const Text('Edit Trainer'),
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

            const SizedBox(height: 20),

            SizedBox(
              width:
                  double.infinity,
              height: 50,
              child: ElevatedButton(
                onPressed: () async {
  final success =
      await TrainerService.updateTrainer(
    id: widget.trainer['id'],
    firstName:
        firstNameController.text,
    lastName:
        lastNameController.text,
    phone: phoneController.text,
    email: emailController.text,
    specialization:
        specializationController.text,
    experienceYears:
        int.tryParse(
              experienceController.text,
            ) ??
            0,
  );

  if (!mounted) return;

  if (success) {
    ScaffoldMessenger.of(context)
        .showSnackBar(
      const SnackBar(
        content: Text(
          'Trainer Updated Successfully',
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
          'Update Failed',
        ),
      ),
    );
  }
},
                child: const Text(
                  'UPDATE TRAINER',
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
import 'package:flutter/material.dart';
import 'member_service.dart';

class EditMemberScreen extends StatefulWidget {
  final Map<String, dynamic> member;

  const EditMemberScreen({
    super.key,
    required this.member,
  });

  @override
  State<EditMemberScreen> createState() =>
      _EditMemberScreenState();
}

class _EditMemberScreenState
    extends State<EditMemberScreen> {
  late TextEditingController firstNameController;
  late TextEditingController lastNameController;
  late TextEditingController phoneController;
  late TextEditingController emailController;
  late TextEditingController genderController;
  late TextEditingController dobController;

  @override
  void initState() {
    super.initState();

    firstNameController =
        TextEditingController(
      text: widget.member['first_name'] ?? '',
    );

    lastNameController =
        TextEditingController(
      text: widget.member['last_name'] ?? '',
    );

    phoneController =
        TextEditingController(
      text: widget.member['phone'] ?? '',
    );

    emailController =
        TextEditingController(
      text: widget.member['email'] ?? '',
    );

    genderController =
        TextEditingController(
      text: widget.member['gender'] ?? '',
    );

    dobController =
        TextEditingController(
      text:
          widget.member['date_of_birth'] ?? '',
    );
  }

  Future<void> updateMember() async {
    final success =
        await MemberService.updateMember(
      id: widget.member['id'],
      firstName:
          firstNameController.text.trim(),
      lastName:
          lastNameController.text.trim(),
      phone: phoneController.text.trim(),
      email: emailController.text.trim(),
      gender:
          genderController.text.trim(),
      dob: dobController.text.trim(),
    );

    if (!mounted) return;

    if (success) {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content:
              Text('Member Updated Successfully'),
        ),
      );

      Navigator.pop(context, true);
    } else {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content:
              Text('Update Failed'),
        ),
      );
    }
  }

  @override
  void dispose() {
    firstNameController.dispose();
    lastNameController.dispose();
    phoneController.dispose();
    emailController.dispose();
    genderController.dispose();
    dobController.dispose();

    super.dispose();
  }

  Widget buildField(
    String label,
    TextEditingController controller,
  ) {
    return Padding(
      padding:
          const EdgeInsets.only(bottom: 16),
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
        title: const Text(
          'Edit Member',
        ),
      ),
      body: SingleChildScrollView(
        padding:
            const EdgeInsets.all(20),
        child: Column(
          children: [
            buildField(
              'First Name',
              firstNameController,
            ),
            buildField(
              'Last Name',
              lastNameController,
            ),
            buildField(
              'Phone',
              phoneController,
            ),
            buildField(
              'Email',
              emailController,
            ),
            buildField(
              'Gender',
              genderController,
            ),
            buildField(
              'Date Of Birth',
              dobController,
            ),

            const SizedBox(height: 20),

            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton(
                onPressed: updateMember,
                child: const Text(
                  'UPDATE MEMBER',
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
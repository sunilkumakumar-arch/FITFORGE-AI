import 'package:flutter/material.dart';
import 'member_service.dart';

class AddMemberScreen extends StatefulWidget {
  const AddMemberScreen({super.key});

  @override
  State<AddMemberScreen> createState() =>
      _AddMemberScreenState();
}

class _AddMemberScreenState
    extends State<AddMemberScreen> {
  final firstNameController =
      TextEditingController();

  final lastNameController =
      TextEditingController();

  final phoneController =
      TextEditingController();

  final emailController =
      TextEditingController();

  final dobController =
      TextEditingController();

  String selectedGender = 'Male';

  bool isSaving = false;

  final firstNameFocus = FocusNode();
  final lastNameFocus = FocusNode();
  final phoneFocus = FocusNode();
  final emailFocus = FocusNode();

  void showError(String message) {
    ScaffoldMessenger.of(context)
        .showSnackBar(
      SnackBar(
        content: Text(message),
      ),
    );
  }

  Future<void> saveMember() async {
    final firstName =
        firstNameController.text.trim();

    final lastName =
        lastNameController.text.trim();

    final phone =
        phoneController.text.trim();

    final email =
        emailController.text.trim();

    final dob =
        dobController.text.trim();

    if (firstName.isEmpty) {
      showError(
        'First Name is required',
      );
      return;
    }

    if (lastName.isEmpty) {
      showError(
        'Last Name is required',
      );
      return;
    }

    if (phone.isEmpty) {
      showError(
        'Phone Number is required',
      );
      return;
    }

    if (!RegExp(r'^[0-9]{10}$')
        .hasMatch(phone)) {
      showError(
        'Phone Number must be exactly 10 digits',
      );
      return;
    }

    if (email.isEmpty) {
      showError(
        'Email is required',
      );
      return;
    }

    if (!RegExp(
      r'^[\w\-\.]+@([\w\-]+\.)+[\w\-]{2,4}$',
    ).hasMatch(email)) {
      showError(
        'Enter a valid email address',
      );
      return;
    }

    if (dob.isEmpty) {
      showError(
        'Date Of Birth is required',
      );
      return;
    }

    setState(() {
      isSaving = true;
    });

    final error =
        await MemberService.createMember(
      firstName: firstName,
      lastName: lastName,
      phone: phone,
      email: email,
      gender: selectedGender,
      dob: dob,
    );

    setState(() {
      isSaving = false;
    });

    if (error == null) {
      ScaffoldMessenger.of(context)
         .showSnackBar(
        const SnackBar(
         content: Text(
           'Member Created Successfully',
          ),
        ),
      );

  Navigator.pop(context, true);
} else {
  showError(error);
}
  }

  Future<void> selectDate() async {
    final pickedDate =
        await showDatePicker(
      context: context,
      initialDate:
          DateTime.now().subtract(
        const Duration(days: 3650),
      ),
      firstDate: DateTime(1940),
      lastDate: DateTime.now(),
    );

    if (pickedDate != null) {
      dobController.text =
          pickedDate
              .toIso8601String()
              .split('T')[0];

      setState(() {});
    }
  }

  @override
  void dispose() {
    firstNameController.dispose();
    lastNameController.dispose();
    phoneController.dispose();
    emailController.dispose();
    dobController.dispose();

    firstNameFocus.dispose();
    lastNameFocus.dispose();
    phoneFocus.dispose();
    emailFocus.dispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Add Member',
        ),
      ),
      body: SingleChildScrollView(
        padding:
            const EdgeInsets.all(20),
        child: Column(
          children: [
            TextField(
              controller:
                  firstNameController,
              focusNode:
                  firstNameFocus,
              textCapitalization:
                  TextCapitalization.words,
              textInputAction:
                  TextInputAction.next,
              onSubmitted: (_) {
                FocusScope.of(context)
                    .requestFocus(
                  lastNameFocus,
                );
              },
              decoration:
                  const InputDecoration(
                labelText:
                    'First Name',
              ),
            ),

            const SizedBox(height: 15),

            TextField(
              controller:
                  lastNameController,
              focusNode:
                  lastNameFocus,
              textCapitalization:
                  TextCapitalization.words,
              textInputAction:
                  TextInputAction.next,
              onSubmitted: (_) {
                FocusScope.of(context)
                    .requestFocus(
                  phoneFocus,
                );
              },
              decoration:
                  const InputDecoration(
                labelText:
                    'Last Name',
              ),
            ),

            const SizedBox(height: 15),

            TextField(
              controller:
                  phoneController,
              focusNode:
                  phoneFocus,
              keyboardType:
                  TextInputType.number,
              textInputAction:
                  TextInputAction.next,
              onSubmitted: (_) {
                FocusScope.of(context)
                    .requestFocus(
                  emailFocus,
                );
              },
              decoration:
                  const InputDecoration(
                labelText:
                    'Phone',
              ),
            ),

            const SizedBox(height: 15),

            TextField(
              controller:
                  emailController,
              focusNode:
                  emailFocus,
              keyboardType:
                  TextInputType.emailAddress,
              decoration:
                  const InputDecoration(
                labelText:
                    'Email',
              ),
            ),

            const SizedBox(height: 15),

            DropdownButtonFormField<String>(
              value: selectedGender,
              decoration:
                  const InputDecoration(
                labelText:
                    'Gender',
                border:
                    OutlineInputBorder(),
              ),
              items: const [
                DropdownMenuItem(
                  value: 'Male',
                  child: Text('Male'),
                ),
                DropdownMenuItem(
                  value: 'Female',
                  child: Text('Female'),
                ),
                DropdownMenuItem(
                  value: 'Other',
                  child: Text('Other'),
                ),
              ],
              onChanged: (value) {
                if (value != null) {
                  setState(() {
                    selectedGender =
                        value;
                  });
                }
              },
            ),

            const SizedBox(height: 15),

            TextField(
              controller:
                  dobController,
              readOnly: true,
              onTap: selectDate,
              decoration:
                  const InputDecoration(
                labelText:
                    'Date Of Birth',
                suffixIcon:
                    Icon(Icons.calendar_month),
              ),
            ),

            const SizedBox(height: 30),

            SizedBox(
              width:
                  double.infinity,
              height: 50,
              child:
                  ElevatedButton(
                onPressed:
                    isSaving
                        ? null
                        : saveMember,
                child: isSaving
                    ? const SizedBox(
                        width: 24,
                        height: 24,
                        child:
                            CircularProgressIndicator(
                          strokeWidth:
                              3,
                        ),
                      )
                    : const Text(
                        'SAVE MEMBER',
                      ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
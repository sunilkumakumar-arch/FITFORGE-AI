import 'package:flutter/material.dart';

import 'membership_service.dart';

class AddMembershipPlanScreen extends StatefulWidget {
  const AddMembershipPlanScreen({super.key});

  @override
  State<AddMembershipPlanScreen> createState() =>
      _AddMembershipPlanScreenState();
}

class _AddMembershipPlanScreenState
    extends State<AddMembershipPlanScreen> {
  final _formKey = GlobalKey<FormState>();

  final _nameController =
      TextEditingController();

  final _durationController =
      TextEditingController();

  final _priceController =
      TextEditingController();

  final _descriptionController =
      TextEditingController();

  bool isSaving = false;

  Future<void> savePlan() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    setState(() {
      isSaving = true;
    });

    final success =
        await MembershipService
            .createMembershipPlan(
      name: _nameController.text.trim(),
      durationDays: int.parse(
        _durationController.text,
      ),
      price: double.parse(
        _priceController.text,
      ),
      description:
          _descriptionController.text.trim(),
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
            'Membership Plan Created',
          ),
        ),
      );

      Navigator.pop(context, true);
    } else {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
            'Failed to create plan',
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
            const Text('Add Membership Plan'),
      ),
      body: Padding(
        padding:
            const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: ListView(
            children: [
              TextFormField(
                controller:
                    _nameController,
                decoration:
                    const InputDecoration(
                  labelText: 'Plan Name',
                ),
                validator: (value) =>
                    value == null ||
                            value.isEmpty
                        ? 'Required'
                        : null,
              ),

              const SizedBox(height: 16),

              TextFormField(
                controller:
                    _durationController,
                keyboardType:
                    TextInputType.number,
                decoration:
                    const InputDecoration(
                  labelText:
                      'Duration Days',
                ),
                validator: (value) =>
                    value == null ||
                            value.isEmpty
                        ? 'Required'
                        : null,
              ),

              const SizedBox(height: 16),

              TextFormField(
                controller:
                    _priceController,
                keyboardType:
                    TextInputType.number,
                decoration:
                    const InputDecoration(
                  labelText: 'Price',
                ),
                validator: (value) =>
                    value == null ||
                            value.isEmpty
                        ? 'Required'
                        : null,
              ),

              const SizedBox(height: 16),

              TextFormField(
                controller:
                    _descriptionController,
                maxLines: 3,
                decoration:
                    const InputDecoration(
                  labelText:
                      'Description',
                ),
              ),

              const SizedBox(height: 24),

              ElevatedButton(
                onPressed:
                    isSaving
                        ? null
                        : savePlan,
                child: isSaving
                    ? const CircularProgressIndicator()
                    : const Text(
                        'Save Plan',
                      ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
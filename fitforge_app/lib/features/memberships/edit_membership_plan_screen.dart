import 'package:flutter/material.dart';

import 'membership_service.dart';

class EditMembershipPlanScreen extends StatefulWidget {
  final Map<String, dynamic> plan;

  const EditMembershipPlanScreen({
    super.key,
    required this.plan,
  });

  @override
  State<EditMembershipPlanScreen> createState() =>
      _EditMembershipPlanScreenState();
}

class _EditMembershipPlanScreenState
    extends State<EditMembershipPlanScreen> {
  final _formKey = GlobalKey<FormState>();

  late TextEditingController _nameController;
  late TextEditingController _durationController;
  late TextEditingController _priceController;
  late TextEditingController _descriptionController;

  bool isSaving = false;

  @override
  void initState() {
    super.initState();

    _nameController = TextEditingController(
      text: widget.plan['name']?.toString() ?? '',
    );

    _durationController = TextEditingController(
      text:
          widget.plan['duration_days']
              ?.toString() ??
          '',
    );

    _priceController = TextEditingController(
      text:
          widget.plan['price']?.toString() ??
          '',
    );

    _descriptionController =
        TextEditingController(
      text:
          widget.plan['description']
              ?.toString() ??
          '',
    );
  }

  Future<void> updatePlan() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    setState(() {
      isSaving = true;
    });

    final success =
        await MembershipService
            .updateMembershipPlan(
      id: widget.plan['id'],
      name: _nameController.text.trim(),
      durationDays: int.parse(
        _durationController.text,
      ),
      price: double.parse(
        _priceController.text,
      ),
      description:
          _descriptionController.text.trim(),
      isActive:
          widget.plan['is_active'] ?? true,
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
            'Membership Plan Updated',
          ),
        ),
      );

      Navigator.pop(context, true);
    } else {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
            'Failed to update plan',
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
            const Text('Edit Membership Plan'),
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
                        : updatePlan,
                child: isSaving
                    ? const CircularProgressIndicator()
                    : const Text(
                        'Update Plan',
                      ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
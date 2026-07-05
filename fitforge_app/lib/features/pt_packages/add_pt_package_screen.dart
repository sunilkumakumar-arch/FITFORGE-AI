import 'package:flutter/material.dart';

import 'pt_package_service.dart';

class AddPTPackageScreen extends StatefulWidget {
  const AddPTPackageScreen({super.key});

  @override
  State<AddPTPackageScreen> createState() =>
      _AddPTPackageScreenState();
}

class _AddPTPackageScreenState
    extends State<AddPTPackageScreen> {
  final _formKey = GlobalKey<FormState>();

  final _nameController =
      TextEditingController();

  final _sessionsController =
      TextEditingController();

  final _validityController =
      TextEditingController();

  final _priceController =
      TextEditingController();

  final _descriptionController =
      TextEditingController();

  bool isSaving = false;

  Future<void> savePackage() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    setState(() {
      isSaving = true;
    });

    final success =
        await PTPackageService.createPackage(
      name: _nameController.text.trim(),
      totalSessions: int.parse(
        _sessionsController.text,
      ),
      validityDays: int.parse(
        _validityController.text,
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
      Navigator.pop(context, true);
    } else {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
            'Failed to create package',
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
            const Text('Add PT Package'),
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
                  labelText:
                      'Package Name',
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
                    _sessionsController,
                keyboardType:
                    TextInputType.number,
                decoration:
                    const InputDecoration(
                  labelText:
                      'Total Sessions',
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
                    _validityController,
                keyboardType:
                    TextInputType.number,
                decoration:
                    const InputDecoration(
                  labelText:
                      'Validity Days',
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
                        : savePackage,
                child: isSaving
                    ? const CircularProgressIndicator()
                    : const Text(
                        'Save Package',
                      ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
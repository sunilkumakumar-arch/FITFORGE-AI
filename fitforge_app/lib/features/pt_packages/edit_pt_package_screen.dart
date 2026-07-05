import 'package:flutter/material.dart';

import 'pt_package_service.dart';

class EditPTPackageScreen extends StatefulWidget {
  final Map<String, dynamic> package;

  const EditPTPackageScreen({
    super.key,
    required this.package,
  });

  @override
  State<EditPTPackageScreen> createState() =>
      _EditPTPackageScreenState();
}

class _EditPTPackageScreenState
    extends State<EditPTPackageScreen> {
  final _formKey = GlobalKey<FormState>();

  late TextEditingController
      _nameController;

  late TextEditingController
      _sessionsController;

  late TextEditingController
      _validityController;

  late TextEditingController
      _priceController;

  late TextEditingController
      _descriptionController;

  bool isSaving = false;

  @override
  void initState() {
    super.initState();

    _nameController =
        TextEditingController(
      text: widget.package['name']
              ?.toString() ??
          '',
    );

    _sessionsController =
        TextEditingController(
      text: widget
              .package['total_sessions']
              ?.toString() ??
          '',
    );

    _validityController =
        TextEditingController(
      text: widget
              .package['validity_days']
              ?.toString() ??
          '',
    );

    _priceController =
        TextEditingController(
      text: widget.package['price']
              ?.toString() ??
          '',
    );

    _descriptionController =
        TextEditingController(
      text: widget.package['description']
              ?.toString() ??
          '',
    );
  }

  Future<void> updatePackage() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    setState(() {
      isSaving = true;
    });

    final success =
        await PTPackageService.updatePackage(
      id: widget.package['id'],
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
            'Failed to update package',
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
            const Text('Edit PT Package'),
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
                        : updatePackage,
                child: isSaving
                    ? const CircularProgressIndicator()
                    : const Text(
                        'Update Package',
                      ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
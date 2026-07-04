import 'package:flutter/material.dart';

import 'package:fitforge_app/features/payments/payment_service.dart';

class AddPaymentScreen extends StatefulWidget {
  final Map<String, dynamic>? member;

  const AddPaymentScreen({
    super.key,
    this.member,
  });

  @override
  State<AddPaymentScreen> createState() =>
      _AddPaymentScreenState();
}

class _AddPaymentScreenState
    extends State<AddPaymentScreen> {
  final memberIdController =
      TextEditingController();

  final planIdController =
      TextEditingController();

  final amountController =
      TextEditingController();

  final transactionController =
      TextEditingController();

  final notesController =
      TextEditingController();

  String paymentMethod = 'Cash';

  String paymentStatus = 'Paid';

  @override
  void initState() {
    super.initState();

    if (widget.member != null) {
      memberIdController.text =
          widget.member!['id'].toString();
    }
  }

  Future<void> savePayment() async {
    if (memberIdController.text.isEmpty ||
        planIdController.text.isEmpty ||
        amountController.text.isEmpty) {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
            'Please fill all required fields',
          ),
        ),
      );
      return;
    }

    final success =
        await PaymentService.createPayment(
      memberId: int.parse(
        memberIdController.text,
      ),
      membershipPlanId: int.parse(
        planIdController.text,
      ),
      amount: double.parse(
        amountController.text,
      ),
      paymentMethod: paymentMethod,
      paymentStatus: paymentStatus,
      transactionId:
          transactionController.text,
      notes: notesController.text,
    );

    if (!mounted) return;

    if (success) {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
            'Payment Added Successfully',
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
            'Failed To Add Payment',
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
        title: const Text(
          'Add Payment',
        ),
      ),
      body: SingleChildScrollView(
        padding:
            const EdgeInsets.all(20),
        child: Column(
          children: [
            buildField(
              memberIdController,
              'Member ID',
            ),

            buildField(
              planIdController,
              'Membership Plan ID',
            ),

            buildField(
              amountController,
              'Amount',
            ),

            DropdownButtonFormField<String>(
              value: paymentMethod,
              decoration:
                  const InputDecoration(
                labelText:
                    'Payment Method',
                border:
                    OutlineInputBorder(),
              ),
              items: const [
                DropdownMenuItem(
                  value: 'Cash',
                  child: Text('Cash'),
                ),
                DropdownMenuItem(
                  value: 'UPI',
                  child: Text('UPI'),
                ),
                DropdownMenuItem(
                  value: 'Card',
                  child: Text('Card'),
                ),
                DropdownMenuItem(
                  value:
                      'Bank Transfer',
                  child: Text(
                    'Bank Transfer',
                  ),
                ),
              ],
              onChanged: (value) {
                setState(() {
                  paymentMethod =
                      value!;
                });
              },
            ),

            const SizedBox(
              height: 15,
            ),

            DropdownButtonFormField<String>(
              value: paymentStatus,
              decoration:
                  const InputDecoration(
                labelText:
                    'Payment Status',
                border:
                    OutlineInputBorder(),
              ),
              items: const [
                DropdownMenuItem(
                  value: 'Paid',
                  child: Text('Paid'),
                ),
                DropdownMenuItem(
                  value: 'Pending',
                  child: Text('Pending'),
                ),
                DropdownMenuItem(
                  value: 'Failed',
                  child: Text('Failed'),
                ),
              ],
              onChanged: (value) {
                setState(() {
                  paymentStatus =
                      value!;
                });
              },
            ),

            const SizedBox(
              height: 15,
            ),

            buildField(
              transactionController,
              'Transaction ID',
            ),

            buildField(
              notesController,
              'Notes',
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
                    savePayment,
                child: const Text(
                  'SAVE PAYMENT',
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
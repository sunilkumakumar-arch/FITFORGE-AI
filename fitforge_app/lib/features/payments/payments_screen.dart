import 'package:flutter/material.dart';

import 'package:fitforge_app/features/payments/payment_service.dart';
import 'package:fitforge_app/features/payments/add_payment_screen.dart';
import 'package:fitforge_app/features/payments/payment_details_screen.dart';

class PaymentsScreen extends StatefulWidget {
  const PaymentsScreen({super.key});

  @override
  State<PaymentsScreen> createState() =>
      _PaymentsScreenState();
}

class _PaymentsScreenState
    extends State<PaymentsScreen> {
  List<dynamic> payments = [];

  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    loadPayments();
  }

  Future<void> loadPayments() async {
    final data =
        await PaymentService.getPayments();

    if (!mounted) return;

    setState(() {
      payments = data;
      isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Payments',
        ),
        actions: [
          IconButton(
            icon: const Icon(
              Icons.add,
            ),
            onPressed: () async {
              final result =
                  await Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) =>
                      const AddPaymentScreen(),
                ),
              );

              if (result == true) {
                loadPayments();
              }
            },
          ),
        ],
      ),
      body: isLoading
          ? const Center(
              child:
                  CircularProgressIndicator(),
            )
          : ListView.builder(
              itemCount: payments.length,
              itemBuilder:
                  (context, index) {
                final payment =
                    payments[index];

                return Card(
                  margin:
                      const EdgeInsets.all(
                    12,
                  ),
                  child: ListTile(
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) =>
                              PaymentDetailsScreen(
                            payment: payment,
                          ),
                        ),
                      );
                    },
                    leading: const Icon(
                      Icons.currency_rupee,
                    ),
                    title: Text(
                      '₹${payment['amount']}',
                    ),
                    subtitle: Text(
                      payment['payment_method'] ??
                          '',
                    ),
                  ),
                );
              },
            ),
    );
  }
}
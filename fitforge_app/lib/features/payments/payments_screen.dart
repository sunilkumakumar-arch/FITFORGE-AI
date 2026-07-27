import 'package:flutter/material.dart';

import 'package:fitforge_app/features/payments/payment_service.dart';
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
          'Payment History',
        ),
      ),
      body: isLoading
          ? const Center(
              child:
                  CircularProgressIndicator(),
            )
          : payments.isEmpty
              ? const Center(
                  child: Text(
                    'No Payments Found',
                  ),
                )
              : ListView.builder(
                  itemCount: payments.length,
                  itemBuilder:
                      (context, index) {
                    final payment =
                        payments[index];

                    return Card(
                      margin:
                          const EdgeInsets.symmetric(
                        horizontal: 12,
                        vertical: 8,
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

                        leading:
                            const CircleAvatar(
                          child: Icon(
                            Icons.currency_rupee,
                          ),
                        ),

                        title: Text(
                          payment['member_name'] ??
                              'Unknown Member',
                          style:
                              const TextStyle(
                            fontWeight:
                                FontWeight.bold,
                          ),
                        ),

                        subtitle: Column(
                          crossAxisAlignment:
                              CrossAxisAlignment
                                  .start,
                          mainAxisSize:
                              MainAxisSize.min,
                          children: [
                            const SizedBox(
                              height: 4,
                            ),

                            Text(
                              payment[
                                      'membership_plan_name'] ??
                                  'No Plan',
                            ),

                            const SizedBox(
                              height: 4,
                            ),

                            Text(
                              '${payment['payment_method']} • ${payment['payment_status']}',
                            ),
                          ],
                        ),

                        trailing: Column(
                          mainAxisAlignment:
                              MainAxisAlignment
                                  .center,
                          children: [
                            Text(
                              '₹${payment['amount']}',
                              style:
                                  const TextStyle(
                                fontWeight:
                                    FontWeight.bold,
                                fontSize: 16,
                              ),
                            ),
                          ],
                        ),
                      ),
                    );
                  },
                ),
    );
  }
}
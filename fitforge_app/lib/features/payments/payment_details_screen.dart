import 'package:flutter/material.dart';

class PaymentDetailsScreen extends StatelessWidget {
  final Map<String, dynamic> payment;

  const PaymentDetailsScreen({
    super.key,
    required this.payment,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Payment Details'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Text(
          payment.toString(),
        ),
      ),
    );
  }
}
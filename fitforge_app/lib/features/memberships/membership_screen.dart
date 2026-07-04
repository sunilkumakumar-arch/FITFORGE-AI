import 'package:flutter/material.dart';

class MembershipScreen extends StatefulWidget {
  const MembershipScreen({super.key});

  @override
  State<MembershipScreen> createState() =>
      _MembershipScreenState();
}

class _MembershipScreenState
    extends State<MembershipScreen> {
  final List<Map<String, dynamic>>
      memberships = [
    {
      'name': 'Monthly',
      'duration': '30 Days',
      'price': '1500'
    },
    {
      'name': 'Quarterly',
      'duration': '90 Days',
      'price': '4000'
    },
    {
      'name': 'Half Yearly',
      'duration': '180 Days',
      'price': '7000'
    },
    {
      'name': 'Yearly',
      'duration': '365 Days',
      'price': '12000'
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Membership Plans',
        ),
      ),
      body: ListView.builder(
        itemCount: memberships.length,
        itemBuilder:
            (context, index) {
          final plan =
              memberships[index];

          return Card(
            margin:
                const EdgeInsets.all(12),
            child: ListTile(
              leading: const Icon(
                Icons.card_membership,
              ),
              title: Text(
                plan['name'],
              ),
              subtitle: Text(
                'Duration: ${plan['duration']}',
              ),
              trailing: Text(
                '₹${plan['price']}',
                style: const TextStyle(
                  fontWeight:
                      FontWeight.bold,
                  fontSize: 16,
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}
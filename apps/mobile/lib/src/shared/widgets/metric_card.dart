import 'package:flutter/material.dart';

class MetricCard extends StatelessWidget {
  const MetricCard({required this.label, required this.value, required this.delta, super.key});
  final String label;
  final String value;
  final String delta;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(label, style: Theme.of(context).textTheme.labelLarge),
          const SizedBox(height: 12),
          Text(value, style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold)),
          const SizedBox(height: 4),
          Text(delta, style: TextStyle(color: Theme.of(context).colorScheme.primary)),
        ]),
      ),
    );
  }
}

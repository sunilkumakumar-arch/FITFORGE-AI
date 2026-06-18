import 'package:flutter/material.dart';

class ModuleScreen extends StatelessWidget {
  const ModuleScreen({required this.title, super.key});
  final String title;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(title)),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text(title, style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold)),
                const SizedBox(height: 8),
                const Text('API-ready mobile interface for FITFORGE AI backend workflows.'),
                const SizedBox(height: 18),
                FilledButton.icon(onPressed: () {}, icon: const Icon(Icons.sync), label: const Text('Sync with backend')),
              ]),
            ),
          ),
          const SizedBox(height: 16),
          for (final item in _records(title))
            Card(child: ListTile(title: Text(item.$1), subtitle: Text(item.$2), trailing: const Icon(Icons.chevron_right))),
        ],
      ),
    );
  }
}

List<(String, String)> _records(String title) => [
      ('$title Overview', 'Live state, filters, and role-aware actions.'),
      ('$title History', 'Offline-friendly timeline and backend sync queue.'),
      ('$title Insights', 'AI-assisted recommendations and analytics.'),
    ];

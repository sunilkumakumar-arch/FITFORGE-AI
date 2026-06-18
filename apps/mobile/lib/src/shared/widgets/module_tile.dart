import 'package:flutter/material.dart';

class ModuleTile extends StatelessWidget {
  const ModuleTile({required this.title, required this.description, required this.icon, super.key});
  final String title;
  final String description;
  final IconData icon;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: Icon(icon, color: Theme.of(context).colorScheme.primary),
        title: Text(title, style: const TextStyle(fontWeight: FontWeight.w700)),
        subtitle: Text(description),
        trailing: const Icon(Icons.chevron_right),
        onTap: () => Navigator.of(context).pushNamed('/module', arguments: title),
      ),
    );
  }
}

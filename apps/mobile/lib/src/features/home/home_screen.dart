import 'package:flutter/material.dart';
import '../../core/state/app_scope.dart';
import '../../core/state/app_state.dart';
import '../../shared/widgets/metric_card.dart';
import '../../shared/widgets/module_tile.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final state = AppScope.of(context);
    final isTrainer = state.role == MobileRole.trainer;
    final modules = isTrainer ? _trainerModules : _memberModules;
    return Scaffold(
      appBar: AppBar(
        title: Text(isTrainer ? 'Trainer App' : 'Member App'),
        actions: [IconButton(onPressed: state.logout, icon: const Icon(Icons.logout))],
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text(isTrainer ? 'Coach your clients with AI insights.' : 'Forge your transformation.', style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold)),
          const SizedBox(height: 16),
          const Row(children: [
            Expanded(child: MetricCard(label: 'Workouts', value: '18', delta: '+4 this week')),
            SizedBox(width: 12),
            Expanded(child: MetricCard(label: 'Posture', value: '82%', delta: 'Low risk')),
          ]),
          const SizedBox(height: 16),
          ...modules.map((module) => ModuleTile(title: module.$1, description: module.$2, icon: module.$3)),
        ],
      ),
    );
  }
}

const _memberModules = [
  ('Attendance', 'QR check-ins and visit history.', Icons.qr_code),
  ('Memberships', 'Plan status, renewals, and payments.', Icons.credit_card),
  ('Workout Programs', 'Assigned workouts and completion tracking.', Icons.fitness_center),
  ('Exercise Library', 'Premium exercise guidance and videos.', Icons.video_library),
  ('Nutrition Plans', 'Macros, meals, water, and food logs.', Icons.restaurant),
  ('Progress Tracking', 'Body metrics and transformation timeline.', Icons.show_chart),
  ('AI Posture Analysis', 'Real-time camera posture scans.', Icons.camera_alt),
  ('E-commerce Store', 'Supplements, apparel, and accessories.', Icons.store),
  ('Notifications', 'Reminders, alerts, and coach messages.', Icons.notifications),
];

const _trainerModules = [
  ('Client Management', 'Assigned members and adherence status.', Icons.groups),
  ('Workout Programs', 'Create and assign training plans.', Icons.fitness_center),
  ('Exercise Library', 'Exercise coaching and safety references.', Icons.video_library),
  ('Nutrition Plans', 'Review client macros and meal adherence.', Icons.restaurant),
  ('Progress Tracking', 'Strength, body, and habit trends.', Icons.show_chart),
  ('AI Posture Analysis', 'Review scan reports and corrective plans.', Icons.camera_alt),
  ('Reports and Analytics', 'Client outcomes and trainer performance.', Icons.analytics),
  ('Notifications', 'Send reminders and coaching nudges.', Icons.notifications),
];

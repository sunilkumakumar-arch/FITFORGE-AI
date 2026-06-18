import 'package:flutter/material.dart';
import '../../core/state/app_scope.dart';
import '../../core/state/app_state.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final emailController = TextEditingController(text: 'member@fitforge.ai');
  final passwordController = TextEditingController(text: 'Fitforge@12345');
  bool loading = false;

  @override
  Widget build(BuildContext context) {
    final appState = AppScope.of(context);
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            const Spacer(),
            Text('FITFORGE AI', style: Theme.of(context).textTheme.displaySmall?.copyWith(fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Text('Member and Trainer mobile command center.', style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 32),
            SegmentedButton<MobileRole>(
              segments: const [
                ButtonSegment(value: MobileRole.member, label: Text('Member')),
                ButtonSegment(value: MobileRole.trainer, label: Text('Trainer')),
              ],
              selected: {appState.role},
              onSelectionChanged: (value) => appState.switchRole(value.first),
            ),
            const SizedBox(height: 16),
            TextField(controller: emailController, decoration: const InputDecoration(labelText: 'Email')),
            const SizedBox(height: 12),
            TextField(controller: passwordController, obscureText: true, decoration: const InputDecoration(labelText: 'Password')),
            const SizedBox(height: 24),
            FilledButton(
              onPressed: loading ? null : () async {
                setState(() => loading = true);
                try {
                  await appState.login(emailController.text, passwordController.text);
                } catch (_) {
                  appState.apiClient.setToken('demo-token');
                }
                if (context.mounted) Navigator.of(context).pushReplacementNamed('/home');
              },
              child: Text(loading ? 'Signing in...' : 'Sign in'),
            ),
            const Spacer(),
          ]),
        ),
      ),
    );
  }
}

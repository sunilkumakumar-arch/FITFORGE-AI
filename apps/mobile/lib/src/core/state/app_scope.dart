import 'package:flutter/material.dart';
import 'app_state.dart';

class AppScope extends StatefulWidget {
  const AppScope({required this.child, super.key});
  final Widget child;

  static AppState of(BuildContext context) {
    final scope = context.dependOnInheritedWidgetOfExactType<_InheritedAppScope>();
    assert(scope != null, 'AppScope not found in widget tree');
    return scope!.notifier!;
  }

  @override
  State<AppScope> createState() => _AppScopeState();
}

class _AppScopeState extends State<AppScope> {
  final AppState state = AppState();

  @override
  Widget build(BuildContext context) {
    return _InheritedAppScope(notifier: state, child: widget.child);
  }
}

class _InheritedAppScope extends InheritedNotifier<AppState> {
  const _InheritedAppScope({required super.notifier, required super.child});
}

import 'package:flutter/material.dart';
import '../features/auth/login_screen.dart';
import '../features/home/home_screen.dart';
import '../features/modules/module_screen.dart';

class AppRoute {
  const AppRoute._(this.path);
  final String path;

  static const login = AppRoute._('/login');
  static const home = AppRoute._('/home');
  static const module = AppRoute._('/module');
}

class AppRouter {
  static Route<void> onGenerateRoute(RouteSettings settings) {
    return MaterialPageRoute<void>(
      settings: settings,
      builder: (_) {
        switch (settings.name) {
          case '/login':
            return const LoginScreen();
          case '/module':
            final title = settings.arguments as String? ?? 'Module';
            return ModuleScreen(title: title);
          case '/home':
          default:
            return const HomeScreen();
        }
      },
    );
  }
}

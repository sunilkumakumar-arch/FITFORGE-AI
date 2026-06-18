import 'package:flutter/material.dart';
import '../core/state/app_scope.dart';
import '../core/theme/app_theme.dart';
import '../routing/app_router.dart';

class FitforgeApp extends StatelessWidget {
  const FitforgeApp({super.key});

  @override
  Widget build(BuildContext context) {
    return AppScope(
      child: MaterialApp(
        title: 'FITFORGE AI',
        debugShowCheckedModeBanner: false,
        theme: AppTheme.light,
        darkTheme: AppTheme.dark,
        themeMode: ThemeMode.dark,
        onGenerateRoute: AppRouter.onGenerateRoute,
        initialRoute: AppRoute.login.path,
      ),
    );
  }
}

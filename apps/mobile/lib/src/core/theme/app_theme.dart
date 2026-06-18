import 'package:flutter/material.dart';

class AppTheme {
  static const gold = Color(0xFFD4AF37);
  static const black = Color(0xFF050505);

  static ThemeData get dark => ThemeData(
        brightness: Brightness.dark,
        colorScheme: ColorScheme.fromSeed(seedColor: gold, brightness: Brightness.dark, surface: const Color(0xFF101010)),
        scaffoldBackgroundColor: black,
        useMaterial3: true,
        cardTheme: CardThemeData(
          color: const Color(0xFF101010),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
        ),
      );

  static ThemeData get light => ThemeData(
        brightness: Brightness.light,
        colorScheme: ColorScheme.fromSeed(seedColor: gold),
        useMaterial3: true,
      );
}

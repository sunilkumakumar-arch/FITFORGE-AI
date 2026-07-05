import 'dart:convert';
import 'package:http/http.dart' as http;

import '../../core/services/auth_service.dart';

class PTPackageService {
  static const String baseUrl =
      'http://127.0.0.1:8000/api/v1/pt-packages';

  static Future<List<dynamic>> getPackages() async {
    final token = await AuthService.getToken();

    final response = await http.get(
      Uri.parse('$baseUrl/packages/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }

    return [];
  }

  static Future<int> getPackageCount() async {
    final packages = await getPackages();
    return packages.length;
  }

  static Future<bool> createPackage({
    required String name,
    required int totalSessions,
    required int validityDays,
    required double price,
    String description = '',
  }) async {
    final token = await AuthService.getToken();

    final response = await http.post(
      Uri.parse('$baseUrl/packages/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode({
        'name': name,
        'description': description,
        'total_sessions': totalSessions,
        'validity_days': validityDays,
        'price': price,
        'is_active': true,
      }),
    );

    return response.statusCode == 201;
  }

  static Future<bool> updatePackage({
    required int id,
    required String name,
    required int totalSessions,
    required int validityDays,
    required double price,
    String description = '',
    bool isActive = true,
  }) async {
    final token = await AuthService.getToken();

    final response = await http.put(
      Uri.parse('$baseUrl/packages/$id/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode({
        'name': name,
        'description': description,
        'total_sessions': totalSessions,
        'validity_days': validityDays,
        'price': price,
        'is_active': isActive,
      }),
    );

    return response.statusCode == 200;
  }

  static Future<bool> deactivatePackage(
    int id,
  ) async {
    final token = await AuthService.getToken();

    final response = await http.patch(
      Uri.parse(
        '$baseUrl/packages/$id/deactivate/',
      ),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );

    return response.statusCode == 200;
  }
}
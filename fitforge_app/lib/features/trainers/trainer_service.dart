import 'dart:convert';
import 'package:http/http.dart' as http;

import '../../core/services/auth_service.dart';

class TrainerService {
  static const String baseUrl =
      'http://127.0.0.1:8000/api/v1/trainers/';

  static Future<int> getTrainerCount() async {
    final token =
        await AuthService.getToken();

    final response = await http.get(
      Uri.parse(baseUrl),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );

    print(
      'TRAINER COUNT STATUS: ${response.statusCode}',
    );

    print(
      'TRAINER COUNT BODY: ${response.body}',
    );

    if (response.statusCode == 200) {
      final data =
          jsonDecode(response.body);

      return data.length;
    }

    return 0;
  }

  static Future<List<dynamic>>
      getTrainers() async {
    final token =
        await AuthService.getToken();

    final response = await http.get(
      Uri.parse(baseUrl),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );

    print(
      'GET TRAINERS STATUS: ${response.statusCode}',
    );

    print(
      'GET TRAINERS BODY: ${response.body}',
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }

    return [];
  }

  static Future<bool> createTrainer({
    required String firstName,
    required String lastName,
    required String phone,
    required String email,
    required String specialization,
    required int experienceYears,
  }) async {
    final token =
        await AuthService.getToken();

    final response = await http.post(
      Uri.parse(baseUrl),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode({
        'first_name': firstName,
        'last_name': lastName,
        'phone': phone,
        'email': email,
        'specialization': specialization,
        'experience_years': experienceYears,
      }),
    );

    print(
      'CREATE STATUS: ${response.statusCode}',
    );

    print(
      'CREATE BODY: ${response.body}',
    );

    return response.statusCode == 201;
  }

  static Future<bool>
      deleteTrainer(int id) async {
    final token =
        await AuthService.getToken();

    final response = await http.delete(
      Uri.parse('$baseUrl$id/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );

    print(
      'DELETE STATUS: ${response.statusCode}',
    );

    print(
      'DELETE BODY: ${response.body}',
    );

    return response.statusCode == 204;
  }

  static Future<bool> updateTrainer({
    required int id,
    required String firstName,
    required String lastName,
    required String phone,
    required String email,
    required String specialization,
    required int experienceYears,
  }) async {
    final token =
        await AuthService.getToken();

    final response = await http.put(
      Uri.parse('$baseUrl$id/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode({
        'first_name': firstName,
        'last_name': lastName,
        'phone': phone,
        'email': email,
        'specialization': specialization,
        'experience_years': experienceYears,
      }),
    );

    print(
      'UPDATE STATUS: ${response.statusCode}',
    );

    print(
      'UPDATE BODY: ${response.body}',
    );

    return response.statusCode == 200;
  }
}
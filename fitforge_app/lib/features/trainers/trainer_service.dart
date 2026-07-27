import 'dart:convert';
import 'package:http/http.dart' as http;

import '../../core/services/auth_service.dart';

class TrainerService {
  static const String baseUrl =
      'http://127.0.0.1:8000/api/v1/trainers/';

  // ==========================
  // GET TRAINER COUNT
  // ==========================
  static Future<int> getTrainerCount() async {
    final token = await AuthService.getToken();

    final response = await http.get(
      Uri.parse(baseUrl),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );

    print('TRAINER COUNT STATUS: ${response.statusCode}');
    print('TRAINER COUNT BODY: ${response.body}');

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);

      if (data is List) {
        return data.length;
      }

      if (data is Map && data.containsKey('count')) {
        return data['count'];
      }
    }

    return 0;
  }

  // ==========================
  // GET ALL TRAINERS
  // ==========================
  static Future<List<dynamic>> getTrainers() async {
    final token = await AuthService.getToken();

    final response = await http.get(
      Uri.parse(baseUrl),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );

    print('GET TRAINERS STATUS: ${response.statusCode}');
    print('GET TRAINERS BODY: ${response.body}');

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);

      if (data is List) {
        return data;
      }

      if (data is Map && data.containsKey('results')) {
        return data['results'];
      }
    }

    return [];
  }

  // ==========================
  // ASSIGNMENT CENTER
  // ==========================
  static Future<List<dynamic>> getAssignmentCenter() async {
    final token = await AuthService.getToken();

    final response = await http.get(
      Uri.parse('${baseUrl}assignment_center/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );

    print(
      'ASSIGNMENT CENTER STATUS: ${response.statusCode}',
    );

    print(
      'ASSIGNMENT CENTER BODY: ${response.body}',
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }

    return [];
  }

  // ==========================
  // CREATE TRAINER
  // ==========================
  static Future<String?> createTrainer({
    required String firstName,
    required String lastName,
    required String phone,
    required String email,
    required String specialization,
    required int experienceYears,
    required String trainerLevel,
    required String shiftType,
    required String trainerStatus,
  }) async {
    final token = await AuthService.getToken();

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
        'trainer_level': trainerLevel,
        'shift_type': shiftType,
        'trainer_status': trainerStatus,
      }),
    );

    print(
      'CREATE STATUS: ${response.statusCode}',
    );

    print(
      'CREATE BODY: ${response.body}',
    );

    if (response.statusCode == 201) {
      return null;
    }

    final errorData = jsonDecode(response.body);

    if (errorData['phone'] != null) {
      return errorData['phone'][0];
    }

    if (errorData['email'] != null) {
      return errorData['email'][0];
    }

    return 'Failed To Create Trainer';
  }

  // ==========================
  // DELETE TRAINER
  // ==========================
  static Future<bool> deleteTrainer(int id) async {
    final token = await AuthService.getToken();

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

  // ==========================
  // UPDATE TRAINER
  // ==========================
  static Future<bool> updateTrainer({
    required int id,
    required String firstName,
    required String lastName,
    required String phone,
    required String email,
    required String specialization,
    required int experienceYears,
  }) async {
    final token = await AuthService.getToken();

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

  // ==========================
  // TRAINER DASHBOARD
  // ==========================
  static Future<Map<String, dynamic>?> getDashboardSummary() async {
    final token = await AuthService.getToken();

    final response = await http.get(
      Uri.parse('${baseUrl}dashboard/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );

    print(
      'TRAINER DASHBOARD STATUS: ${response.statusCode}',
    );

    print(
      'TRAINER DASHBOARD BODY: ${response.body}',
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }

    return null;
  }
}
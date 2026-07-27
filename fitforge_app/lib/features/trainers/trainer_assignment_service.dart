import 'dart:convert';
import 'package:http/http.dart' as http;

import '../../core/services/auth_service.dart';

class TrainerAssignmentService {
  static const String baseUrl =
      'http://127.0.0.1:8000/api/v1/trainer-assignments/';

  static Future<List<dynamic>> getAssignments() async {
    final token = await AuthService.getToken();

    final response = await http.get(
      Uri.parse(baseUrl),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);

      // Supports both paginated and non-paginated APIs
      if (data is List) {
        return data;
      }

      if (data is Map<String, dynamic>) {
        return data['results'] ?? [];
      }
    }

    return [];
  }

  static Future<List<dynamic>> getTrainerAssignments(
    int trainerId,
  ) async {
    final assignments = await getAssignments();

    return assignments.where((item) {
      return item['trainer'] == trainerId;
    }).toList();
  }

  static Future<Map<String, dynamic>?> getMemberTrainer(
    int memberId,
  ) async {
    final assignments = await getAssignments();

    try {
      return assignments.firstWhere(
        (item) =>
            item['member'] == memberId &&
            item['is_active'] == true,
      );
    } catch (_) {
      return null;
    }
  }

  static Future<List<dynamic>> getAvailableTrainers({
    required String goalType,
    required String slotTime,
    required String trainerLevel,
  }) async {
    final token = await AuthService.getToken();

    final response = await http.get(
      Uri.parse(
        '${baseUrl}available-trainers/'
        '?goal_type=$goalType'
        '&slot_time=$slotTime'
        '&trainer_level=$trainerLevel',
      ),
      headers: {
        'Authorization': 'Bearer $token',
      },
    );

    print(
      'AVAILABLE TRAINERS STATUS: ${response.statusCode}',
    );

    print(
      'AVAILABLE TRAINERS BODY: ${response.body}',
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);

      if (data is List) {
        return data;
      }

      if (data is Map<String, dynamic>) {
        return data['results'] ?? [];
      }
    }

    return [];
  }

  static Future<Map<String, dynamic>?> autoAssignTrainer({
    required String goalType,
    required String slotTime,
  }) async {
    final token = await AuthService.getToken();

    final response = await http.post(
      Uri.parse('${baseUrl}auto-assign/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode({
        'goal_type': goalType,
        'slot_time': slotTime,
      }),
    );

    print(
      'AUTO ASSIGN STATUS: ${response.statusCode}',
    );

    print(
      'AUTO ASSIGN BODY: ${response.body}',
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }

    return null;
  }

  static Future<int?> changeTrainer({
    required int memberId,
    required int trainerId,
    required String goalType,
    required String slotTime,
  }) async {
    final token = await AuthService.getToken();

    final response = await http.post(
      Uri.parse('${baseUrl}change-trainer/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode({
        'member_id': memberId,
        'trainer_id': trainerId,
        'goal_type': goalType,
        'slot_time': slotTime,
        'day_pattern': 'MWF',
      }),
    );

    print(
      'CHANGE TRAINER STATUS: ${response.statusCode}',
    );

    print(
      'CHANGE TRAINER BODY: ${response.body}',
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data['assignment_id'];
    }

    return null;
  }

  static Future<int?> createTrainerAssignment({
    required int trainerId,
    required int memberId,
    required String goalType,
    required String slotTime,
    required String dayPattern,
  }) async {
    final token = await AuthService.getToken();

    final response = await http.post(
      Uri.parse('${baseUrl}create-assignment/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode({
        'trainer': trainerId,
        'member': memberId,
        'start_date':
            DateTime.now().toIso8601String().split('T')[0],
        'monthly_fee': 0,
        'sessions_per_week': 3,
        'assignment_type': 'MEMBERSHIP',
        'package_type': '6_DAYS',
        'goal_type': goalType,
        'slot_time': slotTime,
        'day_pattern': dayPattern,
        'auto_assigned': false,
        'is_active': true,
      }),
    );

    print(
      'CREATE ASSIGNMENT STATUS: ${response.statusCode}',
    );

    print(
      'CREATE ASSIGNMENT BODY: ${response.body}',
    );

    if (response.statusCode == 200 ||
        response.statusCode == 201) {
      final data = jsonDecode(response.body);
      return data['assignment_id'];
    }

    return null;
  }

  static Future<bool> assignMember({
    required int trainerId,
    required int memberId,
  }) async {
    final token = await AuthService.getToken();

    final response = await http.post(
      Uri.parse(baseUrl),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode({
        'trainer': trainerId,
        'member': memberId,
        'start_date':
            DateTime.now().toIso8601String().split('T')[0],
        'monthly_fee': 0,
        'sessions_per_week': 3,
        'is_active': true,
      }),
    );

    return response.statusCode == 201;
  }
}
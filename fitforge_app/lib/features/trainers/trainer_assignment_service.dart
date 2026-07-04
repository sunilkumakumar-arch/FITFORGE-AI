import 'dart:convert';
import 'package:http/http.dart' as http;

import '../../core/services/auth_service.dart';

class TrainerAssignmentService {
  static const String baseUrl =
      'http://127.0.0.1:8000/api/v1/trainer-assignments/';

  static Future<List<dynamic>>
      getAssignments() async {
    final token =
        await AuthService.getToken();

    final response = await http.get(
      Uri.parse(baseUrl),
      headers: {
        'Content-Type':
            'application/json',
        'Authorization':
            'Bearer $token',
      },
    );

    print(
      'ASSIGNMENTS STATUS: ${response.statusCode}',
    );

    print(
      'ASSIGNMENTS BODY: ${response.body}',
    );

    if (response.statusCode == 200) {
      final data =
          jsonDecode(response.body);

      print(data);

      return data;
    }

    return [];
  }

  static Future<List<dynamic>>
      getTrainerAssignments(
    int trainerId,
  ) async {
    final assignments =
        await getAssignments();

    return assignments.where((item) {
      return item['trainer'] ==
          trainerId;
    }).toList();
  }

  static Future<bool> assignMember({
    required int trainerId,
    required int memberId,
  }) async {
    final token =
        await AuthService.getToken();

    final response = await http.post(
      Uri.parse(baseUrl),
      headers: {
        'Content-Type':
            'application/json',
        'Authorization':
            'Bearer $token',
      },
      body: jsonEncode({
        'trainer': trainerId,
        'member': memberId,
        'start_date':
            DateTime.now()
                .toIso8601String()
                .split('T')[0],
        'monthly_fee': 0,
        'sessions_per_week': 3,
        'is_active': true,
      }),
    );

    print(
      'ASSIGN MEMBER STATUS: ${response.statusCode}',
    );

    print(
      'ASSIGN MEMBER BODY: ${response.body}',
    );

    return response.statusCode == 201;
  }
}
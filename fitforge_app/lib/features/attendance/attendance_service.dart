import 'dart:convert';
import 'package:http/http.dart' as http;

import '../../core/services/auth_service.dart';

class AttendanceService {
  static const String baseUrl =
      'http://127.0.0.1:8000/api/v1/attendance/';

  static Future<List<dynamic>> getAttendance() async {
    final token = await AuthService.getToken();

    final response = await http.get(
      Uri.parse(baseUrl),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );

    print('ATTENDANCE STATUS: ${response.statusCode}');
    print('ATTENDANCE BODY: ${response.body}');

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }

    return [];
  }

  static Future<bool> markAttendance({
    required int memberId,
    required int branchId,
  }) async {
    final token = await AuthService.getToken();

    final now = DateTime.now();

    final response = await http.post(
      Uri.parse(baseUrl),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode({
        'member': memberId,
        'branch': branchId,
        'attendance_date':
            now.toIso8601String().split('T')[0],
        'check_in': now.toIso8601String(),
        'status': 'Present',
        'checkin_method': 'Manual',
      }),
    );

    print('ATTENDANCE STATUS: ${response.statusCode}');
    print('ATTENDANCE BODY: ${response.body}');

    return response.statusCode == 201;
  }

  static Future<int> getAttendanceCount() async {
    final data = await getAttendance();
    return data.length;
  }
}
import 'dart:convert';
import 'package:http/http.dart' as http;

import '../../core/services/auth_service.dart';

class MembershipService {
  static const String baseUrl =
      'http://127.0.0.1:8000/api/v1/memberships';

  static Future<List<dynamic>> getMembershipPlans() async {
    final token = await AuthService.getToken();

    final response = await http.get(
      Uri.parse('$baseUrl/membership-plans/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );

    print('PLANS STATUS: ${response.statusCode}');
    print('PLANS BODY: ${response.body}');

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }

    return [];
  }

  static Future<int> getMembershipPlanCount() async {
    final token = await AuthService.getToken();

    final response = await http.get(
      Uri.parse('$baseUrl/membership-plans/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data.length;
    }

    return 0;
  }

  static Future<bool> assignMembership({
    required int memberId,
    required int planId,
    required String startDate,
    required double amountPaid,
  }) async {
    final token = await AuthService.getToken();

    final response = await http.post(
      Uri.parse('$baseUrl/member-memberships/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode({
        'member': memberId,
        'plan': planId,
        'start_date': startDate,
        'amount_paid': amountPaid,
        'status': 'Active',
      }),
    );

    print('ASSIGN STATUS: ${response.statusCode}');
    print('ASSIGN BODY: ${response.body}');

    return response.statusCode == 201;
  }

  static Future<Map<String, dynamic>?> getMemberMembership(
    int memberId,
  ) async {
    final token = await AuthService.getToken();

    final response = await http.get(
      Uri.parse('$baseUrl/member-memberships/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );

    print('MEMBERSHIP STATUS: ${response.statusCode}');
    print('MEMBERSHIP BODY: ${response.body}');

    if (response.statusCode == 200) {
      final List data = jsonDecode(response.body);

      try {
        return data.firstWhere(
          (item) => item['member'] == memberId,
        );
      } catch (e) {
        return null;
      }
    }

    return null;
  }

  static Future<bool> createMembershipPlan({
    required String name,
    required int durationDays,
    required double price,
    String description = '',
  }) async {
    final token = await AuthService.getToken();

    final response = await http.post(
      Uri.parse('$baseUrl/membership-plans/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode({
        'name': name,
        'duration_days': durationDays,
        'price': price,
        'description': description,
        'is_active': true,
      }),
    );

    print('CREATE PLAN STATUS: ${response.statusCode}');
    print('CREATE PLAN BODY: ${response.body}');

    return response.statusCode == 201;
  }

  static Future<bool> updateMembershipPlan({
    required int id,
    required String name,
    required int durationDays,
    required double price,
    String description = '',
    bool isActive = true,
  }) async {
    final token = await AuthService.getToken();

    final response = await http.put(
      Uri.parse('$baseUrl/membership-plans/$id/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode({
        'name': name,
        'duration_days': durationDays,
        'price': price,
        'description': description,
        'is_active': isActive,
      }),
    );

    print('UPDATE PLAN STATUS: ${response.statusCode}');
    print('UPDATE PLAN BODY: ${response.body}');

    return response.statusCode == 200;
  }

  static Future<bool> deactivateMembershipPlan(
    int id,
  ) async {
    final token = await AuthService.getToken();

    final response = await http.patch(
      Uri.parse('$baseUrl/membership-plans/$id/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode({
        'is_active': false,
      }),
    );

    print('DEACTIVATE PLAN STATUS: ${response.statusCode}');
    print('DEACTIVATE PLAN BODY: ${response.body}');

    return response.statusCode == 200;
  }
}
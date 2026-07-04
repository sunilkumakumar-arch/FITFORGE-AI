import 'dart:convert';
import 'package:http/http.dart' as http;
import '../../core/services/auth_service.dart';

class MemberService {
  static const String baseUrl =
      'http://127.0.0.1:8000/api/v1/accounts';

  static Future<int> getMemberCount() async {
    final token = await AuthService.getToken();

    final response = await http.get(
      Uri.parse('$baseUrl/members/'),
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

  static Future<List<dynamic>> getMembers() async {
    final token = await AuthService.getToken();

    final response = await http.get(
      Uri.parse('$baseUrl/members/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );

    print(
        'GET MEMBERS STATUS: ${response.statusCode}');
    print(
        'GET MEMBERS BODY: ${response.body}');

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }

    return [];
  }

  static Future<bool> createMember({
    required String firstName,
    required String lastName,
    required String phone,
    required String email,
    required String gender,
    required String dob,
  }) async {
    final token = await AuthService.getToken();

    final response = await http.post(
      Uri.parse('$baseUrl/members/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode({
        'first_name': firstName,
        'last_name': lastName,
        'phone': phone,
        'email': email,
        'gender': gender,
        'date_of_birth': dob,
        'joining_date':
            DateTime.now().toString().split(' ')[0],
      }),
    );

    print(
        'CREATE MEMBER STATUS: ${response.statusCode}');
    print(
        'CREATE MEMBER BODY: ${response.body}');

    return response.statusCode == 201;
  }

  static Future<bool> updateMember({
    required int id,
    required String firstName,
    required String lastName,
    required String phone,
    required String email,
    required String gender,
    required String dob,
  }) async {
    final token = await AuthService.getToken();

    final response = await http.put(
      Uri.parse('$baseUrl/members/$id/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode({
        'first_name': firstName,
        'last_name': lastName,
        'phone': phone,
        'email': email,
        'gender': gender,
        'date_of_birth': dob,
      }),
    );

    print(
        'UPDATE MEMBER STATUS: ${response.statusCode}');
    print(
        'UPDATE MEMBER BODY: ${response.body}');

    return response.statusCode == 200;
  }

  static Future<bool> deleteMember(
    int id,
  ) async {
    final token = await AuthService.getToken();

    final response = await http.delete(
      Uri.parse('$baseUrl/members/$id/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );

    print(
        'DELETE MEMBER STATUS: ${response.statusCode}');

    return response.statusCode == 204;
  }
}
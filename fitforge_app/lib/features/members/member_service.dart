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
      return data['count'] ?? 0;
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

    print('GET MEMBERS STATUS: ${response.statusCode}');
    print('GET MEMBERS BODY: ${response.body}');

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);

      if (data is Map<String, dynamic>) {
        return List<dynamic>.from(data['results'] ?? []);
      }

      if (data is List) {
        return List<dynamic>.from(data);
      }
    }

    return [];
  }

  static Future<Map<String, dynamic>?> getMemberById(
    int memberId,
  ) async {
    final members = await getMembers();

    try {
      return members.firstWhere(
        (member) => member['id'] == memberId,
      );
    } catch (_) {
      return null;
    }
  }

  static Future<String?> createMember({
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

    print('CREATE MEMBER STATUS: ${response.statusCode}');
    print('CREATE MEMBER BODY: ${response.body}');

    if (response.statusCode == 201) {
      return null;
    }

    try {
      final errorData = jsonDecode(response.body);

      if (errorData['phone'] != null) {
        return errorData['phone'][0];
      }

      if (errorData['email'] != null) {
        return errorData['email'][0];
      }

      if (errorData['detail'] != null) {
        return errorData['detail'];
      }
    } catch (_) {}

    return 'Unable to create member';
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

    print('UPDATE MEMBER STATUS: ${response.statusCode}');
    print('UPDATE MEMBER BODY: ${response.body}');

    return response.statusCode == 200;
  }

  static Future<bool> updateMemberPreferences({
    required int memberId,
    required String preferredSlot,
    required String experienceLevel,
    required String trainerPreference,
  }) async {
    final token = await AuthService.getToken();

    final response = await http.patch(
      Uri.parse('$baseUrl/members/$memberId/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode({
        'preferred_slot': preferredSlot,
        'experience_level': experienceLevel,
        'trainer_preference': trainerPreference,
      }),
    );

    print(
      'UPDATE MEMBER PREF STATUS: ${response.statusCode}',
    );

    print(
      'UPDATE MEMBER PREF BODY: ${response.body}',
    );

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
      'DELETE MEMBER STATUS: ${response.statusCode}',
    );

    return response.statusCode == 204;
  }
}
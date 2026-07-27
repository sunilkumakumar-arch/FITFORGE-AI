import 'dart:convert';
import 'package:http/http.dart' as http;


import '../../core/services/auth_service.dart';

class MemberPTPackageService {
  static const String baseUrl =
      'http://127.0.0.1:8000/api/v1/pt-packages';

  static Future<List<dynamic>>
      getMemberPackages() async {
    final token =
        await AuthService.getToken();

    final response = await http.get(
      Uri.parse(
        '$baseUrl/member-packages/',
      ),
      headers: {
        'Content-Type':
            'application/json',
        'Authorization':
            'Bearer $token',
      },
    );

    if (response.statusCode == 200) {

      final data = jsonDecode(response.body);

      if (data is List) {
        return data;
      }

      if (data is Map<String, dynamic>) {
        return data['results'] ?? [];
      }

      return [];
    }

    return [];
  }

  static Future<Map<String, dynamic>?>
    getMemberActivePackage(
  int memberId,
) async {

  final packages =
      await getMemberPackages();

  try {
    return packages.firstWhere(
      (package) =>
          package['member'] ==
              memberId &&
          package['is_active'] ==
              true,
    );
  } catch (_) {
    return null;
  }
} 

  static Future<bool> assignPackage({
    required int memberId,
    required int trainerAssignmentId,
    required int packageId,
    required String purchaseDate,
    required String expiryDate,
  }) async {
    final token =
        await AuthService.getToken();

    final response = await http.post(
      Uri.parse(
        '$baseUrl/member-packages/',
      ),
      headers: {
        'Content-Type':
            'application/json',
        'Authorization':
            'Bearer $token',
      },
      body: jsonEncode({
        'member': memberId,
        'trainer_assignment':
            trainerAssignmentId,
        'package': packageId,
        'purchase_date':
            purchaseDate,
        'expiry_date':
            expiryDate,
        'sessions_used': 0,
        'is_active': true,
      }),
    );

    return response.statusCode == 201;
  }
}
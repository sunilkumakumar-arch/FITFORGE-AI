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
      return jsonDecode(
        response.body,
      );
    }

    return [];
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
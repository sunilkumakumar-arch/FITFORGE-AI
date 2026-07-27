import 'dart:convert';
import 'package:http/http.dart' as http;

import '../../core/services/auth_service.dart';

class PaymentService {
  static const String baseUrl =
      'http://127.0.0.1:8000/api/v1/billing/payments/';

  static Future<List<dynamic>> getPayments() async {
    final token = await AuthService.getToken();

    final response = await http.get(
      Uri.parse(baseUrl),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );

    print('PAYMENT STATUS: ${response.statusCode}');
    print('PAYMENT BODY: ${response.body}');

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }

    return [];
  }

  static Future<bool> createPayment({
    required int memberId,
    required int membershipPlanId,
    required double amount,
    required String paymentMethod,
    required String paymentStatus,
    required String transactionId,
    required String notes,
  }) async {
    final token = await AuthService.getToken();

    final response = await http.post(
      Uri.parse(baseUrl),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode({
        'member': memberId,
        'membership_plan': membershipPlanId,
        'amount': amount,
        'payment_method': paymentMethod,
        'payment_status': paymentStatus,
        'transaction_id': transactionId,
        'notes': notes,
      }),
    );

    print('CREATE PAYMENT STATUS: ${response.statusCode}');
    print('CREATE PAYMENT BODY: ${response.body}');

    return response.statusCode == 201;
  }
}
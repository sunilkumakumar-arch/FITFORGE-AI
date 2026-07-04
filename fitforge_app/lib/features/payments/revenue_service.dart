import 'dart:convert';
import 'package:http/http.dart' as http;

import '../../core/services/auth_service.dart';

class RevenueService {
  static const String revenueUrl =
      'http://127.0.0.1:8000/api/v1/billing/payments/total_revenue/';

  static Future<double> getRevenue() async {
    final token = await AuthService.getToken();

    final response = await http.get(
      Uri.parse(revenueUrl),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );

    print(
      'REVENUE STATUS: ${response.statusCode}',
    );

    print(
      'REVENUE BODY: ${response.body}',
    );

    if (response.statusCode == 200) {
      final data =
          jsonDecode(response.body);

      return double.tryParse(
            data['total_revenue']
                .toString(),
          ) ??
          0;
    }

    return 0;
  }
}
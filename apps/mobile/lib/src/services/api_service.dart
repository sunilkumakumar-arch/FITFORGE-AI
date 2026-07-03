import 'dart:convert';
import 'dart:io';

import '../models/dashboard_model.dart';

class ApiException implements Exception {
  ApiException(this.message);
  final String message;

  @override
  String toString() => message;
}

class ApiService {
  ApiService({this.baseUrl = 'http://localhost:3000/api/v1'});

  final String baseUrl;

  Future<DashboardSummary> getDashboardSummary(String token) async {
    final client = HttpClient();
    try {
      final request = await client.getUrl(Uri.parse('$baseUrl/dashboard/summary/'));
      request.headers.set(HttpHeaders.authorizationHeader, 'Bearer $token');
      final response = await request.close();
      final payload = await response.transform(utf8.decoder).join();

      if (response.statusCode < 200 || response.statusCode >= 300) {
        throw ApiException(
          'Failed to load dashboard summary (${response.statusCode})',
        );
      }

      if (payload.isEmpty) {
        throw ApiException('Dashboard summary response was empty');
      }

      final json = jsonDecode(payload) as Map<String, dynamic>;
      return DashboardSummary.fromJson(json);
    } on ApiException {
      rethrow;
    } on SocketException {
      throw ApiException('Unable to reach the server. Check your connection.');
    } on FormatException {
      throw ApiException('Received an invalid dashboard response.');
    } catch (error) {
      throw ApiException('Failed to load dashboard summary: $error');
    } finally {
      client.close();
    }
  }
}

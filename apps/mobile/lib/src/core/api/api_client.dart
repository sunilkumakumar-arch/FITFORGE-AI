import 'dart:convert';
import 'dart:io';

class ApiClient {
  ApiClient({this.baseUrl = 'http://localhost:3000/api/v1'});

  final String baseUrl;
  String? _accessToken;

  void setToken(String? token) => _accessToken = token;

  Future<Map<String, dynamic>> get(String path) => _send('GET', path);
  Future<Map<String, dynamic>> post(String path, Map<String, dynamic> body) => _send('POST', path, body: body);

  Future<Map<String, dynamic>> _send(String method, String path, {Map<String, dynamic>? body}) async {
    final client = HttpClient();
    final request = await client.openUrl(method, Uri.parse('$baseUrl$path'));
    request.headers.contentType = ContentType.json;
    if (_accessToken != null) {
      request.headers.set(HttpHeaders.authorizationHeader, 'Bearer $_accessToken');
    }
    if (body != null) {
      request.write(jsonEncode(body));
    }
    final response = await request.close();
    final payload = await response.transform(utf8.decoder).join();
    client.close();
    if (response.statusCode >= 400) {
      throw ApiException(response.statusCode, payload);
    }
    if (payload.isEmpty) return <String, dynamic>{};
    return jsonDecode(payload) as Map<String, dynamic>;
  }
}

class ApiException implements Exception {
  ApiException(this.statusCode, this.message);
  final int statusCode;
  final String message;

  @override
  String toString() => 'ApiException($statusCode): $message';
}

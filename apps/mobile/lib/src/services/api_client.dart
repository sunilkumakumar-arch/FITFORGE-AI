import 'dart:convert';
import 'dart:io';

class ApiClient {
  ApiClient({this.baseUrl = 'http://localhost:3000/api/v1'});

  final String baseUrl;
  String? accessToken;

  Future<Map<String, dynamic>> get(String path) => _send('GET', path);
  Future<Map<String, dynamic>> post(String path, Map<String, dynamic> body) => _send('POST', path, body: body);
  Future<Map<String, dynamic>> patch(String path, Map<String, dynamic> body) => _send('PATCH', path, body: body);
  Future<Map<String, dynamic>> delete(String path) => _send('DELETE', path);

  Future<dynamic> getJson(String path) => _sendRaw('GET', path);
  Future<dynamic> getList(String path) async {
    final payload = await _sendRaw('GET', path);
    if (payload is List) return payload;
    return <dynamic>[];
  }

  Future<Map<String, dynamic>> _send(String method, String path, {Map<String, dynamic>? body}) async {
    final payload = await _sendRaw(method, path, body: body);
    if (payload is Map<String, dynamic>) return payload;
    return {};
  }

  Future<dynamic> _sendRaw(String method, String path, {Map<String, dynamic>? body}) async {
    final client = HttpClient();
    try {
      final req = await client.openUrl(method, Uri.parse('$baseUrl$path'));
      req.headers.contentType = ContentType.json;
      if (accessToken != null) {
        req.headers.set(HttpHeaders.authorizationHeader, 'Bearer $accessToken');
      }
      if (body != null) {
        req.write(jsonEncode(body));
      }
      final res = await req.close();
      final payload = await res.transform(utf8.decoder).join();
      if (payload.isEmpty) return {};
      return jsonDecode(payload);
    } finally {
      client.close();
    }
  }
}

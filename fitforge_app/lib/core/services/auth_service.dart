import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class AuthService {
  static const String baseUrl =
      'http://127.0.0.1:8000/api/v1';

  static Future<Map<String, dynamic>> login(
    String email,
    String password,
  ) async {
    final response = await http.post(
      Uri.parse('$baseUrl/token/'),
      headers: {
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'username': email,
        'password': password,
      }),
    );

    print("LOGIN STATUS: ${response.statusCode}");
    print("LOGIN BODY: ${response.body}");

    

    final data = jsonDecode(response.body);

    if (response.statusCode == 200 &&
        data.containsKey('access')) {
      final prefs =
          await SharedPreferences.getInstance();

      await prefs.setString(
        'access_token',
        data['access'],
      );

      print("TOKEN SAVED: ${data['access']}");

      
    }

    return data;
  }

  static Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();

    final token = prefs.getString('access_token');

    print("GET TOKEN: $token");

    return token;
  }
}  
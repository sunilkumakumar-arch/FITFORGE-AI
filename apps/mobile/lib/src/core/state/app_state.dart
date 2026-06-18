import 'package:flutter/foundation.dart';
import '../api/api_client.dart';

enum MobileRole { member, trainer }

class AppState extends ChangeNotifier {
  final ApiClient apiClient = ApiClient();
  MobileRole role = MobileRole.member;
  String? accessToken;
  String? refreshToken;

  bool get isAuthenticated => accessToken != null;

  Future<void> login(String email, String password) async {
    final response = await apiClient.post('/auth/login', {'email': email, 'password': password});
    accessToken = response['accessToken'] as String?;
    refreshToken = response['refreshToken'] as String?;
    apiClient.setToken(accessToken);
    notifyListeners();
  }

  void switchRole(MobileRole value) {
    role = value;
    notifyListeners();
  }

  void logout() {
    accessToken = null;
    refreshToken = null;
    apiClient.setToken(null);
    notifyListeners();
  }
}

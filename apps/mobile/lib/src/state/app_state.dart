import 'package:flutter/foundation.dart';
import '../services/api_client.dart';
enum AppRole { member, trainer }
class AppState extends ChangeNotifier { final api = ApiClient(); AppRole role = AppRole.member; String? accessToken; void setRole(AppRole value){ role=value; notifyListeners(); } Future<void> login(String email, String password) async { final tokens = await api.post('/auth/login', {'email':email,'password':password}); accessToken = tokens['accessToken'] as String?; api.accessToken = accessToken; notifyListeners(); } }

import '../../core/services/api_service.dart';
import '../../core/services/auth_service.dart';

import 'dashboard_model.dart';

class DashboardService {
  static Future<DashboardModel>
      getDashboardSummary() async {

    final token =
        await AuthService.getToken();

    final data =
        await ApiService.getDashboardSummary(
      token!,
    );

    

    return DashboardModel.fromJson(
      data,
    );
  }
}
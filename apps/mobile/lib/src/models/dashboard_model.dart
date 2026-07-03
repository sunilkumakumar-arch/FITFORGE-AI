class DashboardSummary {
  const DashboardSummary({
    required this.totalMembers,
    required this.totalEmployees,
    required this.totalTrainers,
    required this.activeMemberships,
    required this.expiredMemberships,
    required this.todayAttendance,
    required this.totalRevenue,
    required this.totalPayments,
    required this.pendingPayments,
  });

  final int totalMembers;
  final int totalEmployees;
  final int totalTrainers;
  final int activeMemberships;
  final int expiredMemberships;
  final int todayAttendance;
  final double totalRevenue;
  final int totalPayments;
  final int pendingPayments;

  factory DashboardSummary.fromJson(Map<String, dynamic> json) {
    return DashboardSummary(
      totalMembers: _asInt(json['total_members']),
      totalEmployees: _asInt(json['total_employees']),
      totalTrainers: _asInt(json['total_trainers']),
      activeMemberships: _asInt(json['active_memberships']),
      expiredMemberships: _asInt(json['expired_memberships']),
      todayAttendance: _asInt(json['today_attendance']),
      totalRevenue: _asDouble(json['total_revenue']),
      totalPayments: _asInt(json['total_payments']),
      pendingPayments: _asInt(json['pending_payments']),
    );
  }

  static int _asInt(dynamic value) {
    if (value == null) return 0;
    if (value is int) return value;
    if (value is num) return value.toInt();
    return int.tryParse(value.toString()) ?? 0;
  }

  static double _asDouble(dynamic value) {
    if (value == null) return 0;
    if (value is double) return value;
    if (value is num) return value.toDouble();
    return double.tryParse(value.toString()) ?? 0;
  }
}

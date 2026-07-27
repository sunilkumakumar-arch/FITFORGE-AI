class DashboardModel {
  final int totalMembers;
  final int totalTrainers;
  final int totalEmployees;
  final int activeMemberships;
  final int expiredMemberships;
  final int todayAttendance;
  final double totalRevenue;
  final int totalPayments;
  final int pendingPayments;

  DashboardModel({
    required this.totalMembers,
    required this.totalTrainers,
    required this.totalEmployees,
    required this.activeMemberships,
    required this.expiredMemberships,
    required this.todayAttendance,
    required this.totalRevenue,
    required this.totalPayments,
    required this.pendingPayments,
  });

  factory DashboardModel.fromJson(
    Map<String, dynamic> json,
  ) {

    
    return DashboardModel(
      totalMembers:
          json['total_members'] ?? 0,

      totalTrainers:
          json['total_trainers'] ?? 0,

      totalEmployees:
          json['total_employees'] ?? 0,

      activeMemberships:
          json['active_memberships'] ?? 0,

      expiredMemberships:
          json['expired_memberships'] ?? 0,

      todayAttendance:
          json['today_attendance'] ?? 0,

      totalRevenue:
          double.tryParse(
            json['total_revenue'].toString(),
          ) ??
          0,

      totalPayments:
          json['total_payments'] ?? 0,

      pendingPayments:
          json['pending_payments'] ?? 0,
    );
  }
}
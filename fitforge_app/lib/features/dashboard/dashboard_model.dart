class DashboardModel {
  final int totalMembers;
  final int totalTrainers;

  DashboardModel({
    required this.totalMembers,
    required this.totalTrainers,
  });

  factory DashboardModel.fromJson(
      Map<String, dynamic> json) {
    return DashboardModel(
      totalMembers: json['total_members'] ?? 0,
      totalTrainers: json['total_trainers'] ?? 0,
    );
  }
}
import 'package:flutter/material.dart';

class AttendanceDetailsScreen
    extends StatelessWidget {
  final Map<String, dynamic>
      attendance;

  const AttendanceDetailsScreen({
    super.key,
    required this.attendance,
  });

  Widget infoTile(
    String title,
    String value,
  ) {
    return Card(
      child: ListTile(
        title: Text(title),
        subtitle: Text(value),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title:
            const Text('Attendance Details'),
      ),
      body: SingleChildScrollView(
        padding:
            const EdgeInsets.all(20),
        child: Column(
          children: [
            infoTile(
              'Member',
              attendance['member_name'] ??
                  '',
            ),

            infoTile(
              'Date',
              attendance[
                      'attendance_date'] ??
                  '',
            ),

            infoTile(
              'Status',
              attendance['status'] ?? '',
            ),

            infoTile(
              'Check In',
              attendance['check_in'] ?? '',
            ),

            infoTile(
              'Check Out',
              attendance['check_out']
                      ?.toString() ??
                  '-',
            ),
          ],
        ),
      ),
    );
  }
}
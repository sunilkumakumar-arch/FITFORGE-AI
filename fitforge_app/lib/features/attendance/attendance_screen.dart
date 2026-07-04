import 'package:flutter/material.dart';

import 'attendance_service.dart';
import 'mark_attendance_screen.dart';
import 'attendance_details_screen.dart';

class AttendanceScreen extends StatefulWidget {
  const AttendanceScreen({super.key});

  @override
  State<AttendanceScreen> createState() =>
      _AttendanceScreenState();
}

class _AttendanceScreenState
    extends State<AttendanceScreen> {
  List<dynamic> records = [];

  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    loadAttendance();
  }

  Future<void> loadAttendance() async {
    final data =
        await AttendanceService.getAttendance();

    if (!mounted) return;

    setState(() {
      records = data;
      isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Attendance'),
        actions: [
          IconButton(
            icon: const Icon(Icons.add),
            onPressed: () async {
              final result =
                  await Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) =>
                      const MarkAttendanceScreen(),
                ),
              );

              if (result == true) {
                loadAttendance();
              }
            },
          ),
        ],
      ),
      body: isLoading
          ? const Center(
              child:
                  CircularProgressIndicator(),
            )
          : ListView.builder(
              itemCount: records.length,
              itemBuilder: (context, index) {
                final record = records[index];

                return Card(
                  margin:
                      const EdgeInsets.all(10),
                  child: ListTile(
                    title: Text(
                      record['member_name'] ??
                          '',
                    ),
                    subtitle: Text(
                      record['attendance_date'] ??
                          '',
                    ),
                    trailing: Text(
                      record['status'] ?? '',
                    ),
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) =>
                              AttendanceDetailsScreen(
                            attendance:
                                record,
                          ),
                        ),
                      );
                    },
                  ),
                );
              },
            ),
    );
  }
}
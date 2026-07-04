import 'package:flutter/material.dart';

import 'attendance_service.dart';

class MarkAttendanceScreen
    extends StatefulWidget {
  const MarkAttendanceScreen({
    super.key,
  });

  @override
  State<MarkAttendanceScreen>
      createState() =>
          _MarkAttendanceScreenState();
}

class _MarkAttendanceScreenState
    extends State<MarkAttendanceScreen> {
  final memberController =
      TextEditingController();

  final branchController =
      TextEditingController();

  Future<void> saveAttendance() async {
    final success =
        await AttendanceService
            .markAttendance(
      memberId: int.parse(
        memberController.text,
      ),
      branchId: int.parse(
        branchController.text,
      ),
    );

    if (!mounted) return;

    if (success) {
      Navigator.pop(
        context,
        true,
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title:
            const Text('Mark Attendance'),
      ),
      body: Padding(
        padding:
            const EdgeInsets.all(20),
        child: Column(
          children: [
            TextField(
              controller:
                  memberController,
              decoration:
                  const InputDecoration(
                labelText:
                    'Member ID',
              ),
            ),

            const SizedBox(height: 15),

            TextField(
              controller:
                  branchController,
              decoration:
                  const InputDecoration(
                labelText:
                    'Branch ID',
              ),
            ),

            const SizedBox(height: 25),

            SizedBox(
              width:
                  double.infinity,
              child:
                  ElevatedButton(
                onPressed:
                    saveAttendance,
                child: const Text(
                  'MARK ATTENDANCE',
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
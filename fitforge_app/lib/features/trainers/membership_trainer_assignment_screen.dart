import 'package:flutter/material.dart';

import 'trainer_assignment_service.dart';

class MembershipTrainerAssignmentScreen
    extends StatefulWidget {
  final Map<String, dynamic> member;

  const MembershipTrainerAssignmentScreen({
    super.key,
    required this.member,
  });

  @override
  State<MembershipTrainerAssignmentScreen>
      createState() =>
          _MembershipTrainerAssignmentScreenState();
}

class _MembershipTrainerAssignmentScreenState
    extends State<
        MembershipTrainerAssignmentScreen> {

  String selectedGoal = 'GENERAL_FITNESS';

  final List<String> goals = [
    'GENERAL_FITNESS',
    'WEIGHT_LOSS',
    'FAT_LOSS',
    'MUSCLE_GAIN',
    'STRENGTH',
  ];

  String selectedSlot =
      '05:00 AM';
    

  String selectedDayPattern =
         'ALL';

  String trainerPreference =
      'AUTO_ASSIGN';

  bool isLoadingTrainers = false;

  bool isSaving = false;

  List<dynamic> availableTrainers =
      [];

  Map<String, dynamic>? autoAssignedTrainer;

  dynamic selectedTrainer;

  String getBackendTime() {
  final parts = selectedSlot.split(' ');

  final timePart = parts[0];
  final period = parts[1];

  final time = timePart.split(':');

  int hour = int.parse(time[0]);
  int minute = int.parse(time[1]);

  if (period == 'PM' && hour != 12) {
    hour += 12;
  }

  if (period == 'AM' && hour == 12) {
    hour = 0;
  }

  return '${hour.toString().padLeft(2, '0')}:${minute.toString().padLeft(2, '0')}:00';
}


  

  Future<void>
      loadAvailableTrainers() async {

    setState(() {
      isLoadingTrainers = true;
      availableTrainers = [];
      selectedTrainer = null;
    });

    final trainers =
        await TrainerAssignmentService
            .getAvailableTrainers(
      goalType: selectedGoal,
      slotTime:  getBackendTime(),
      trainerLevel: '',
    );

    if (!mounted) return;

    setState(() {
      availableTrainers = trainers;
      isLoadingTrainers = false;
    });

    ScaffoldMessenger.of(context)
        .showSnackBar(
      SnackBar(
        content: Text(
          '${trainers.length} trainers found',
        ),
      ),
    );
  }

  Future<void> autoAssignTrainer() async {

    setState(() {
      isLoadingTrainers = true;
    });

    final trainer =
        await TrainerAssignmentService
            .autoAssignTrainer(
      goalType: selectedGoal,
      slotTime: getBackendTime(),
    );

    if (!mounted) return;

    setState(() {
      isLoadingTrainers = false;
    });

    if (trainer == null) {

      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
            'No trainer available',
          ),
        ),
      );

      return;
    }

    setState(() {
      autoAssignedTrainer =
          trainer;
    });

    ScaffoldMessenger.of(context)
        .showSnackBar(
      const SnackBar(
        content: Text(
          'Trainer auto assigned',
        ),
      ),
    );
  }
  

  Future<void> pickTime() async {

  final picked =
      await showTimePicker(
    context: context,
    initialTime:
        TimeOfDay.now(),
  );

  if (picked != null) {

    final hour =
        picked.hourOfPeriod == 0
            ? 12
            : picked.hourOfPeriod;

    final minute =
        picked.minute
            .toString()
            .padLeft(2, '0');

    final period =
        picked.period ==
                DayPeriod.am
            ? 'AM'
            : 'PM';

    setState(() {

      selectedSlot =
          '$hour:$minute $period';
    });
  }
}

  Future<void> saveAssignment() async {

    int? trainerId;

    if (trainerPreference ==
        'AUTO_ASSIGN') {

      if (autoAssignedTrainer ==
          null) {

        ScaffoldMessenger.of(context)
            .showSnackBar(
          const SnackBar(
            content: Text(
              'Please auto assign trainer first',
            ),
          ),
        );

        return;
      }

      trainerId =
          autoAssignedTrainer!['trainer_id'];

    } else {

      if (selectedTrainer == null) {

        ScaffoldMessenger.of(context)
            .showSnackBar(
          const SnackBar(
            content: Text(
              'Select trainer',
            ),
          ),
        );

        return;
      }

      trainerId =
          selectedTrainer['id'];
    }

    setState(() {
      isSaving = true;
    });

    print(
  'DAY PATTERN SENT: ALL_DAYS',
    );

    print('TRAINER ID = $trainerId');
    print('AUTO TRAINER = $autoAssignedTrainer');

    final assignmentId =
        await TrainerAssignmentService
            .createTrainerAssignment(
      trainerId: trainerId!,
      memberId:
          widget.member['id'],
      goalType:
          selectedGoal,
      slotTime:
           getBackendTime(),
      dayPattern: 'ALL_DAYS',
    );

    if (!mounted) return;

    setState(() {
      isSaving = false;
    });

    if (assignmentId != null) {

      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
            'Trainer Assigned Successfully',
          ),
        ),
      );

      Navigator.pop(
        context,
        true,
      );

    } else {

      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
            'Assignment Failed',
          ),
        ),
      );
    }
  }
    @override
  Widget build(BuildContext context) {

    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Trainer Assignment',
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [

            Card(
              child: ListTile(
                leading: const Icon(
                  Icons.person,
                ),
                title: Text(
                  '${widget.member['first_name']} ${widget.member['last_name']}',
                ),
                subtitle: Text(
                  widget.member['email'] ?? '',
                ),
              ),
            ),

            const SizedBox(height: 20),

DropdownButtonFormField<String>(
  value: selectedGoal,
  decoration: const InputDecoration(
    labelText: 'Goal',
    border: OutlineInputBorder(),
  ),
  items: goals.map((goal) {
    return DropdownMenuItem<String>(
      value: goal,
      child: Text(goal),
    );
  }).toList(),
  onChanged: (value) {
    setState(() {
      selectedGoal = value!;
    });
  },
),

const SizedBox(height: 20),

    InkWell(
      onTap: pickTime,
      child: InputDecorator(
        decoration:
            const InputDecoration(
          labelText:
              'Preferred Time',
          border:
              OutlineInputBorder(),
        ),
        child: Row(
          mainAxisAlignment:
              MainAxisAlignment
                  .spaceBetween,
          children: [

            Text(
              selectedSlot,
            ),

            const Icon(
              Icons.access_time,
                ),
            ],
        ),
    ),
),

            const SizedBox(height: 20),

            

            const SizedBox(height: 20),

            

            const SizedBox(height: 25),

            RadioListTile(
              value: 'AUTO_ASSIGN',
              groupValue:
                  trainerPreference,
              title: const Text(
                'Auto Assign Best Trainer',
              ),
              onChanged: (value) {
                setState(() {
                  trainerPreference =
                      value!;
                });
              },
            ),

            RadioListTile(
              value: 'MANUAL',
              groupValue:
                  trainerPreference,
              title: const Text(
                'Select Trainer Myself',
              ),
              onChanged: (value) {
                setState(() {
                  trainerPreference =
                      value!;
                });
              },
            ),

            const SizedBox(height: 20),

            if (trainerPreference ==
                'AUTO_ASSIGN')
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed:
                      autoAssignTrainer,
                  child: const Text(
                    'AUTO ASSIGN',
                  ),
                ),
              ),

            if (trainerPreference ==
                    'AUTO_ASSIGN' &&
                autoAssignedTrainer !=
                    null)
              Card(
                child: ListTile(
                  leading: const Icon(
                    Icons.fitness_center,
                  ),
                  title: Text(
                    autoAssignedTrainer![
                        'trainer_name'],
                  ),
                  subtitle: Column(
                    crossAxisAlignment:
                        CrossAxisAlignment
                            .start,
                    children: [

                      Text(
                        'Level: ${autoAssignedTrainer!['trainer_level']}',
                      ),

                      Text(
                        'Experience: ${autoAssignedTrainer!['experience_years']} Years',
                      ),

                      Text(
                        'Specialization: ${autoAssignedTrainer!['specialization']}',
                      ),

                      Text(
                        'Rating: ${autoAssignedTrainer!['rating']}',
                      ),
                    ],
                  ),
                ),
              ),

            if (trainerPreference ==
                'MANUAL')
              Column(
                children: [

                  SizedBox(
                    width:
                        double.infinity,
                    child:
                        ElevatedButton(
                      onPressed:
                          loadAvailableTrainers,
                      child: const Text(
                        'LOAD TRAINERS',
                      ),
                    ),
                  ),

                  const SizedBox(
                    height: 15,
                  ),

                  if (isLoadingTrainers)
                    const CircularProgressIndicator(),

                  if (!isLoadingTrainers &&
                      availableTrainers
                          .isNotEmpty)

                    DropdownButtonFormField<
                        dynamic>(
                      value:
                          selectedTrainer,
                      decoration:
                          const InputDecoration(
                        labelText:
                            'Trainer',
                        border:
                            OutlineInputBorder(),
                      ),
                      items:
                          availableTrainers
                              .map(
                        (trainer) {

                          return DropdownMenuItem(
                            value:
                                trainer,
                            child:
                                Text(
                              trainer[
                                  'trainer_name'],
                            ),
                          );
                        },
                      ).toList(),
                      onChanged:
                          (value) {

                        setState(() {

                          selectedTrainer =
                              value;
                        });
                      },
                    ),

                  const SizedBox(
                    height: 15,
                  ),

                  if (selectedTrainer !=
                      null)
                    Card(
                      child: ListTile(
                        title: Text(
                          selectedTrainer[
                              'trainer_name'],
                        ),
                        subtitle: Column(
                          crossAxisAlignment:
                              CrossAxisAlignment
                                  .start,
                          children: [

                            Text(
                              'Level: ${selectedTrainer['trainer_level']}',
                            ),

                            Text(
                              'Experience: ${selectedTrainer['experience_years']} Years',
                            ),

                            Text(
                              'Specialization: ${selectedTrainer['specialization']}',
                            ),

                            Text(
                              'Rating: ${selectedTrainer['rating']}',
                            ),
                          ],
                        ),
                      ),
                    ),
                ],
              ),

            const SizedBox(
              height: 30,
            ),

            SizedBox(
              width:
                  double.infinity,
              height: 50,
              child:
                  ElevatedButton(
                onPressed:
                    isSaving
                        ? null
                        : saveAssignment,
                child: isSaving
                    ? const CircularProgressIndicator()
                    : const Text(
                        'CONFIRM ASSIGNMENT',
                      ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
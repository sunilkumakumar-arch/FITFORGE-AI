import 'package:flutter/material.dart';

import 'trainer_service.dart';
import 'add_trainer_screen.dart';
import 'trainer_details_screen.dart';

class TrainersScreen extends StatefulWidget {
  const TrainersScreen({super.key});

  @override
  State<TrainersScreen> createState() =>
      _TrainersScreenState();
}

class _TrainersScreenState
    extends State<TrainersScreen> {
  List<dynamic> trainers = [];
  List<dynamic> filteredTrainers = [];

  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    loadTrainers();
  }

  Future<void> loadTrainers() async {
    final data =
        await TrainerService.getTrainers();

    if (!mounted) return;

    setState(() {
      trainers = data;
      filteredTrainers = data;
      isLoading = false;
    });
  }

  void searchTrainer(String value) {
    setState(() {
      filteredTrainers =
          trainers.where((trainer) {
        final fullName =
            '${trainer['first_name']} ${trainer['last_name']}'
                .toLowerCase();

        return fullName.contains(
          value.toLowerCase(),
        );
      }).toList();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Trainers',
        ),
        actions: [
          IconButton(
            icon: const Icon(
              Icons.add,
            ),
            onPressed: () async {
              final result =
                  await Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) =>
                      const AddTrainerScreen(),
                ),
              );

              if (result == true) {
                loadTrainers();
              }
            },
          ),
        ],
      ),
      body: Column(
        children: [
          Padding(
            padding:
                const EdgeInsets.all(16),
            child: TextField(
              onChanged: searchTrainer,
              decoration: InputDecoration(
                hintText:
                    'Search Trainer',
                prefixIcon:
                    const Icon(
                  Icons.search,
                ),
                border:
                    OutlineInputBorder(
                  borderRadius:
                      BorderRadius.circular(
                    10,
                  ),
                ),
              ),
            ),
          ),
          Expanded(
            child: isLoading
                ? const Center(
                    child:
                        CircularProgressIndicator(),
                  )
                : ListView.builder(
                    itemCount:
                        filteredTrainers
                            .length,
                    itemBuilder:
                        (context, index) {
                      final trainer =
                          filteredTrainers[
                              index];

                      return GestureDetector(
                        onTap: () async {
                          final result =
                              await Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) =>
                                  TrainerDetailsScreen(
                                trainer:
                                    trainer,
                              ),
                            ),
                          );

                          if (result ==
                              true) {
                            loadTrainers();
                          }
                        },
                        child: Card(
                          margin:
                              const EdgeInsets.symmetric(
                            horizontal:
                                16,
                            vertical: 8,
                          ),
                          child: ListTile(
                            leading:
                                const CircleAvatar(
                              child: Icon(
                                Icons
                                    .fitness_center,
                              ),
                            ),
                            title: Text(
                              '${trainer['first_name']} ${trainer['last_name']}',
                            ),
                            subtitle: Text(
                              trainer[
                                      'specialization'] ??
                                  '',
                            ),
                            trailing: Text(
                              trainer[
                                      'trainer_code'] ??
                                  '',
                            ),
                          ),
                        ),
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }
}
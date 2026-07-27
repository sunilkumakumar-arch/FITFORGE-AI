import 'package:flutter/material.dart';

import '../members/member_service.dart';
import '../memberships/membership_service.dart';
import '../trainers/membership_trainer_assignment_screen.dart';

class AddPaymentScreen extends StatefulWidget {
  final Map<String, dynamic>? member;

  const AddPaymentScreen({
    super.key,
    this.member,
  });

  @override
  State<AddPaymentScreen> createState() =>
      _AddPaymentScreenState();
}

class _AddPaymentScreenState
    extends State<AddPaymentScreen> {
  final memberIdController =
      TextEditingController();

  final transactionController =
      TextEditingController();

  final notesController =
      TextEditingController();

  Map<String, dynamic>? member;

  List<dynamic> plans = [];

  dynamic selectedPlan;

  String paymentMethod = 'Cash';

  String paymentStatus = 'Paid';

  bool isLoadingPlans = true;

  @override
  void initState() {
    super.initState();

    loadPlans();

    if (widget.member != null) {
      member = widget.member;

      memberIdController.text =
          widget.member!['id'].toString();
    }
  }

  Future<void> loadPlans() async {
    final data =
        await MembershipService
            .getMembershipPlans();

    if (!mounted) return;

    setState(() {
      plans = data;
      selectedPlan = null;
      isLoadingPlans = false;
    });
  }

  Future<void> findMember() async {
    if (memberIdController.text.isEmpty) {
      return;
    }

    final result =
        await MemberService.getMemberById(
      int.parse(memberIdController.text),
    );

    if (!mounted) return;

    setState(() {
      member = result;
    });
  }

  String maskPhone(String phone) {
    if (phone.length < 4) {
      return phone;
    }

    return "******${phone.substring(phone.length - 4)}";
  }

  Future<void> savePayment() async {
  if (member == null) {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Select Member'),
      ),
    );
    return;
  }

  if (selectedPlan == null) {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Select Membership Plan'),
      ),
    );
    return;
  }

  final success =
    await MembershipService.purchaseMembership(
  memberId: member!['id'],
  planId: selectedPlan['id'],
  amountPaid: double.parse(
    selectedPlan['price'].toString(),
  ),
  paymentMethod: paymentMethod,
  transactionId: transactionController.text,
  notes: notesController.text,
);

  if (!mounted) return;

  if (success) {
    final trainerAssigned =
        await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) =>
            MembershipTrainerAssignmentScreen(
          member: member!,
        ),
      ),
    );

    if (!mounted) return;

    if (trainerAssigned == true) {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
            'Membership & Trainer Assigned Successfully',
          ),
        ),
      );

      Navigator.pop(
        context,
        true,
      );
    }
  } else {
    ScaffoldMessenger.of(context)
        .showSnackBar(
      const SnackBar(
        content: Text(
          'Failed To Save Payment',
        ),
      ),
    );
  }
}

  @override
  Widget build(
    BuildContext context,
  ) {
    return Scaffold(
      appBar: AppBar(
        title:
            const Text('Add Payment'),
      ),
      body: isLoadingPlans
          ? const Center(
              child:
                  CircularProgressIndicator(),
            )
          : SingleChildScrollView(
              padding:
                  const EdgeInsets.all(20),
              child: Column(
                children: [
                  Row(
                    children: [
                      Expanded(
                        child: TextField(
                          controller:
                              memberIdController,
                          keyboardType:
                              TextInputType.number,
                          decoration:
                              const InputDecoration(
                            labelText:
                                'Member ID',
                            border:
                                OutlineInputBorder(),
                          ),
                        ),
                      ),
                      const SizedBox(
                        width: 10,
                      ),
                      ElevatedButton(
                        onPressed:
                            findMember,
                        child:
                            const Text(
                          'Find',
                        ),
                      ),
                    ],
                  ),

                  const SizedBox(
                    height: 20,
                  ),

                  if (member != null)
                    Card(
                      child: ListTile(
                        leading: const Icon(
                          Icons.person,
                        ),
                        title: Text(
                          '${member!['first_name']} ${member!['last_name']}',
                        ),
                        subtitle: Text(
                          maskPhone(
                            member!['phone']
                                .toString(),
                          ),
                        ),
                      ),
                    ),

                  const SizedBox(
                    height: 20,
                  ),

                  DropdownButtonFormField<dynamic>(
                    value: selectedPlan,
                    decoration:
                        const InputDecoration(
                      labelText:
                          'Membership Plan',
                      border:
                          OutlineInputBorder(),
                    ),
                    items: plans.map((plan) {
                      return DropdownMenuItem<dynamic>(
                        value: plan,
                        child: Text(
                          '${plan['name']} - ₹${plan['price']}',
                        ),
                      );
                    }).toList(),
                    onChanged: (value) {
                      setState(() {
                        selectedPlan = value;
                      });
                    },
                  ),

                  const SizedBox(
                    height: 20,
                  ),

                  if (selectedPlan != null)
                    Card(
                      child: ListTile(
                        title: Text(
                          selectedPlan[
                              'name'],
                        ),
                        subtitle: Text(
                          'Duration: ${selectedPlan['duration_days']} Days',
                        ),
                        trailing: Text(
                          '₹${selectedPlan['price']}',
                        ),
                      ),
                    ),

                  const SizedBox(
                    height: 20,
                  ),

                  TextField(
                    controller:
                        transactionController,
                    decoration:
                        const InputDecoration(
                      labelText:
                          'Transaction ID',
                      border:
                          OutlineInputBorder(),
                    ),
                  ),

                  const SizedBox(
                    height: 20,
                  ),

                  TextField(
                    controller:
                        notesController,
                    maxLines: 3,
                    decoration:
                        const InputDecoration(
                      labelText:
                          'Notes',
                      border:
                          OutlineInputBorder(),
                    ),
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
                          savePayment,
                      child:
                          const Text(
                        'SAVE PAYMENT',
                      ),
                    ),
                  ),
                ],
              ),
            ),
    );
  }
}
import 'package:flutter/material.dart';
import 'add_member_screen.dart';
import 'member_details_screen.dart';
import 'member_service.dart';

class MembersScreen extends StatefulWidget {
  const MembersScreen({super.key});

  @override
  State<MembersScreen> createState() =>
      _MembersScreenState();
}

class _MembersScreenState
    extends State<MembersScreen> {
  List<dynamic> members = [];
  List<dynamic> filteredMembers = [];

  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    loadMembers();
  }

  Future<void> loadMembers() async {
    final data =
        await MemberService.getMembers();

    setState(() {
      members = data;
      filteredMembers = data;
      isLoading = false;
    });
  }

  void searchMembers(String value) {
    setState(() {
      filteredMembers = members.where((member) {
        final fullName =
            '${member['first_name']} ${member['last_name']}'
                .toLowerCase();

        final email =
            (member['email'] ?? '')
                .toString()
                .toLowerCase();

        return fullName.contains(
                value.toLowerCase()) ||
            email.contains(
                value.toLowerCase());
      }).toList();
    });
  }

  Future<void> openAddMember() async {
    final result = await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => const AddMemberScreen(),
      ),
    );

    if (result == true) {
      loadMembers();
    }
  }

  Future<void> deleteMember(
      Map<String, dynamic> member) async {
    final confirm =
        await showDialog<bool>(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: const Text(
            'Delete Member',
          ),
          content: Text(
            'Are you sure you want to delete\n\n${member['first_name']} ${member['last_name']}?\n\nThis action cannot be undone.',
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.pop(
                  context,
                  false,
                );
              },
              child: const Text(
                'Cancel',
              ),
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.pop(
                  context,
                  true,
                );
              },
              child: const Text(
                'Delete',
              ),
            ),
          ],
        );
      },
    );

    if (confirm != true) return;

    final success =
        await MemberService.deleteMember(
      member['id'],
    );

    if (success) {
      loadMembers();

      if (!mounted) return;

      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
            'Member Deleted Successfully',
          ),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Members'),
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                ElevatedButton.icon(
                  onPressed: openAddMember,
                  icon: const Icon(Icons.add),
                  label: const Text(
                    'Add Member',
                  ),
                ),
                const SizedBox(width: 20),
                Expanded(
                  child: TextField(
                    onChanged:
                        searchMembers,
                    decoration:
                        InputDecoration(
                      hintText:
                          'Search Member',
                      prefixIcon:
                          const Icon(
                              Icons.search),
                      border:
                          OutlineInputBorder(
                        borderRadius:
                            BorderRadius
                                .circular(
                                    10),
                      ),
                    ),
                  ),
                ),
              ],
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
                        filteredMembers.length,
                    itemBuilder:
                        (context, index) {
                      final member =
                          filteredMembers[
                              index];

                      return Card(
                        margin:
                            const EdgeInsets
                                .symmetric(
                          horizontal: 16,
                          vertical: 8,
                        ),
                        child: InkWell(
                          onTap: () async {
                            final result =
                                await Navigator
                                    .push(
                              context,
                              MaterialPageRoute(
                                builder: (_) =>
                                    MemberDetailsScreen(
                                  member:
                                      member,
                                ),
                              ),
                            );

                            if (result ==
                                true) {
                              loadMembers();
                            }
                          },
                          child: ListTile(
                            leading:
                                const CircleAvatar(
                              child: Icon(
                                Icons.person,
                              ),
                            ),
                            title: Text(
                              '${member['first_name']} ${member['last_name']}',
                            ),
                            subtitle: Text(
                              member['email'] ??
                                  '',
                            ),
                            trailing: Row(
                              mainAxisSize:
                                  MainAxisSize
                                      .min,
                              children: [
                                IconButton(
                                  icon:
                                      const Icon(
                                    Icons.edit,
                                  ),
                                  onPressed:
                                      () {},
                                ),
                                IconButton(
                                  icon:
                                      const Icon(
                                    Icons.delete,
                                    color:
                                        Colors.red,
                                  ),
                                  onPressed:
                                      () {
                                    deleteMember(
                                      member,
                                    );
                                  },
                                ),
                              ],
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
import 'package:flutter/material.dart';

import 'pt_package_service.dart';
import 'add_pt_package_screen.dart';
import 'edit_pt_package_screen.dart';
import 'assign_pt_package_screen.dart';
import 'member_pt_packages_screen.dart';

class PTPackageScreen extends StatefulWidget {
  const PTPackageScreen({super.key});

  @override
  State<PTPackageScreen> createState() =>
      _PTPackageScreenState();
}

class _PTPackageScreenState
    extends State<PTPackageScreen> {
  bool isLoading = true;

  List<dynamic> packages = [];

  String? errorMessage;

  @override
  void initState() {
    super.initState();
    loadPackages();
  }

  Future<void> loadPackages() async {
    setState(() {
      isLoading = true;
      errorMessage = null;
    });

    try {
      final data =
          await PTPackageService.getPackages();

      if (!mounted) return;

      setState(() {
        packages = data
            .where(
              (package) =>
                  package['is_active'] == true,
            )
            .toList();

        isLoading = false;
      });
    } catch (e) {
      if (!mounted) return;

      setState(() {
        errorMessage =
            'Failed to load PT Packages';
        isLoading = false;
      });
    }
  }

  Future<void> openAddPackageScreen() async {
    final result = await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) =>
            const AddPTPackageScreen(),
      ),
    );

    if (result == true) {
      loadPackages();
    }
  }

  Future<void> openEditPackageScreen(
    Map<String, dynamic> package,
  ) async {
    final result = await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) =>
            EditPTPackageScreen(
          package: package,
        ),
      ),
    );

    if (result == true) {
      loadPackages();
    }
  }

  Future<void> openAssignPackageScreen() async {
    final result = await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) =>
            const AssignPTPackageScreen(),
      ),
    );

    if (result == true) {
      loadPackages();
    }
  }

  Future<void> openAssignedPackagesScreen() async {
    await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) =>
            const MemberPTPackagesScreen(),
      ),
    );
  }

  Future<void> deactivatePackage(
    Map<String, dynamic> package,
  ) async {
    final confirm =
        await showDialog<bool>(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: const Text(
            'Deactivate Package',
          ),
          content: Text(
            'Deactivate ${package['name']}?',
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
                'Deactivate',
              ),
            ),
          ],
        );
      },
    );

    if (confirm != true) {
      return;
    }

    final success =
        await PTPackageService
            .deactivatePackage(
      package['id'],
    );

    if (!mounted) return;

    if (success) {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
            'Package Deactivated',
          ),
        ),
      );

      loadPackages();
    } else {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
            'Failed to deactivate package',
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
          'PT Packages',
        ),
        actions: [
          IconButton(
            tooltip: 'Assign Package',
            icon: const Icon(
              Icons.assignment_ind,
            ),
            onPressed:
                openAssignPackageScreen,
          ),
          IconButton(
            tooltip:
                'Assigned Packages',
            icon: const Icon(
              Icons.list_alt,
            ),
            onPressed:
                openAssignedPackagesScreen,
          ),
          IconButton(
            icon: const Icon(
              Icons.add,
            ),
            onPressed:
                openAddPackageScreen,
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: loadPackages,
        child: _buildBody(),
      ),
    );
  }

  Widget _buildBody() {
    if (isLoading) {
      return const Center(
        child:
            CircularProgressIndicator(),
      );
    }

    if (errorMessage != null) {
      return Center(
        child: Column(
          mainAxisAlignment:
              MainAxisAlignment.center,
          children: [
            Text(errorMessage!),
            const SizedBox(
              height: 16,
            ),
            ElevatedButton(
              onPressed:
                  loadPackages,
              child: const Text(
                'Retry',
              ),
            ),
          ],
        ),
      );
    }

    if (packages.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment:
              MainAxisAlignment.center,
          children: [
            const Text(
              'No PT Packages Found',
            ),
            const SizedBox(
              height: 16,
            ),
            ElevatedButton.icon(
              onPressed:
                  openAddPackageScreen,
              icon: const Icon(
                Icons.add,
              ),
              label: const Text(
                'Create First Package',
              ),
            ),
          ],
        ),
      );
    }

    return ListView.builder(
      physics:
          const AlwaysScrollableScrollPhysics(),
      itemCount: packages.length,
      itemBuilder: (
        context,
        index,
      ) {
        final package =
            packages[index];

        return Card(
          margin:
              const EdgeInsets.symmetric(
            horizontal: 12,
            vertical: 6,
          ),
          child: ListTile(
            leading: const Icon(
              Icons.workspace_premium,
            ),
            title: Text(
              package['name'] ?? '',
            ),
            subtitle: Column(
              crossAxisAlignment:
                  CrossAxisAlignment.start,
              children: [
                Text(
                  'Sessions: ${package['total_sessions']}',
                ),
                Text(
                  'Validity: ${package['validity_days']} Days',
                ),
                if ((package['description'] ?? '')
                    .toString()
                    .isNotEmpty)
                  Text(
                    package['description'],
                  ),
              ],
            ),
            trailing: Row(
              mainAxisSize:
                  MainAxisSize.min,
              children: [
                Text(
                  '₹${package['price']}',
                  style: const TextStyle(
                    fontWeight:
                        FontWeight.bold,
                    fontSize: 16,
                  ),
                ),
                IconButton(
                  icon: const Icon(
                    Icons.edit,
                  ),
                  onPressed: () =>
                      openEditPackageScreen(
                    package,
                  ),
                ),
                IconButton(
                  icon: const Icon(
                    Icons.delete_outline,
                  ),
                  onPressed: () =>
                      deactivatePackage(
                    package,
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}
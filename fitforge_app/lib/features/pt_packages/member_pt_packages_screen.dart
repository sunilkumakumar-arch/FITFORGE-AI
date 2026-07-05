import 'package:flutter/material.dart';

import 'member_pt_package_service.dart';

class MemberPTPackagesScreen
    extends StatefulWidget {
  const MemberPTPackagesScreen({
    super.key,
  });

  @override
  State<MemberPTPackagesScreen>
      createState() =>
          _MemberPTPackagesScreenState();
}

class _MemberPTPackagesScreenState
    extends State<
        MemberPTPackagesScreen> {
  bool isLoading = true;

  List<dynamic> packages = [];

  @override
  void initState() {
    super.initState();
    loadPackages();
  }

  Future<void> loadPackages() async {
    final data =
        await MemberPTPackageService
            .getMemberPackages();

    if (!mounted) return;

    setState(() {
      packages = data;
      isLoading = false;
    });
  }

  @override
  Widget build(
    BuildContext context,
  ) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Assigned PT Packages',
        ),
      ),
      body: isLoading
          ? const Center(
              child:
                  CircularProgressIndicator(),
            )
          : ListView.builder(
              itemCount:
                  packages.length,
              itemBuilder:
                  (context, index) {
                final item =
                    packages[index];

                return Card(
                  margin:
                      const EdgeInsets
                          .all(8),
                  child: ListTile(
                    title: Text(
                      item[
                              'package_name'] ??
                          '',
                    ),
                    subtitle: Text(
                      '${item['member_name']}'
                      '\nRemaining Sessions: '
                      '${item['sessions_remaining']}',
                    ),
                  ),
                );
              },
            ),
    );
  }
}
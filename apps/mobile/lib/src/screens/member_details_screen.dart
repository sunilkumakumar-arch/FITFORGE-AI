import 'package:flutter/material.dart';
import '../app.dart';
import '../state/app_state.dart';

class MemberDetailsScreen extends StatefulWidget {
  const MemberDetailsScreen({super.key, this.memberId});

  final String? memberId;

  @override
  State<MemberDetailsScreen> createState() => _MemberDetailsScreenState();
}

class _MemberDetailsScreenState extends State<MemberDetailsScreen> {
  Map<String, dynamic>? summary;
  String? error;
  bool loading = true;
  String? resolvedMemberId;
  final memberLookup = TextEditingController();

  @override
  void dispose() {
    memberLookup.dispose();
    super.dispose();
  }

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (widget.memberId != null) {
        _loadSummary(memberId: widget.memberId);
      } else if (AppScope.of(context).role == AppRole.member) {
        _loadSummary();
      } else {
        setState(() => loading = false);
      }
    });
  }

  Future<void> _loadSummary({String? memberId}) async {
    setState(() {
      loading = true;
      error = null;
    });

    try {
      final api = AppScope.of(context).api;
      final lookupId = memberLookup.text.trim();
      final resolvedId = memberId ??
          (lookupId.isNotEmpty ? lookupId : null) ??
          (await api.get('/auth/me'))['id'] as String?;
      if (resolvedId == null || resolvedId.isEmpty) {
        throw Exception('Member ID is required');
      }

      final data = await api.get('/members/$resolvedId/summary');
      if (!mounted) return;
      setState(() {
        resolvedMemberId = resolvedId;
        summary = data;
        loading = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        error = e.toString();
        loading = false;
      });
    }
  }

  Map<String, dynamic> _section(String key) => (summary?[key] as Map<String, dynamic>?) ?? {};

  String _text(dynamic value, {String fallback = 'Not available'}) {
    if (value == null) return fallback;
    final text = value.toString().trim();
    return text.isEmpty ? fallback : text;
  }

  String _formatDate(dynamic value) {
    if (value == null) return 'Not available';
    final parsed = DateTime.tryParse(value.toString());
    if (parsed == null) return value.toString();
    return '${parsed.year}-${parsed.month.toString().padLeft(2, '0')}-${parsed.day.toString().padLeft(2, '0')}';
  }

  Future<void> _editMember() async {
    final member = _section('member');
    final firstName = TextEditingController(text: _text(member['firstName'], fallback: ''));
    final lastName = TextEditingController(text: _text(member['lastName'], fallback: ''));
    final email = TextEditingController(text: _text(member['email'], fallback: ''));
    final phone = TextEditingController(text: _text(member['phone'], fallback: ''));

    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Edit Member'),
        content: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(controller: firstName, decoration: const InputDecoration(labelText: 'First Name')),
              TextField(controller: lastName, decoration: const InputDecoration(labelText: 'Last Name')),
              TextField(controller: email, decoration: const InputDecoration(labelText: 'Email')),
              TextField(controller: phone, decoration: const InputDecoration(labelText: 'Phone')),
            ],
          ),
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context, false), child: const Text('Cancel')),
          FilledButton(onPressed: () => Navigator.pop(context, true), child: const Text('Save')),
        ],
      ),
    );

    if (confirmed != true || resolvedMemberId == null) return;

    await AppScope.of(context).api.patch('/users/$resolvedMemberId', {
      'firstName': firstName.text.trim(),
      'lastName': lastName.text.trim(),
      'email': email.text.trim(),
      if (phone.text.trim().isNotEmpty) 'phone': phone.text.trim(),
    });

    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Member updated')));
    await _loadSummary();
  }

  Future<void> _deleteMember() async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Delete Member'),
        content: const Text('This action cannot be undone. Delete this member?'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context, false), child: const Text('Cancel')),
          FilledButton(onPressed: () => Navigator.pop(context, true), child: const Text('Delete')),
        ],
      ),
    );

    if (confirmed != true || resolvedMemberId == null) return;

    await AppScope.of(context).api.delete('/users/$resolvedMemberId');
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Member deleted')));
    Navigator.pop(context);
  }

  Future<void> _assignMembership() async {
    final organizationId = TextEditingController();
    final branchId = TextEditingController();
    final planId = TextEditingController();

    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Assign Membership'),
        content: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(controller: organizationId, decoration: const InputDecoration(labelText: 'Organization ID')),
              TextField(controller: branchId, decoration: const InputDecoration(labelText: 'Branch ID')),
              TextField(controller: planId, decoration: const InputDecoration(labelText: 'Membership Plan ID')),
            ],
          ),
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context, false), child: const Text('Cancel')),
          FilledButton(onPressed: () => Navigator.pop(context, true), child: const Text('Assign')),
        ],
      ),
    );

    if (confirmed != true || resolvedMemberId == null) return;

    await AppScope.of(context).api.post('/memberships', {
      'organizationId': organizationId.text.trim(),
      'branchId': branchId.text.trim(),
      'memberId': resolvedMemberId,
      'planId': planId.text.trim(),
      'activateImmediately': true,
    });

    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Membership assigned')));
    await _loadSummary();
  }

  Widget _infoSection(String title, List<MapEntry<String, String>> rows) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(title, style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: 12),
            for (final row in rows)
              Padding(
                padding: const EdgeInsets.only(bottom: 8),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    SizedBox(width: 140, child: Text(row.key, style: const TextStyle(fontWeight: FontWeight.w600))),
                    Expanded(child: Text(row.value)),
                  ],
                ),
              ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final member = _section('member');
    final membership = _section('membership');
    final trainer = _section('trainer');
    final ptPackage = _section('ptPackage');

    return Scaffold(
      appBar: AppBar(
        title: const Text('Member Details'),
        actions: [
          IconButton(tooltip: 'Refresh', onPressed: loading || summary == null ? null : () => _loadSummary(), icon: const Icon(Icons.refresh)),
          PopupMenuButton<String>(
            onSelected: (value) {
              if (value == 'edit') _editMember();
              if (value == 'delete') _deleteMember();
              if (value == 'assign') _assignMembership();
            },
            itemBuilder: (context) => const [
              PopupMenuItem(value: 'edit', child: Text('Edit Member')),
              PopupMenuItem(value: 'assign', child: Text('Assign Membership')),
              PopupMenuItem(value: 'delete', child: Text('Delete Member')),
            ],
          ),
        ],
      ),
      body: loading
          ? const Center(child: CircularProgressIndicator())
          : summary == null
              ? ListView(
                  padding: const EdgeInsets.all(16),
                  children: [
                    Text('Enter a member ID to load the summary dashboard.', style: Theme.of(context).textTheme.titleMedium),
                    const SizedBox(height: 16),
                    TextField(controller: memberLookup, decoration: const InputDecoration(labelText: 'Member ID')),
                    const SizedBox(height: 16),
                    FilledButton(onPressed: () => _loadSummary(), child: const Text('Load Member Summary')),
                    if (error != null) ...[
                      const SizedBox(height: 16),
                      Text(error!, style: TextStyle(color: Theme.of(context).colorScheme.error)),
                    ],
                  ],
                )
              : error != null
              ? Center(
                  child: Padding(
                    padding: const EdgeInsets.all(24),
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Text(error!, textAlign: TextAlign.center),
                        const SizedBox(height: 16),
                        FilledButton(onPressed: _loadSummary, child: const Text('Retry')),
                      ],
                    ),
                  ),
                )
              : RefreshIndicator(
                  onRefresh: _loadSummary,
                  child: ListView(
                    padding: const EdgeInsets.all(16),
                    children: [
                      _infoSection('Member Information', [
                        MapEntry('Name', '${_text(member['firstName'], fallback: '')} ${_text(member['lastName'], fallback: '')}'.trim()),
                        MapEntry('Email', _text(member['email'])),
                        MapEntry('Phone', _text(member['phone'])),
                        MapEntry('Status', _text(member['status'])),
                      ]),
                      _infoSection('Membership Information', [
                        MapEntry('Membership Plan', _text(membership['planName'])),
                        MapEntry('Membership Status', _text(membership['status'])),
                        MapEntry('Membership Expiry', _formatDate(membership['expiry'])),
                        MapEntry('Remaining Days', _text(membership['remainingDays'], fallback: '0')),
                      ]),
                      _infoSection('Trainer Information', [
                        MapEntry('Assigned Trainer', trainer['firstName'] == null && trainer['lastName'] == null
                            ? 'Not assigned'
                            : '${_text(trainer['firstName'], fallback: '')} ${_text(trainer['lastName'], fallback: '')}'.trim()),
                      ]),
                      _infoSection('PT Package Information', [
                        MapEntry('PT Package', _text(ptPackage['name'])),
                        MapEntry('Remaining Sessions', _text(ptPackage['remainingSessions'], fallback: '0')),
                        MapEntry('PT Package Expiry', _formatDate(ptPackage['expiry'])),
                      ]),
                      const SizedBox(height: 8),
                      FilledButton.icon(
                        onPressed: _assignMembership,
                        icon: const Icon(Icons.card_membership),
                        label: const Text('Assign Membership'),
                      ),
                      const SizedBox(height: 8),
                      OutlinedButton.icon(
                        onPressed: _editMember,
                        icon: const Icon(Icons.edit),
                        label: const Text('Edit Member'),
                      ),
                      const SizedBox(height: 8),
                      OutlinedButton.icon(
                        onPressed: _deleteMember,
                        icon: const Icon(Icons.delete_outline),
                        label: const Text('Delete Member'),
                      ),
                    ],
                  ),
                ),
    );
  }
}

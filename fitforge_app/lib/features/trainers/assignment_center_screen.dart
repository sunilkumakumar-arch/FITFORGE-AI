import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'trainer_service.dart';
import 'assign_member_screen.dart';
import 'membership_trainer_assignment_screen.dart';

class AssignmentCenterScreen extends StatefulWidget {
  const AssignmentCenterScreen({Key? key}) : super(key: key);

  @override
  State<AssignmentCenterScreen> createState() => _AssignmentCenterScreenState();
}

class _AssignmentCenterScreenState extends State<AssignmentCenterScreen> {
  List<Map<String, dynamic>> _trainers = [];
  bool _isLoading = true;
  bool _hasError = false;
  String _searchText = '';

  @override
  void initState() {
    super.initState();
    _fetchTrainers();
  }

  Future<void> _fetchTrainers() async {
    setState(() {
      _isLoading = true;
      _hasError = false;
    });
    try {
      final data = await TrainerService.getAssignmentCenter();
      if (!mounted) return;
      setState(() {
        _trainers = List<Map<String, dynamic>>.from(data);
        _isLoading = false;
        _hasError = false;
      });
    } catch (_) {
      if (!mounted) return;
      setState(() {
        _isLoading = false;
        _hasError = true;
      });
    }
  }

  void _onSearchChanged(String text) {
    setState(() {
      _searchText = text.trim().toLowerCase();
    });
  }

  List<Map<String, dynamic>> get _filteredTrainers {
    if (_searchText.isEmpty) return _trainers;
    return _trainers.where((trainer) {
      final name = (trainer['trainer_name'] as String).toLowerCase();
      final code = (trainer['trainer_code'] as String).toLowerCase();
      return name.contains(_searchText) || code.contains(_searchText);
    }).toList();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(
        backgroundColor: theme.colorScheme.surface,
        elevation: 1,
        centerTitle: false,
        systemOverlayStyle: SystemUiOverlayStyle.light,
        title: Text(
          'Assignment Center',
          style: theme.textTheme.titleLarge?.copyWith(
            color: theme.colorScheme.onSurface,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),
      body: SafeArea(
        child: LayoutBuilder(
          builder: (context, constraints) {
            return RefreshIndicator(
              onRefresh: _fetchTrainers,
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  children: [
                    _SearchBar(onChanged: _onSearchChanged),
                    const SizedBox(height: 12),
                    Expanded(
                      child: Builder(
                        builder: (context) {
                          if (_isLoading) return const _LoadingIndicator();
                          if (_hasError) {
                            return Center(
                              child: _ErrorRetryButton(
                                onPressed: _fetchTrainers,
                              ),
                            );
                          }
                          final trainers = _filteredTrainers;
                          if (trainers.isEmpty) return const _NoTrainersFound();

                          return ListView.builder(
                            physics: const AlwaysScrollableScrollPhysics(),
                            itemCount: trainers.length,
                            itemBuilder: (_, index) {
                              return _TrainerCard(
                                key: ValueKey(trainers[index]['trainer_id']),
                                trainer: trainers[index],
                                onAssignMember: () {
                                  Navigator.push(
                                    context,
                                    MaterialPageRoute(
                                      builder: (_) => AssignMemberScreen(
                                        trainer: trainers[index],
                                      ),
                                    ),
                                  );
                                },
                              );
                            },
                          );
                        },
                      ),
                    ),
                  ],
                ),
              ),
            );
          },
        ),
      ),
    );
  }
}

class _SearchBar extends StatelessWidget {
  final ValueChanged<String> onChanged;

  const _SearchBar({Key? key, required this.onChanged}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return TextField(
      onChanged: onChanged,
      autocorrect: false,
      textInputAction: TextInputAction.search,
      keyboardType: TextInputType.text,
      decoration: InputDecoration(
        hintText: 'Search trainer by name or code',
        prefixIcon: const Icon(Icons.search),
        filled: true,
        fillColor: theme.colorScheme.surfaceVariant,
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(18),
          borderSide: BorderSide(color: theme.colorScheme.outlineVariant),
        ),
      ),
      style: theme.textTheme.bodyLarge,
    );
  }
}

class _TrainerCard extends StatefulWidget {
  final Map<String, dynamic> trainer;
  final VoidCallback onAssignMember;

  const _TrainerCard({
    Key? key,
    required this.trainer,
    required this.onAssignMember,
  }) : super(key: key);

  @override
  State<_TrainerCard> createState() => _TrainerCardState();
}

class _TrainerCardState extends State<_TrainerCard> {
  bool _membershipExpanded = false;
  bool _ptClientsExpanded = false;

  void _toggleMembershipExpansion() {
    setState(() {
      _membershipExpanded = !_membershipExpanded;
    });
  }

  void _togglePTClientsExpansion() {
    setState(() {
      _ptClientsExpanded = !_ptClientsExpanded;
    });
  }

  Color _getUtilizationColor(double ratio) {
    if (ratio < 0.7) return Colors.green;
    if (ratio < 0.9) return Colors.orange;
    return Colors.red;
  }

  @override
  Widget build(BuildContext context) {
    final t = widget.trainer;
    final theme = Theme.of(context);
    final int capacity = t['capacity'] ?? 0;
    final int occupied = t['occupied'] ?? 0;
    final int available = t['available'] ?? 0;
    final double utilization = capacity > 0 ? occupied / capacity : 0;
    final utilizationColor = _getUtilizationColor(utilization);

    return AnimatedContainer(
      duration: const Duration(milliseconds: 350),
      margin: const EdgeInsets.symmetric(vertical: 8),
      decoration: BoxDecoration(
        color: theme.colorScheme.surface,
        borderRadius: BorderRadius.circular(18),
        boxShadow: [
          BoxShadow(
            color: theme.shadowColor.withOpacity(0.12),
            blurRadius: 10,
            offset: const Offset(0, 6),
            spreadRadius: 0,
          ),
        ],
      ),
      child: Material(
        color: Colors.transparent,
        child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _buildHeader(t, theme),
              const SizedBox(height: 12),
              _CapacitySection(
                capacity: capacity,
                occupied: occupied,
                available: available,
                utilizationRatio: utilization,
                utilizationColor: utilizationColor,
              ),
              const SizedBox(height: 16),
              _ExpandableSection(
                title: 'Membership Clients',
                clients: List<dynamic>.from(t['membership_clients'] ?? []),
                isExpanded: _membershipExpanded,
                onToggle: _toggleMembershipExpansion,
              ),
              const SizedBox(height: 16),
              _ExpandableSection(
                title: 'PT Clients',
                clients: List<dynamic>.from(t['pt_clients'] ?? []),
                isExpanded: _ptClientsExpanded,
                onToggle: _togglePTClientsExpansion,
              ),
              const SizedBox(height: 20),
              SizedBox(
                width: double.infinity,
                child: FilledButton.tonal(
                  onPressed: widget.onAssignMember,
                  style: FilledButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 14),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(18),
                    ),
                    textStyle: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w600),
                  ),
                  child: const Text('Assign Member'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildHeader(Map<String, dynamic> trainer, ThemeData theme) {
    return Row(
      children: [
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                trainer['trainer_name'] ?? '',
                style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w700, color: theme.colorScheme.onSurface),
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),
              const SizedBox(height: 4),
              Text(
                trainer['trainer_code'] ?? '',
                style: theme.textTheme.labelMedium?.copyWith(
                  letterSpacing: 1.2,
                  fontWeight: FontWeight.w600,
                  color: theme.colorScheme.outline,
                ),
              ),
            ],
          ),
        ),
        const SizedBox(width: 12),
        _StatusChip(
          label: trainer['trainer_status'] ?? '',
          isStatus: true,
        ),
        const SizedBox(width: 8),
        _StatusChip(
          label: trainer['employment_status'] ?? '',
          isStatus: false,
        ),
      ],
    );
  }
}

class _CapacitySection extends StatelessWidget {
  final int capacity;
  final int occupied;
  final int available;
  final double utilizationRatio;
  final Color utilizationColor;

  const _CapacitySection({
    Key? key,
    required this.capacity,
    required this.occupied,
    required this.available,
    required this.utilizationRatio,
    required this.utilizationColor,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final int percentage = (utilizationRatio * 100).clamp(0, 100).toInt();

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Capacity',
          style: theme.textTheme.titleSmall?.copyWith(
            fontWeight: FontWeight.w600,
            color: theme.colorScheme.primary,
          ),
        ),
        const SizedBox(height: 8),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            _SingleCapacityData(label: 'Total', value: capacity),
            _SingleCapacityData(label: 'Occupied', value: occupied),
            _SingleCapacityData(label: 'Available', value: available),
          ],
        ),
        const SizedBox(height: 12),
        ClipRRect(
          borderRadius: BorderRadius.circular(12),
          child: LinearProgressIndicator(
            value: utilizationRatio,
            minHeight: 8,
            backgroundColor: utilizationColor.withOpacity(0.3),
            valueColor: AlwaysStoppedAnimation(utilizationColor),
          ),
        ),
        const SizedBox(height: 6),
        Align(
          alignment: Alignment.centerRight,
          child: Text(
            '$percentage% Utilization',
            style: theme.textTheme.labelMedium?.copyWith(
              fontWeight: FontWeight.w700,
              color: utilizationColor,
            ),
          ),
        ),
      ],
    );
  }
}

class _SingleCapacityData extends StatelessWidget {
  final String label;
  final int value;

  const _SingleCapacityData({
    Key? key,
    required this.label,
    required this.value,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Text(
          label,
          style: theme.textTheme.labelSmall?.copyWith(color: theme.colorScheme.outline),
        ),
        const SizedBox(height: 4),
        Text(
          value.toString(),
          style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w700),
        ),
      ],
    );
  }
}

class _ExpandableSection extends StatelessWidget {
  final String title;
  final List<dynamic> clients;
  final bool isExpanded;
  final VoidCallback onToggle;

  const _ExpandableSection({
    Key? key,
    required this.title,
    required this.clients,
    required this.isExpanded,
    required this.onToggle,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Column(
      children: [
        InkWell(
          borderRadius: BorderRadius.circular(12),
          onTap: onToggle,
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 8),
            child: Row(
              children: [
                Text(
                  '$title (${clients.length})',
                  style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w700, color: theme.colorScheme.onSurface),
                ),
                const Spacer(),
                AnimatedRotation(
                  turns: isExpanded ? 0.5 : 0,
                  duration: const Duration(milliseconds: 300),
                  child: Icon(Icons.expand_more, color: theme.colorScheme.outline, size: 26),
                ),
              ],
            ),
          ),
        ),
        AnimatedCrossFade(
          firstChild: const SizedBox.shrink(),
          secondChild: Padding(
            padding: const EdgeInsets.only(top: 8),
            child: Column(
              children: clients.map((client) => _ClientTile(client: client as Map<String, dynamic>)).toList(),
            ),
          ),
          crossFadeState: isExpanded ? CrossFadeState.showSecond : CrossFadeState.showFirst,
          duration: const Duration(milliseconds: 350),
          firstCurve: Curves.easeInOut,
          secondCurve: Curves.easeInOut,
        ),
      ],
    );
  }
}

class _ClientTile extends StatelessWidget {
  final Map<String, dynamic> client;

  const _ClientTile({
    Key? key,
    required this.client,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final String name = client['name'] ?? '';

    return Card(
      margin: const EdgeInsets.symmetric(vertical: 6),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
      elevation: 0,
      color: theme.colorScheme.surfaceVariant,
      child: ListTile(
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
        leading: Icon(Icons.person, color: theme.colorScheme.primary, size: 28),
        title: Text(name, style: theme.textTheme.bodyLarge?.copyWith(fontWeight: FontWeight.w600)),
        trailing: ElevatedButton(
          onPressed: () {},
          style: ElevatedButton.styleFrom(
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            minimumSize: const Size(80, 36),
            padding: const EdgeInsets.symmetric(horizontal: 12),
          ),
          child: const Text('Reassign'),
        ),
      ),
    );
  }
}

class _NoTrainersFound extends StatelessWidget {
  const _NoTrainersFound({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.fitness_center_outlined, size: 120, color: theme.colorScheme.primary.withOpacity(0.24)),
            const SizedBox(height: 16),
            Text(
              'No Trainers Found',
              style: theme.textTheme.titleLarge?.copyWith(
                fontWeight: FontWeight.w600,
                color: theme.colorScheme.outline,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _LoadingIndicator extends StatelessWidget {
  const _LoadingIndicator({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return const Center(child: CircularProgressIndicator());
  }
}

class _ErrorRetryButton extends StatelessWidget {
  final VoidCallback onPressed;

  const _ErrorRetryButton({Key? key, required this.onPressed}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return ElevatedButton.icon(
      icon: const Icon(Icons.refresh),
      label: const Text('Retry'),
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 14),
        textStyle: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w600),
      ),
    );
  }
}

class _StatusChip extends StatelessWidget {
  final String label;
  final bool isStatus;

  const _StatusChip({
    super.key,
    required this.label,
    required this.isStatus,
  });

  Color _backgroundColor(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    switch (label.toUpperCase()) {
      case 'AVAILABLE':
        return isStatus ? Colors.green.shade100 : colorScheme.surfaceVariant;
      case 'BUSY':
        return isStatus ? Colors.orange.shade100 : colorScheme.surfaceVariant;
      case 'UNAVAILABLE':
        return isStatus ? Colors.red.shade100 : colorScheme.surfaceVariant;
      case 'ACTIVE':
        return !isStatus ? Colors.blue.shade100 : colorScheme.surfaceVariant;
      case 'INACTIVE':
        return !isStatus ? Colors.grey.shade300 : colorScheme.surfaceVariant;
      default:
        return colorScheme.surfaceVariant;
    }
  }

  Color _textColor(BuildContext context) {
    switch (label.toUpperCase()) {
      case 'AVAILABLE':
        return isStatus ? Colors.green.shade800 : Colors.black87;
      case 'BUSY':
        return isStatus ? Colors.orange.shade800 : Colors.black87;
      case 'UNAVAILABLE':
        return isStatus ? Colors.red.shade800 : Colors.black87;
      case 'ACTIVE':
        return !isStatus ? Colors.blue.shade800 : Colors.black87;
      case 'INACTIVE':
        return !isStatus ? Colors.grey.shade700 : Colors.black87;
      default:
        return Theme.of(context).colorScheme.onSurfaceVariant;
    }
  }

  @override
  Widget build(BuildContext context) {
    final bgColor = _backgroundColor(context);
    final fgColor = _textColor(context);

    return Chip(
      backgroundColor: bgColor,
      label: Text(
        label.toUpperCase(),
        style: TextStyle(
          color: fgColor,
          fontWeight: FontWeight.w700,
          fontSize: 12,
          letterSpacing: 1.25,
        ),
      ),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(14),
      ),
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
      materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
    );
  }
}


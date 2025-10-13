import 'package:flutter/material.dart';
import 'dart:math';
















void main() {
runApp(const PlannerApp());
}
















class PlannerApp extends StatefulWidget {
const PlannerApp({super.key});
















@override
State<PlannerApp> createState() => _PlannerAppState();
}
















class _PlannerAppState extends State<PlannerApp> {
ThemeMode _themeMode = ThemeMode.dark;
String _themeChoice = "Blue"; // options: Blue, Rainbow, BlueWhite
















void updateTheme(ThemeMode m, String choice) {
setState(() {
  _themeMode = m;
  _themeChoice = choice;
});
}
















@override
Widget build(BuildContext context) {
return MaterialApp(
  debugShowCheckedModeBanner: false,
  title: "Planner App",
  themeMode: _themeMode,
  theme: ThemeData.light().copyWith(
    primaryColor: Colors.indigo,
    scaffoldBackgroundColor: Colors.white,
    appBarTheme: const AppBarTheme(backgroundColor: Colors.indigo),
  ),
  darkTheme: ThemeData.dark().copyWith(
    primaryColor: Colors.indigo,
    scaffoldBackgroundColor: const Color(0xFF121212),
    appBarTheme: const AppBarTheme(backgroundColor: Colors.indigo),
  ),
  home: PlannerScreen(
    themeMode: _themeMode,
    themeChoice: _themeChoice,
    onThemeChanged: updateTheme,
  ),
);
}
}
















// ----------- New additions: categories, recurrence, classes storage ----------
// ignore: unused_field
enum EventType { fixed, flexible, breakTime,}
















enum Recurrence { none, daily, weekly, monthly }
















class PlannerEvent {
String title;
EventType eventType;
int priority; // 1 = highest, 5 = lowest (for flexible tasks) - now mutable to allow auto-prioritization
int duration; // minutes (original duration)
DateTime? startTime; // for fixed chunks (may be null for scheduled flexible)
DateTime? endTime;
final DateTime? deadline;
DateTime? eventDate; // original anchor date (if set)
Color color;
String? classTag; // link to class/commitment tag
Recurrence recurrence;
// estimation field (may be null)
int? estimatedDuration;
final PlannerEvent? sourceEvent;
















PlannerEvent({
required this.title,
required this.eventType,
required this.priority,
required this.duration,
this.startTime,
this.endTime,
this.deadline,
this.eventDate,
required this.color,
this.classTag,
this.recurrence = Recurrence.none,
this.estimatedDuration,
this.sourceEvent,
});
















PlannerEvent copyWith({
String? title,
EventType? eventType,
int? priority,
int? duration,
DateTime? startTime,
DateTime? endTime,
DateTime? deadline,
DateTime? eventDate,
Color? color,
String? classTag,
Recurrence? recurrence,
int? estimatedDuration,
PlannerEvent? sourceEvent,
}) {
return PlannerEvent(
  title: title ?? this.title,
  eventType: eventType ?? this.eventType,
  priority: priority ?? this.priority,
  duration: duration ?? this.duration,
  startTime: startTime ?? this.startTime,
  endTime: endTime ?? this.endTime,
  deadline: deadline ?? this.deadline,
  eventDate: eventDate ?? this.eventDate,
  color: color ?? this.color,
  classTag: classTag ?? this.classTag,
  recurrence: recurrence ?? this.recurrence,
  estimatedDuration: estimatedDuration ?? this.estimatedDuration,
  sourceEvent: sourceEvent ?? this.sourceEvent,
);
}
}
















/// Internal mutable copy used by the scheduling algorithm so we can
/// modify durations / remove tasks without changing original PlannerEvent objects.
class _MutableTask {
final PlannerEvent original;
int remaining; // minutes remaining
bool removed = false;
















_MutableTask(this.original) : remaining = original.duration;
}
















enum CalendarView { weekly, daily, monthly }
















class ClassItem {
final String name;
Color color;
ClassItem({required this.name, required this.color});
}
















// ----------------- PlannerScreen -----------------
class PlannerScreen extends StatefulWidget {
final ThemeMode themeMode;
final String themeChoice;
final void Function(ThemeMode, String) onThemeChanged;
















const PlannerScreen({
super.key,
required this.themeMode,
required this.themeChoice,
required this.onThemeChanged,
});
















@override
State<PlannerScreen> createState() => _PlannerScreenState();
}
















class _PlannerScreenState extends State<PlannerScreen> {
final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();
final List<PlannerEvent> _events = [];
final List<ClassItem> _classes = [];
DateTime _selectedDate = DateTime.now();
CalendarView _view = CalendarView.weekly;
















// Settings (user-editable via Settings dialog)
int breakLength = 10; // minutes for a normal inserted break
int showerLength = 15;
int mealLength = 30;
TimeOfDay workStart = const TimeOfDay(hour: 16, minute: 0);
TimeOfDay workEnd = const TimeOfDay(hour: 22, minute: 0);
int bufferBetweenEvents = 5; // minutes buffer after fixed events
int workChunkLength = 50; // amount of time spent working before a break
















// UI colors (final because we don't change them)
final Color _primaryColor = Colors.indigo;
final Color _scaffoldBackgroundColor = const Color(0xFF121212);
final Color _dayHeaderColor = Colors.indigo;
final Color _dayHeaderTodayColor = Colors.indigoAccent;
final Color _dayColumnBackground = Colors.indigo;
final Color _dayColumnTodayBackground = Colors.indigoAccent;
















String? _userName;
















// History for duration estimation: map from title (or classTag) -> list of recorded actual durations
final Map<String, List<int>> _durationHistory = {};
















// ---------------- Helper for day label ----------------
String _dayLabel(int weekday) {
const labels = {
  1: "Mon",
  2: "Tue",
  3: "Wed",
  4: "Thu",
  5: "Fri",
  6: "Sat",
  7: "Sun"
};
return labels[weekday] ?? "";
}
















@override
void initState() {
super.initState();
// Ask for user name at first open
WidgetsBinding.instance.addPostFrameCallback((_) => _promptForNameIfMissing());
}
















Future<void> _promptForNameIfMissing() async {
if (_userName != null && _userName!.isNotEmpty) return;
String tmp = "";
await showDialog(
  context: context,
  barrierDismissible: false,
  builder: (c) {
    return AlertDialog(
      title: const Text("Welcome!"),
      content: TextFormField(
        decoration: const InputDecoration(labelText: "What's your name?"),
        onChanged: (v) => tmp = v.trim(),
      ),
      actions: [
        TextButton(
          onPressed: () {
            if (tmp.isEmpty) tmp = "My";
            setState(() {
              _userName = tmp;
            });
            Navigator.pop(c);
          },
          child: const Text("OK"),
        )
      ],
    );
  },
);
}
















// ---------------- Scheduling and recurrence-aware getters ----------------
















// helper: whether event occurs on given day (checks recurrence + anchor eventDate)
bool _occursOnDay(PlannerEvent e, DateTime day) {
if (e.eventType == EventType.fixed && e.startTime != null) {
  return e.startTime!.year == day.year &&
      e.startTime!.month == day.month &&
      e.startTime!.day == day.day;
}
if (e.eventDate == null) return false;
final anchor = e.eventDate!;
if (_isSameDay(anchor, day)) return true;
switch (e.recurrence) {
  case Recurrence.none:
    return false;
  case Recurrence.daily:
    return !day.isBefore(anchor); // occurs every day after anchor
  case Recurrence.weekly:
    if (day.isBefore(anchor)) return false;
    return anchor.weekday == day.weekday;
  case Recurrence.monthly:
    if (day.isBefore(anchor)) return false;
    return anchor.day == day.day;
}
}
















bool _isSameDay(DateTime a, DateTime b) =>
  a.year == b.year && a.month == b.month && a.day == b.day;
















// ---------------- Automatic prioritization: suggested adjustments --------------
// Simple heuristic: closer deadline -> increase priority; longer estimated duration with soon deadline -> even higher priority.
void _autoPrioritizeForDay(DateTime day, List<_MutableTask> mutableTasks) {
final now = DateTime.now();
for (var mt in mutableTasks) {
  final e = mt.original;
  int suggested = e.priority;
  final deadline = e.deadline;
  final estimate = e.estimatedDuration ?? e.duration;
  if (deadline != null) {
    final minutesLeft = deadline.difference(day).inMinutes;
    if (minutesLeft <= 0) {
      suggested = max(1, suggested - 2); // due now -> higher priority
    } else if (minutesLeft <= 24 * 60) {
      suggested = max(1, suggested - 1);
    } else if (minutesLeft <= 3 * 24 * 60) {
      suggested = max(1, suggested - 0);
    }
    // if long estimate and approaching deadline, bump priority
    if (estimate >= 120 && minutesLeft <= 3 * 24 * 60) suggested = max(1, suggested - 1);
  }
  mt.original.priority = suggested;
}
}
















// ---------------- Generate schedule for a day (recurrence-aware & auto-prioritize) ----------------
List<PlannerEvent> _generateScheduleForDay(DateTime day) {
final schedule = <PlannerEvent>[];
















// 1) Get fixed events that happen on this day (including recurring fixed events if startTime anchored)
final fixedEvents = _events.where((e) => e.eventType == EventType.fixed && _occursOnDay(e, day)).toList();
fixedEvents.sort((a, b) {
  final aStart = a.startTime ?? DateTime(2100);
  final bStart = b.startTime ?? DateTime(2100);
  return aStart.compareTo(bStart);
});
schedule.addAll(fixedEvents);
















// 2) Collect flexible tasks that have eventDate equal to this day OR recurring occurrences that fall on this day
final flexibleEventsForDay = _events.where((e) =>
    e.eventType == EventType.flexible && e.eventDate != null && _occursOnDay(e, day)).toList();
















if (flexibleEventsForDay.isEmpty) {
  // Sort schedule by startTime if present
  schedule.sort((a, b) =>
      (a.startTime ?? DateTime(2100)).compareTo(b.startTime ?? DateTime(2100)));
  return schedule;
}
















// 3) Build mutable copies to apply reductions & estimation adjustments
final mutableTasks = flexibleEventsForDay.map((e) => _MutableTask(e)).toList();
















// Fill estimatedDuration using history if available
for (var t in mutableTasks) {
  final key = t.original.title.toLowerCase();
  final hist = _durationHistory[key] ?? _durationHistory[t.original.classTag ?? ""];
  if (hist != null && hist.isNotEmpty) {
    final avg = (hist.reduce((a, b) => a + b) / hist.length).round();
    t.original.estimatedDuration = avg;
    // optionally adjust remaining to estimated if we think original duration was outdated
    // keep original duration for now, but we can use estimated when deciding priority
  }
}
















// Auto-prioritize before reductions
_autoPrioritizeForDay(day, mutableTasks);
















// rest of your reduction algorithm (adapted from your original)
final mutable = mutableTasks;
DateTime cursor = DateTime(day.year, day.month, day.day, workStart.hour, workStart.minute);
final cutoff = DateTime(day.year, day.month, day.day, workEnd.hour, workEnd.minute);
















int totalAvailable = cutoff.difference(cursor).inMinutes;
















// subtract blocked time from fixed events (only portions within it)
for (var fe in fixedEvents) {
  final feStart = fe.startTime!;
  final feEnd = fe.endTime ?? fe.startTime!.add(Duration(minutes: fe.duration));
  final overlapStart = feStart.isAfter(cursor) ? feStart : cursor;
  final overlapEnd = feEnd.isBefore(cutoff) ? feEnd : cutoff;
  if (overlapEnd.isAfter(overlapStart)) {
    totalAvailable -= overlapEnd.difference(overlapStart).inMinutes;
    totalAvailable -= bufferBetweenEvents;
  }
}
if (totalAvailable < 0) totalAvailable = 0;
















int totalTaskTime = mutable.fold(0, (s, t) => s + t.remaining);
















if (totalTaskTime <= totalAvailable) {
  schedule.addAll(_allocateFlexibleIntoTimeline(day, mutable, fixedEvents));
  schedule.sort((a, b) =>
      (a.startTime ?? DateTime(2100)).compareTo(b.startTime ?? DateTime(2100)));
  return schedule;
}
















// Reduction steps (same as original). I kept steps but used the updated priority access.
void step1() {
  for (var t in mutable) {
    if (t.removed) continue;
    if (t.original.priority == 5) {
      final old = t.remaining;
      t.remaining = (t.remaining / 2).ceil();
      totalTaskTime -= (old - t.remaining);
    }
  }
}
















void step2() {
  for (var t in mutable) {
    if (t.removed) continue;
    if (t.original.priority == 4) {
      final old = t.remaining;
      t.remaining = (t.remaining / 2).ceil();
      totalTaskTime -= (old - t.remaining);
    }
  }
}
















void step3() {
  for (var t in mutable) {
    if (t.removed) continue;
    if (t.original.priority == 5) {
      t.removed = true;
      totalTaskTime -= t.remaining;
    }
  }
}
















void step4() {
  for (var t in mutable) {
    if (t.removed) continue;
    if (t.original.priority == 4) {
      t.removed = true;
      totalTaskTime -= t.remaining;
    }
  }
}
















bool step5() {
  if (breakLength <= 1) return false;
  final old = breakLength;
  breakLength = (breakLength / 2).ceil();
  return old != breakLength;
}
















void step6() {
  for (var t in mutable) {
    if (t.removed) continue;
    if (t.original.priority == 3) {
      final old = t.remaining;
      t.remaining = (t.remaining / 2).ceil();
      totalTaskTime -= (old - t.remaining);
    }
  }
}
















void step7() {
  for (var t in mutable) {
    if (t.removed) continue;
    if (t.original.priority == 3) {
      t.removed = true;
      totalTaskTime -= t.remaining;
    }
  }
}
















void step8() {
  for (var t in mutable) {
    if (t.removed) continue;
    if (t.original.priority == 2) {
      final old = t.remaining;
      t.remaining = (t.remaining / 2).ceil();
      totalTaskTime -= (old - t.remaining);
    }
  }
}
















void step9() {
  for (var t in mutable) {
    if (t.removed) continue;
    if (t.original.priority == 2) {
      t.removed = true;
      totalTaskTime -= t.remaining;
    }
  }
}
















void step10() {
  for (var t in mutable) {
    if (t.removed) continue;
    if (t.original.priority == 1) {
      final old = t.remaining;
      t.remaining = (t.remaining / 2).ceil();
      totalTaskTime -= (old - t.remaining);
    }
  }
}
















final List<Function()> orderedSteps = [
  step1,
  step2,
  step3,
  step4,
  () => step5(),
  step6,
  step7,
  step8,
  step9,
  step10
];
















for (var step in orderedSteps) {
  if (totalTaskTime <= totalAvailable) break;
  step();
  totalAvailable = _recomputeAvailableMinutes(day);
  if (totalTaskTime <= totalAvailable) break;
}
















schedule.addAll(_allocateFlexibleIntoTimeline(day, mutable, fixedEvents));
















schedule.sort((a, b) =>
    (a.startTime ?? DateTime(2100)).compareTo(b.startTime ?? DateTime(2100)));
return schedule;
}
















// Helper: recompute available minutes for comfortable interval (same as original)
int _recomputeAvailableMinutes(DateTime day) {
DateTime cursor = DateTime(day.year, day.month, day.day, workStart.hour, workStart.minute);
final cutoff = DateTime(day.year, day.month, day.day, workEnd.hour, workEnd.minute);
int available = cutoff.difference(cursor).inMinutes;
final fixedEvents = _events.where((e) => e.eventType == EventType.fixed && _occursOnDay(e, day)).toList();
for (var fe in fixedEvents) {
  final feStart = fe.startTime!;
  final feEnd = fe.endTime ?? fe.startTime!.add(Duration(minutes: fe.duration));
  final overlapStart = feStart.isAfter(cursor) ? feStart : cursor;
  final overlapEnd = feEnd.isBefore(cutoff) ? feEnd : cutoff;
  if (overlapEnd.isAfter(overlapStart)) {
    available -= overlapEnd.difference(overlapStart).inMinutes;
    available -= bufferBetweenEvents;
  }
}
if (available < 0) available = 0;
return available;
}
















// ---------------- Allocation with adaptive breaks ----------------
List<PlannerEvent> _allocateFlexibleIntoTimeline(
  DateTime day, List<_MutableTask> tasks, List<PlannerEvent> fixedEvents) {
final List<PlannerEvent> allocated = [];
















DateTime cursor = DateTime(day.year, day.month, day.day, workStart.hour, workStart.minute);
final cutoff = DateTime(day.year, day.month, day.day, workEnd.hour, workEnd.minute);
















final sortedFixed = List<PlannerEvent>.from(fixedEvents)
  ..sort((a, b) => a.startTime!.compareTo(b.startTime!));
















int fixedIdx = 0;
















void skipOverFixedEvents() {
  while (fixedIdx < sortedFixed.length) {
    final fe = sortedFixed[fixedIdx];
    final feStart = fe.startTime!;
    final feEnd = fe.endTime ?? fe.startTime!.add(Duration(minutes: fe.duration));
    if (cursor.isBefore(feStart)) {
      break;
    }
    if (cursor.isAfter(feStart) && cursor.isBefore(feEnd)) {
      cursor = feEnd.add(Duration(minutes: bufferBetweenEvents));
      fixedIdx++;
      continue;
    }
    if (!cursor.isBefore(feStart)) {
      fixedIdx++;
      continue;
    }
  }
}
















// allocate tasks in priority order (lower number = higher priority)
final remainingTasks = tasks.where((t) => !t.removed && t.remaining > 0).toList()
  ..sort((a, b) {
    final p = a.original.priority.compareTo(b.original.priority);
    if (p != 0) return p;
    // prefer shorter estimated duration earlier
    final aEst = a.original.estimatedDuration ?? a.original.duration;
    final bEst = b.original.estimatedDuration ?? b.original.duration;
    return aEst.compareTo(bEst);
  });
















// adaptive break logic:
int continuousWorkMinutes = 0;
int adaptiveBreak = breakLength;
















for (var task in remainingTasks) {
  int remaining = task.remaining;
















  while (remaining > 0 && cursor.isBefore(cutoff)) {
    skipOverFixedEvents();
















    // update adaptiveBreak based on continuousWorkMinutes
    if (continuousWorkMinutes >= 120) {
      adaptiveBreak = (breakLength * 1.5).ceil();
    } else if (continuousWorkMinutes >= 60) {
      adaptiveBreak = (breakLength * 1.25).ceil();
    } else {
      adaptiveBreak = breakLength;
    }
















    DateTime nextFixedStart = cutoff;
    if (fixedIdx < sortedFixed.length) {
      final fe = sortedFixed[fixedIdx];
      nextFixedStart = fe.startTime!;
    }
















    if (!cursor.isBefore(nextFixedStart)) {
      if (fixedIdx < sortedFixed.length) {
        final fe = sortedFixed[fixedIdx];
        final feEnd = fe.endTime ?? fe.startTime!.add(Duration(minutes: fe.duration));
        cursor = feEnd.add(Duration(minutes: bufferBetweenEvents));
        fixedIdx++;
        // reset continuous work because we had a fixed-event gap
        continuousWorkMinutes = 0;
        continue;
      } else {
        break;
      }
    }
















    final segmentEnd = nextFixedStart.isBefore(cutoff) ? nextFixedStart : cutoff;
    final freeMinutes = segmentEnd.difference(cursor).inMinutes;
    if (freeMinutes <= 0) {
      if (fixedIdx < sortedFixed.length) {
        final fe = sortedFixed[fixedIdx];
        final feEnd = fe.endTime ?? fe.startTime!.add(Duration(minutes: fe.duration));
        cursor = feEnd.add(Duration(minutes: bufferBetweenEvents));
        fixedIdx++;
        continuousWorkMinutes = 0;
        continue;
      } else {
        break;
      }
    }
















    final chunk = remaining < workChunkLength ? remaining : (workChunkLength < freeMinutes ? workChunkLength : freeMinutes);
    final end = cursor.add(Duration(minutes: chunk));
















    allocated.add(PlannerEvent(
      title: task.original.title + (remaining == task.remaining ? "" : " (cont)"),
      eventType: EventType.flexible,
      priority: task.original.priority,
      duration: chunk,
      startTime: cursor,
      endTime: end,
      deadline: task.original.deadline,
      eventDate: task.original.eventDate,
      color: task.original.color,
      classTag: task.original.classTag,
      sourceEvent: task.original,
    ));
















    cursor = end;
    remaining -= chunk;
    continuousWorkMinutes += chunk;
















    // record a pseudo "completion" when a whole task finishes — store history for estimation
    if (remaining <= 0) {
      final key = task.original.title.toLowerCase();
      _durationHistory.putIfAbsent(key, () => []).add(task.original.duration);
    }
















    // try to insert break using adaptiveBreak
    final breakEnd = cursor.add(Duration(minutes: adaptiveBreak));
    if (breakEnd.isBefore(nextFixedStart) && breakEnd.isBefore(cutoff)) {
      allocated.add(PlannerEvent(
        title: "Break",
        eventType: EventType.breakTime,
        priority: 5,
        duration: adaptiveBreak,
        startTime: cursor,
        endTime: breakEnd,
        eventDate: task.original.eventDate,
        color: Colors.green,
      ));
      cursor = breakEnd;
      // after a break continuous work resets a bit
      continuousWorkMinutes = max(0, continuousWorkMinutes - adaptiveBreak);
    } else {
      // no break inserted; continue scheduling
    }
  }
















  if (remaining > 0) {
    allocated.add(PlannerEvent(
      title: "${task.original.title} (pushed)",
      eventType: EventType.flexible,
      priority: task.original.priority,
      duration: remaining,
      startTime: null,
      endTime: null,
      eventDate: task.original.eventDate,
      color: task.original.color,
      classTag: task.original.classTag,
    ));
  }
}
















return allocated;
}
















// ---------------- Color helpers ----------------
Color _hexToColor(String hex) {
try {
  String h = hex.replaceAll("#", "");
  if (h.length == 6) h = "FF$h";
  final val = int.parse(h, radix: 16);
  return Color(val);
} catch (e) {
  return Colors.grey;
}
}
















// ---------------- UI dialogs: Add event, Settings, Classes ----------------
















void _showAddClassDialog() {
final formKey = GlobalKey<FormState>();
String className = "";
String hex = "#2196F3"; // default
showDialog(
  context: context,
  builder: (c) {
    return AlertDialog(
      title: const Text("Add Class / Commitment"),
      content: Form(
        key: formKey,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextFormField(
              decoration: const InputDecoration(labelText: "Name"),
              onSaved: (v) => className = v?.trim() ?? "",
            ),
            TextFormField(
              decoration: const InputDecoration(labelText: "Hex color (e.g. #FF0000)"),
              initialValue: hex,
              onSaved: (v) => hex = v?.trim() ?? hex,
            ),
          ],
        ),
      ),
      actions: [
        TextButton(onPressed: () => Navigator.pop(c), child: const Text("Cancel")),
        ElevatedButton(
          onPressed: () {
            formKey.currentState?.save();
            if (className.isEmpty) className = "Unnamed";
            setState(() {
              _classes.add(ClassItem(name: className, color: _hexToColor(hex)));
            });
            Navigator.pop(c);
          },
          child: const Text("Add"),
        ),
      ],
    );
  },
);
}
















void _showAddEventDialog() {
final formKey = GlobalKey<FormState>();
String title = "";
EventType eventType = EventType.flexible;
int duration = 30;
int priority = 3; // 1-5
DateTime eventDate = _selectedDate;
DateTime? pickedStartTime;
Recurrence recurrence = Recurrence.none;
String? selectedClass;
















showDialog(
  context: context,
  builder: (context) {
    return AlertDialog(
      backgroundColor: Theme.of(context).scaffoldBackgroundColor,
      title: const Text("Add Event"),
      content: SingleChildScrollView(
        child: Form(
          key: formKey,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextFormField(
                decoration: const InputDecoration(labelText: "Title"),
                onSaved: (v) => title = v?.trim() ?? "",
              ),
              const SizedBox(height: 8),
              DropdownButtonFormField<EventType>(
                value: eventType,
                decoration: const InputDecoration(labelText: "Event Type"),
                items: const [
                  DropdownMenuItem(value: EventType.fixed, child: Text("Fixed")),
                  DropdownMenuItem(value: EventType.flexible, child: Text("Flexible")),
                ],
                onChanged: (v) => eventType = v ?? EventType.flexible,
              ),
              const SizedBox(height: 8),
              TextFormField(
                initialValue: "30",
                decoration: const InputDecoration(labelText: "Duration (minutes)"),
                keyboardType: TextInputType.number,
                onSaved: (v) => duration = int.tryParse(v ?? "30") ?? 30,
              ),
              const SizedBox(height: 8),
              DropdownButtonFormField<int>(
                value: priority,
                decoration: const InputDecoration(labelText: "Priority (1=highest,5=lowest)"),
                items: [1, 2, 3, 4, 5]
                    .map((p) => DropdownMenuItem(value: p, child: Text("$p")))
                    .toList(),
                onChanged: (v) => priority = v ?? 3,
              ),
              const SizedBox(height: 8),
              DropdownButtonFormField<Recurrence>(
                value: recurrence,
                decoration: const InputDecoration(labelText: "Recurrence"),
                items: Recurrence.values
                    .map((r) => DropdownMenuItem(value: r, child: Text(r.toString().split('.').last)))
                    .toList(),
                onChanged: (v) => recurrence = v ?? Recurrence.none,
              ),
              const SizedBox(height: 8),
              DropdownButtonFormField<String>(
                value: selectedClass,
                decoration: const InputDecoration(labelText: "Class / Commitment (optional)"),
                items: [null, ..._classes.map((c) => c.name)].map((name) {
                  return DropdownMenuItem(value: name, child: Text(name ?? "None"));
                }).toList(),
                onChanged: (v) => selectedClass = v,
              ),
              const SizedBox(height: 8),
              ElevatedButton(
                onPressed: () async {
                  final picked = await showDatePicker(
                    context: context,
                    initialDate: eventDate,
                    firstDate: DateTime.now().subtract(const Duration(days: 365)),
                    lastDate: DateTime.now().add(const Duration(days: 365)),
                  );
                  if (picked != null) eventDate = picked;
                  setState(() {}); // to reflect the chosen date in UI (if desired)
                },
                child: const Text("Pick Event Date"),
              ),
              const SizedBox(height: 8),
              if (eventType == EventType.fixed)
                ElevatedButton(
                  onPressed: () async {
                    final picked = await showTimePicker(
                      context: context,
                      initialTime: TimeOfDay.now(),
                    );
                    if (picked != null) {
                      pickedStartTime = DateTime(eventDate.year, eventDate.month, eventDate.day, picked.hour, picked.minute);
                    }
                  },
                  child: const Text("Pick Fixed Start Time"),
                ),
            ],
          ),
        ),
      ),
      actions: [
        TextButton(onPressed: () => Navigator.pop(context), child: const Text("Cancel")),
        ElevatedButton(
          onPressed: () {
            formKey.currentState?.save();
















            // Use estimation if enough history
            int finalDuration = duration;
            final key = title.toLowerCase();
            final hist = _durationHistory[key] ?? (selectedClass != null ? _durationHistory[selectedClass!.toLowerCase()] : null);
            if (hist != null && hist.isNotEmpty) {
              final avg = (hist.reduce((a, b) => a + b) / hist.length).round();
              finalDuration = avg;
            }
















            DateTime? start = pickedStartTime;
            DateTime? end;
            if (start != null) end = start.add(Duration(minutes: finalDuration));
            final color = (selectedClass != null)
                ? (_classes.firstWhere((c) => c.name == selectedClass).color)
                : _getDefaultColorForPriority(priority);
















            final newEvent = PlannerEvent(
              title: title.isEmpty ? "(untitled)" : title,
              eventType: eventType,
              priority: priority,
              duration: finalDuration,
              startTime: start,
              endTime: end,
              deadline: null,
              eventDate: eventDate,
              color: color,
              classTag: selectedClass,
              recurrence: recurrence,
            );
            setState(() {
              _events.add(newEvent);
            });
            Navigator.pop(context);
          },
          child: const Text("Add"),
        ),
      ],
    );
  },
);
}
void _showEditEventDialog(PlannerEvent eventTappedOnScreen) {
// Key Fix: Identify the true source event from the main _events list.
// If the tapped event has a sourceEvent, use that. Otherwise, it's a fixed event and is its own source.
final PlannerEvent originalEvent = eventTappedOnScreen.sourceEvent ?? eventTappedOnScreen;








// Pre-fill the form with data from the ORIGINAL event.
final formKey = GlobalKey<FormState>();
String title = originalEvent.title;
EventType eventType = originalEvent.eventType;
int duration = originalEvent.duration;
int priority = originalEvent.priority;
DateTime eventDate = originalEvent.eventDate ?? _selectedDate;
DateTime? pickedStartTime = originalEvent.startTime;
Recurrence recurrence = originalEvent.recurrence;
String? selectedClass = originalEvent.classTag;








showDialog(
 context: context,
 // Use a StatefulBuilder to update the dialog's internal UI when the event type changes.
 builder: (context) {
   return StatefulBuilder(
     builder: (context, setDialogState) {
       return AlertDialog(
         backgroundColor: Theme.of(context).scaffoldBackgroundColor,
         title: const Text("Edit Event"),
         content: SingleChildScrollView(
           child: Form(
             key: formKey,
             child: Column(
               mainAxisSize: MainAxisSize.min,
               children: [
                 TextFormField(
                   initialValue: title,
                   decoration: const InputDecoration(labelText: "Title"),
                   onSaved: (v) => title = v?.trim() ?? "",
                 ),
                 const SizedBox(height: 8),
                 DropdownButtonFormField<EventType>(
                   value: eventType,
                   decoration: const InputDecoration(labelText: "Event Type"),
                   items: const [
                     DropdownMenuItem(value: EventType.fixed, child: Text("Fixed")),
                     DropdownMenuItem(value: EventType.flexible, child: Text("Flexible")),
                   ],
                   onChanged: (v) {
                     setDialogState(() {
                       eventType = v ?? EventType.flexible;
                     });
                   },
                 ),
                 const SizedBox(height: 8),
                 TextFormField(
                   initialValue: duration.toString(),
                   decoration: const InputDecoration(labelText: "Duration (minutes)"),
                   keyboardType: TextInputType.number,
                   onSaved: (v) => duration = int.tryParse(v ?? "30") ?? 30,
                 ),
                 const SizedBox(height: 8),
                 DropdownButtonFormField<int>(
                   value: priority,
                   decoration: const InputDecoration(labelText: "Priority (1=highest,5=lowest)"),
                   items: [1, 2, 3, 4, 5].map((p) => DropdownMenuItem(value: p, child: Text("$p"))).toList(),
                   onChanged: (v) => priority = v ?? 3,
                 ),
                 const SizedBox(height: 8),
                 DropdownButtonFormField<Recurrence>(
                   value: recurrence,
                   decoration: const InputDecoration(labelText: "Recurrence"),
                   items: Recurrence.values
                       .map((r) => DropdownMenuItem(value: r, child: Text(r.toString().split('.').last)))
                       .toList(),
                   onChanged: (v) => recurrence = v ?? Recurrence.none,
                 ),
                 const SizedBox(height: 8),
                 DropdownButtonFormField<String>(
                   value: selectedClass,
                   decoration: const InputDecoration(labelText: "Class / Commitment (optional)"),
                   items: [null, ..._classes.map((c) => c.name)].map((name) {
                     return DropdownMenuItem(value: name, child: Text(name ?? "None"));
                   }).toList(),
                   onChanged: (v) => selectedClass = v,
                 ),
                 const SizedBox(height: 8),
                 ElevatedButton(
                   onPressed: () async {
                     final picked = await showDatePicker(
                       context: context,
                       initialDate: eventDate,
                       firstDate: DateTime.now().subtract(const Duration(days: 365)),
                       lastDate: DateTime.now().add(const Duration(days: 365)),
                     );
                     if (picked != null) {
                       setDialogState(() {
                         eventDate = picked;
                       });
                     }
                   },
                   child: const Text("Pick Event Date"),
                 ),
                 const SizedBox(height: 8),
                 // Show the time picker ONLY for fixed events.
                 if (eventType == EventType.fixed)
                   ElevatedButton(
                     onPressed: () async {
                       final picked = await showTimePicker(
                         context: context,
                         initialTime: pickedStartTime != null
                             ? TimeOfDay.fromDateTime(pickedStartTime!)
                             : TimeOfDay.now(),
                       );
                       if (picked != null) {
                         setDialogState(() {
                           pickedStartTime = DateTime(eventDate.year, eventDate.month, eventDate.day, picked.hour, picked.minute);
                         });
                       }
                     },
                     child: Text(pickedStartTime == null ? "Pick Fixed Start Time" : TimeOfDay.fromDateTime(pickedStartTime!).format(context)),
                   ),
               ],
             ),
           ),
         ),
         actions: [
           TextButton(onPressed: () => Navigator.pop(context), child: const Text("Cancel")),
           ElevatedButton(
             onPressed: () {
               formKey.currentState?.save();








               // Create the updated event from the original source.
               final updatedEvent = originalEvent.copyWith(
                 title: title.isEmpty ? "(untitled)" : title,
                 eventType: eventType,
                 priority: priority,
                 duration: duration,
                 eventDate: eventDate,
                 startTime: eventType == EventType.fixed ? pickedStartTime : null,
                 endTime: eventType == EventType.fixed && pickedStartTime != null
                     ? pickedStartTime!.add(Duration(minutes: duration))
                     : null,
                 recurrence: recurrence,
                 classTag: selectedClass,
                 color: selectedClass != null
                     ? (_classes.firstWhere((c) => c.name == selectedClass).color)
                     : _getDefaultColorForPriority(priority),
               );








               setState(() {
                 // Key Fix: Use indexOf to find the exact object in the list. This is 100% reliable.
                 final index = _events.indexOf(originalEvent);
                 if (index != -1) {
                   _events[index] = updatedEvent;
                 }
               });
               Navigator.pop(context);
             },
             child: const Text("Save"),
           ),
         ],
       );
     },
   );
 },
);
}
























Color _getDefaultColorForPriority(int p) {
switch (p) {
  case 1:
    return Colors.blue[900]!;
  case 2:
    return Colors.blue[700]!;
  case 3:
    return Colors.blue[500]!;
  case 4:
    return Colors.blue[300]!;
  default:
    return Colors.blue[100]!;
}
}
















void _showSettingsDialog() {
final formKey = GlobalKey<FormState>();
int tempBreak = breakLength;
int tempShower = showerLength;
int tempMeal = mealLength;
TimeOfDay tempStart = workStart;
TimeOfDay tempEnd = workEnd;
int tempBuffer = bufferBetweenEvents;
int tempWorkChunk = workChunkLength;
ThemeMode tempMode = widget.themeMode;
String tempChoice = widget.themeChoice;
















showDialog(
  context: context,
  builder: (context) {
    return StatefulBuilder(builder: (c, setLocal) {
      return AlertDialog(
        backgroundColor: Theme.of(context).scaffoldBackgroundColor,
        title: const Text("Settings"),
        content: SingleChildScrollView(
          child: Form(
            key: formKey,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                TextFormField(
                  initialValue: tempBreak.toString(),
                  decoration: const InputDecoration(labelText: "Break Length (minutes)"),
                  keyboardType: TextInputType.number,
                  onSaved: (v) => tempBreak = int.tryParse(v ?? "10") ?? 10,
                ),
                TextFormField(
                  initialValue: tempShower.toString(),
                  decoration: const InputDecoration(labelText: "Shower Length (minutes)"),
                  keyboardType: TextInputType.number,
                  onSaved: (v) => tempShower = int.tryParse(v ?? "15") ?? 15,
                ),
                TextFormField(
                  initialValue: tempMeal.toString(),
                  decoration: const InputDecoration(labelText: "Meal Length (minutes)"),
                  keyboardType: TextInputType.number,
                  onSaved: (v) => tempMeal = int.tryParse(v ?? "30") ?? 30,
                ),
                TextFormField(
                  initialValue: tempBuffer.toString(),
                  decoration: const InputDecoration(labelText: "Buffer Between Events (minutes)"),
                  keyboardType: TextInputType.number,
                  onSaved: (v) => tempBuffer = int.tryParse(v ?? "5") ?? 5,
                ),
                TextFormField(
                  initialValue: tempWorkChunk.toString(),
                  decoration: const InputDecoration(labelText: "Work Chunk Length (minutes)"),
                  keyboardType: TextInputType.number,
                  onSaved: (v) => tempWorkChunk = int.tryParse(v ?? "50") ?? 50,
                ),
                ListTile(
                  title: const Text("Work Start Time"),
                  trailing: TextButton(
                    child: Text(tempStart.format(context)),
                    onPressed: () async {
                      final time = await showTimePicker(
                        context: context,
                        initialTime: tempStart,
                      );
                      if (time != null) setLocal(() => tempStart = time);
                    },
                  ),
                ),
                ListTile(
                  title: const Text("Work End Time"),
                  trailing: TextButton(
                    child: Text(tempEnd.format(context)),
                    onPressed: () async {
                      final time = await showTimePicker(
                        context: context,
                        initialTime: tempEnd,
                      );
                      if (time != null) setLocal(() => tempEnd = time);
                    },
                  ),
                ),
                const Divider(),
                const Text("Theme"),
                Row(
                  children: [
                    Expanded(
                      child: RadioListTile<ThemeMode>(
                        title: const Text("Light"),
                        value: ThemeMode.light,
                        groupValue: tempMode,
                        onChanged: (v) => setLocal(() => tempMode = v!),
                      ),
                    ),
                    Expanded(
                      child: RadioListTile<ThemeMode>(
                        title: const Text("Dark"),
                        value: ThemeMode.dark,
                        groupValue: tempMode,
                        onChanged: (v) => setLocal(() => tempMode = v!),
                      ),
                    ),
                  ],
                ),
                DropdownButtonFormField<String>(
                  value: tempChoice,
                  decoration: const InputDecoration(labelText: "Theme Color"),
                  items: ["Blue", "Rainbow", "BlueWhite"]
                      .map((c) => DropdownMenuItem(value: c, child: Text(c)))
                      .toList(),
                  onChanged: (v) => setLocal(() => tempChoice = v!),
                ),
              ],
            ),
          ),
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(c), child: const Text("Cancel")),
          ElevatedButton(
            onPressed: () {
              formKey.currentState?.save();
              setState(() {
                breakLength = tempBreak;
                showerLength = tempShower;
                mealLength = tempMeal;
                workStart = tempStart;
                workEnd = tempEnd;
                bufferBetweenEvents = tempBuffer;
                workChunkLength = tempWorkChunk;
              });
              widget.onThemeChanged(tempMode, tempChoice);
              Navigator.pop(c);
            },
            child: const Text("Save"),
          ),
        ],
      );
    });
  },
);
}
















// ---------------- UI Building ----------------
















@override
Widget build(BuildContext context) {
return Scaffold(
  key: _scaffoldKey,
  appBar: AppBar(
    title: Text("$_userName's Planner"),
    actions: [
      IconButton(
        icon: const Icon(Icons.calendar_view_week),
        onPressed: () => setState(() => _view = CalendarView.weekly),
      ),
      IconButton(
        icon: const Icon(Icons.calendar_view_day),
        onPressed: () => setState(() => _view = CalendarView.daily),
      ),
      IconButton(
        icon: const Icon(Icons.calendar_month),
        onPressed: () => setState(() => _view = CalendarView.monthly),
      ),
      IconButton(
        icon: const Icon(Icons.settings),
        onPressed: _showSettingsDialog,
      ),
    ],
  ),
  drawer: Drawer(
    child: ListView(
      padding: EdgeInsets.zero,
      children: <Widget>[
        DrawerHeader(
          decoration: BoxDecoration(
            color: Theme.of(context).primaryColor,
          ),
          child: const Text(
            'Classes & Commitments',
            style: TextStyle(
              color: Colors.white,
              fontSize: 24,
            ),
          ),
        ),
        ListTile(
          leading: const Icon(Icons.add),
          title: const Text('Add New Class'),
          onTap: () {
            Navigator.pop(context);
            _showAddClassDialog();
          },
        ),
        const Divider(),
        ..._classes.map((c) => ListTile(
          leading: Icon(Icons.circle, color: c.color),
          title: Text(c.name),
        )).toList(),
      ],
    ),
  ),
  body: _buildCalendarView(),
  floatingActionButton: FloatingActionButton(
    onPressed: _showAddEventDialog,
    child: const Icon(Icons.add),
  ),
);
}
















Widget _buildCalendarView() {
switch (_view) {
  case CalendarView.weekly:
    return _buildWeeklyView();
  case CalendarView.daily:
    return _buildDailyView(_selectedDate);
  case CalendarView.monthly:
    return _buildMonthlyView();
  default:
    return Container();
}
}
















Widget _buildWeeklyView() {
final startOfWeek = _selectedDate.subtract(Duration(days: _selectedDate.weekday - 1));
return Column(
  children: [
    _buildWeekHeader(startOfWeek),
    Expanded(
      child: SingleChildScrollView(
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: List.generate(7, (index) {
            final day = startOfWeek.add(Duration(days: index));
            return Expanded(
              child: Container(
                padding: const EdgeInsets.all(4),
                decoration: BoxDecoration(
                  border: Border.all(color: Theme.of(context).dividerColor),
                  color: _isSameDay(day, _selectedDate)
                      ? (Theme.of(context).brightness == Brightness.dark ? Colors.indigo.withOpacity(0.3) : Colors.indigo.withOpacity(0.1))
                      : null,
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    Center(
                      child: Text(
                        "${_dayLabel(day.weekday)} ${day.day}",
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          color: _isSameDay(day, DateTime.now()) ? Colors.redAccent : null,
                        ),
                      ),
                    ),
                    const SizedBox(height: 8),
                    ..._buildEventsForDay(day),
                  ],
                ),
              ),
            );
          }),
        ),
      ),
    ),
  ],
);
}
















Widget _buildDailyView(DateTime day) {
return Column(
  children: [
    _buildDailyHeader(day),
    Expanded(
      child: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: _buildEventsForDay(day),
        ),
      ),
    ),
  ],
);
}
















Widget _buildMonthlyView() {
final firstDayOfMonth = DateTime(_selectedDate.year, _selectedDate.month, 1);
final lastDayOfMonth = DateTime(_selectedDate.year, _selectedDate.month + 1, 0);
final startWeekday = firstDayOfMonth.weekday;
final totalDays = lastDayOfMonth.day;




int dayCounter = 1;
List<Widget> weeks = [];




for (int week = 0; week < 6; week++) {
  List<Widget> days = [];
  for (int weekday = 1; weekday <= 7; weekday++) {
    if ((week == 0 && weekday < startWeekday) || dayCounter > totalDays) {
      days.add(Expanded(child: Container())); // empty cell
    } else {
      final day = DateTime(_selectedDate.year, _selectedDate.month, dayCounter);
      final isToday = _isSameDay(day, DateTime.now());




      // Get up to 2 events for this day
      final dayEvents = _generateScheduleForDay(day).take(2).toList();
      final extraEvents = _generateScheduleForDay(day).length - dayEvents.length;




      days.add(
        Expanded(
          child: GestureDetector(
            onTap: () {
              setState(() {
                _selectedDate = day;
                _view = CalendarView.daily;
              });
            },
            child: Container(
              margin: const EdgeInsets.all(2),
              padding: const EdgeInsets.all(4),
              decoration: BoxDecoration(
                color: Theme.of(context).scaffoldBackgroundColor,
                border: Border.all(
                    color: isToday ? Colors.redAccent : Colors.grey.shade300),
                borderRadius: BorderRadius.circular(6),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  // Date on top-left
                  Align(
                    alignment: Alignment.topLeft,
                    child: Text(
                      "${day.day}",
                      style: const TextStyle(
                          fontWeight: FontWeight.bold, fontSize: 12),
                    ),
                  ),
                  const SizedBox(height: 4),
                  // Events
                  ...dayEvents.map((e) {
                    return Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 2, vertical: 1),
                      margin: const EdgeInsets.only(bottom: 2),
                      decoration: BoxDecoration(
                        color: e.color,
                        borderRadius: BorderRadius.circular(4),
                      ),
                      child: Text(
                        e.title,
                        style: const TextStyle(
                            fontSize: 10,
                            fontWeight: FontWeight.bold,
                            color: Colors.white),
                        overflow: TextOverflow.ellipsis,
                      ),
                    );
                  }),
                  if (extraEvents > 0)
                    Text(
                      "+$extraEvents more",
                      style:
                          const TextStyle(fontSize: 10, color: Colors.grey),
                    ),
                ],
              ),
            ),
          ),
        ),
      );




      dayCounter++;
    }
  }




  weeks.add(Expanded(child: Row(children: days)));
}




return Scaffold(
  body: Column(
    children: [
      // Month header with arrows
      Padding(
        padding: const EdgeInsets.symmetric(vertical: 8.0, horizontal: 4.0),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            IconButton(
              icon: const Icon(Icons.arrow_back_ios),
              onPressed: () {
                setState(() {
                  _selectedDate =
                      DateTime(_selectedDate.year, _selectedDate.month - 1, 1);
                });
              },
            ),
            Text(
              "${_monthLabel(_selectedDate.month)} ${_selectedDate.year}",
              style: Theme.of(context).textTheme.titleLarge,
            ),
            IconButton(
              icon: const Icon(Icons.arrow_forward_ios),
              onPressed: () {
                setState(() {
                  _selectedDate =
                      DateTime(_selectedDate.year, _selectedDate.month + 1, 1);
                });
              },
            ),
          ],
        ),
      ),
      // Weekday labels
      Row(
        children: const [
          Expanded(child: Center(child: Text("Mon"))),
          Expanded(child: Center(child: Text("Tue"))),
          Expanded(child: Center(child: Text("Wed"))),
          Expanded(child: Center(child: Text("Thu"))),
          Expanded(child: Center(child: Text("Fri"))),
          Expanded(child: Center(child: Text("Sat"))),
          Expanded(child: Center(child: Text("Sun"))),
        ],
      ),
      const Divider(height: 1),
      // Calendar grid
      Expanded(
        child: Column(children: weeks),
      ),
    ],
  ),
  floatingActionButton: FloatingActionButton(
    onPressed: () {
      _showAddEventDialog(); // add event for selected date
      setState(() {});
    },
    child: const Icon(Icons.add),
  ),
);
}
















// Helper to convert month number to string
String _monthLabel(int month) {
const months = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];
return months[month - 1];
}












Widget _buildDailyHeader(DateTime day) {
return Padding(
  padding: const EdgeInsets.all(8.0),
  child: Row(
    mainAxisAlignment: MainAxisAlignment.spaceBetween,
    children: [
      IconButton(
        icon: const Icon(Icons.arrow_back_ios),
        onPressed: () {
          setState(() {
            _selectedDate = _selectedDate.subtract(const Duration(days: 1));
          });
        },
      ),
      Text(
        "${_dayLabel(day.weekday)}, ${day.month}/${day.day}",
        style: Theme.of(context).textTheme.headlineSmall,
      ),
      IconButton(
        icon: const Icon(Icons.arrow_forward_ios),
        onPressed: () {
          setState(() {
            _selectedDate = _selectedDate.add(const Duration(days: 1));
          });
        },
      ),
    ],
  ),
);
}
















Widget _buildWeekHeader(DateTime startOfWeek) {
return Padding(
  padding: const EdgeInsets.symmetric(vertical: 8.0, horizontal: 4.0),
  child: Row(
    mainAxisAlignment: MainAxisAlignment.spaceBetween,
    children: [
      IconButton(
        icon: const Icon(Icons.arrow_back_ios),
        onPressed: () {
          setState(() {
            _selectedDate = _selectedDate.subtract(const Duration(days: 7));
          });
        },
      ),
      Text(
        "Week of ${_dayLabel(startOfWeek.weekday)}, ${startOfWeek.month}/${startOfWeek.day}",
        style: Theme.of(context).textTheme.titleLarge,
      ),
      IconButton(
        icon: const Icon(Icons.arrow_forward_ios),
        onPressed: () {
          setState(() {
            _selectedDate = _selectedDate.add(const Duration(days: 7));
          });
        },
      ),
    ],
  ),
);
}
















List<Widget> _buildEventsForDay(DateTime day) {
final scheduledEvents = _generateScheduleForDay(day);








if (scheduledEvents.isEmpty) {
 return [const Text("No events scheduled for this day.")];
}








return scheduledEvents.map((event) {
 String timeRange = "Time: N/A";
 if (event.startTime != null && event.endTime != null) {
   final start = event.startTime!;
   final end = event.endTime!;
   final startFmt = "${start.hour}:${start.minute.toString().padLeft(2, '0')}";
   final endFmt = "${end.hour}:${end.minute.toString().padLeft(2, '0')}";
   timeRange = "$startFmt - $endFmt";
 }








 return GestureDetector(
   onTap: () => _showEditEventDialog(event),
   child: Card(
     color: event.color,
     child: Padding(
       padding: const EdgeInsets.all(8.0),
       child: Column(
         crossAxisAlignment: CrossAxisAlignment.start,
         children: [
           Text(
             event.title,
             style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white),
           ),
           const SizedBox(height: 4),
           Text(
             timeRange,
             style: const TextStyle(color: Colors.white70),
           ),
           Text(
             "Duration: ${event.duration} min",
             style: const TextStyle(color: Colors.white70),
           ),
           if (event.classTag != null)
             Text("Class: ${event.classTag}", style: const TextStyle(color: Colors.white70)),
         ],
       ),
     ),
   ),
 );
}).toList();
}
}





import 'dart:convert';

class ApiResponseParser {
  /// Returns a List regardless of whether the backend
  /// returns:
  ///
  /// [
  ///   ...
  /// ]
  ///
  /// OR
  ///
  /// {
  ///   "count":10,
  ///   "results":[...]
  /// }
  static List<dynamic> parseList(String body) {
    final decoded = jsonDecode(body);

    if (decoded is List) {
      return List<dynamic>.from(decoded);
    }

    if (decoded is Map<String, dynamic>) {
      return List<dynamic>.from(
        decoded['results'] ?? [],
      );
    }

    return [];
  }

  static int parseCount(String body) {
    final decoded = jsonDecode(body);

    if (decoded is Map<String, dynamic>) {
      return decoded['count'] ?? 0;
    }

    if (decoded is List) {
      return decoded.length;
    }

    return 0;
  }

  static Map<String, dynamic> parseObject(
    String body,
  ) {
    final decoded = jsonDecode(body);

    if (decoded is Map<String, dynamic>) {
      return decoded;
    }

    return {};
  }
}
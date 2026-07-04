class PaymentService {
  static Future<List<dynamic>> getPayments() async {
    return [];
  }

  static Future<bool> createPayment({
    required int memberId,
    required int membershipPlanId,
    required double amount,
    required String paymentMethod,
    required String paymentStatus,
    required String transactionId,
    required String notes,
  }) async {
    return true;
  }
}
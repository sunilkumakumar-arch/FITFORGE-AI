variable "project" { type = string }
variable "environment" { type = string }
variable "api_base_url" { type = string default = "" }
resource "aws_cloudwatch_event_rule" "release_reservations" { name = "${var.project}-${var.environment}-release-reservations" schedule_expression = "rate(5 minutes)" }
resource "aws_cloudwatch_event_rule" "scan_renewals" { name = "${var.project}-${var.environment}-scan-renewals" schedule_expression = "rate(1 day)" }
resource "aws_cloudwatch_event_rule" "aggregate_metrics" { name = "${var.project}-${var.environment}-aggregate-metrics" schedule_expression = "cron(10 0 * * ? *)" }
# Targets should invoke a secured worker/Lambda or private API integration in the deployment account.
output "schedule_rule_names" { value = [aws_cloudwatch_event_rule.release_reservations.name, aws_cloudwatch_event_rule.scan_renewals.name, aws_cloudwatch_event_rule.aggregate_metrics.name] }

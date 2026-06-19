variable "project" { type = string }
variable "environment" { type = string }
variable "alb_arn_suffix" { type = string default = "" }
resource "aws_sns_topic" "alerts" { name = "${var.project}-${var.environment}-alerts" }
resource "aws_cloudwatch_metric_alarm" "api_5xx" { alarm_name = "${var.project}-${var.environment}-api-5xx" comparison_operator = "GreaterThanThreshold" evaluation_periods = 2 metric_name = "HTTPCode_Target_5XX_Count" namespace = "AWS/ApplicationELB" period = 300 statistic = "Sum" threshold = 5 alarm_actions = [aws_sns_topic.alerts.arn] treat_missing_data = "notBreaching" }
resource "aws_cloudwatch_metric_alarm" "high_latency" { alarm_name = "${var.project}-${var.environment}-api-latency" comparison_operator = "GreaterThanThreshold" evaluation_periods = 3 metric_name = "TargetResponseTime" namespace = "AWS/ApplicationELB" period = 300 statistic = "Average" threshold = 2 alarm_actions = [aws_sns_topic.alerts.arn] treat_missing_data = "notBreaching" }
output "alerts_topic_arn" { value = aws_sns_topic.alerts.arn }

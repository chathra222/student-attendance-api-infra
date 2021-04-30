output "email-sns-arn" {
  value = "${aws_sns_topic.codecommit-email.arn}"
}

output "email-sns-name" {
  value = "${aws_sns_topic.codecommit-email.name}"
}
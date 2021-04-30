# resource "aws_codecommit_repository" "main" {
#   repository_name = var.reponame
#   description     = "CodeCommit repo: ${var.reponame}"
#   default_branch  = "master"
# }

resource "aws_sns_topic" "main" {
  name         = "${var.topic-prefix}${var.reponame}${var.topic-suffix}"
  display_name = "CodeCommit ${var.reponame} notifications"
}

resource "aws_sns_topic_policy" "main" {
  arn    = aws_sns_topic.main.arn
  policy = data.aws_iam_policy_document.sns-policy.json
}

resource "aws_sns_topic_subscription" "sqs" {
  topic_arn            = aws_sns_topic.main.arn
  endpoint             = aws_sqs_queue.main.arn
  raw_message_delivery = "true"
  protocol             = "sqs"
}

resource "aws_sns_topic" "codecommit-email" {
  name = "codecommit-email-notifications-${var.reponame}"
  display_name = "CodeCommit notifications-${var.reponame}"
}

resource "aws_codecommit_trigger" "main" {
  repository_name = var.reponame

  trigger {
    name            = "notifications"
    events          = ["all"]
    destination_arn = aws_sns_topic.main.arn
  }

  trigger {
    name            = "email"
    events          = ["all"]
    destination_arn = aws_sns_topic.codecommit-email.arn
  }
}


resource "aws_sns_topic_policy" "codecommit-email-sns-policy" {
  arn = "${aws_sns_topic.codecommit-email.arn}"
  policy = "${data.aws_iam_policy_document.codecommit-email-sns-policy.json}"
}


resource "aws_sqs_queue" "main" {
  name = "codecommit-notifications-queue-${var.reponame}"
  delay_seconds = 90
  max_message_size = 2048
  message_retention_seconds = 86400
  receive_wait_time_seconds = 10
}

resource "aws_sqs_queue_policy" "sns" {
  queue_url = "${aws_sqs_queue.main.id}"
  policy = "${data.aws_iam_policy_document.sns-sqs-policy.json}"
}

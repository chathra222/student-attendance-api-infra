

data "aws_iam_policy_document" "codecommit-email-sns-policy" {
  statement {
    sid = "AllowSubscription"
    effect = "Allow"
    principals {
      type = "AWS"
      identifiers = [ "*" ]
    }
    actions = [
      "SNS:Publish",
      "SNS:RemovePermission",
      "SNS:SetTopicAttributes",
      "SNS:DeleteTopic",
      "SNS:ListSubscriptionsByTopic",
      "SNS:GetTopicAttributes",
      "SNS:Receive",
      "SNS:AddPermission",
      "SNS:Subscribe"
    ]
    resources = [ "${aws_sns_topic.codecommit-email.arn}" ]
    condition {
      test = "StringEquals"
      variable = "AWS:SourceOwner"
      values = [ "528196604817" ]
    }
  }

}

data "aws_iam_policy_document" "sns-sqs-policy" {
  policy_id = "arn:aws:sqs:us-east-1:528196604817:testing/SQSDefaultPolicy"

  statement {
    sid = "SubscribeToSNS"
    effect = "Allow"
    principals {
      type = "AWS"
      identifiers = [ "*" ]
    }
    actions = [ "SQS:SendMessage" ]
    resources = [ "${aws_sqs_queue.main.arn}" ]
    condition {
      test = "ArnLike"
      variable = "aws:SourceArn"
      values = [ "arn:aws:sns:us-east-1:528196604817:codecommit*" ]
    }
  }
}
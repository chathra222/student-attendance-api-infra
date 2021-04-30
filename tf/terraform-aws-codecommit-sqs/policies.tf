data "aws_iam_policy_document" "sns-policy" {
  policy_id = "__default_policy_ID"
  statement {
    sid    = "AllowSubscriptionFromSQS"
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
    actions = [
      "SNS:GetTopicAttributes",
      "SNS:SetTopicAttributes",
      "SNS:AddPermission",
      "SNS:RemovePermission",
      "SNS:DeleteTopic",
      "SNS:Subscribe",
      "SNS:ListSubscriptionsByTopic",
      "SNS:Publish",
      "SNS:Receive",
    ]
    resources = [aws_sns_topic.main.arn]
    condition {
      test     = "StringEquals"
      variable = "AWS:SourceOwner"
      values   = [var.aws-account-id]
    }
  }
}


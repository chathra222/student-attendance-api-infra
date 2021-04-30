# Link it with this module
module "web-repo-hook" {
  source = "./terraform-aws-codecommit-sqs"
  reponame = "student-attendance-web"
  aws-account-id = "528196604817"
 # email-sns-arn = aws_sns_topic.codecommit-email.arn
 # sqs-id = aws_sqs_queue.main.id
  
}

module "mobile-repo-hook" {
  source = "./terraform-aws-codecommit-sqs"
  reponame = "student-attendance-mobile"
  aws-account-id = "528196604817"
 # email-sns-arn = aws_sns_topic.codecommit-email.arn
 # sqs-id = aws_sqs_queue.main.id
  
}
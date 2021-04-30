variable "reponame" {
}

variable "aws-account-id" {
}

# Can enable if an email notification is desired.
# variable "email-sns-arn" {
# }


variable "topic-prefix" {
  default = "codecommit-"
}

variable "topic-suffix" {
  default = "-topic"
}


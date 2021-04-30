resource "aws_s3_bucket" "source" {
  bucket = "student-faces-source"
  acl    = "private"
  tags = {
    Name        = "student-faces-source"
  }
}


resource "aws_s3_bucket" "target" {
  bucket = "student-faces-target"
  acl    = "private"
  tags = {
    Name        = "student-faces-target"
  }
}
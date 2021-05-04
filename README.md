# Student Attendance API and Infra Setup

This Repository includes code for following
  * APIs for Student Attendance 

Technologies
* Python
* Uses the [Serverless Framework](https://serverless.com/) to deploy the APIs in AWS
* APIs use [AWS Rekognition Collection](https://aws.amazon.com/rekognition/) for Face Recognition and Analysis.
* Cloudformation and Terraform to Setup the infrastructure.


### Infra Setup

To run Cloudformation and Terraform Commands,
You should have the Access key and Secret key of a AWS User having Sufficient Permissions for your AWS account

```
export AWS_ACCESS_KEY_ID=<>
export AWS_SECRET_ACCESS_KEY=<>

```

* Create CodeCommit Repos and Service Roles
```
cd  cf/
aws cloudformation deploy --template cicd.yaml --stack-name ci-cd-stack  --capabilities CAPABILITY_IAM
```

* Create Aurora Serverless DB,Jenkins Code Commit Web Hook
```
cd tf/
terraform init
terraform apply
```

## Steps

Install aws cli 
Install NodeJs and npm https://www.npmjs.com/get-npm
Install serverless framework - (https://serverless.com/framework/docs/getting-started/)

Once you have the Serverless framework installed,In the base directory run following,:

```
npm install
serverless deploy --owner <owner-name>
```

## Usage / Testing

vscode rest client is used for excuting test cases in testcases/test.http file.

## Static Code Analysis
Install pylint
http://pylint.pycqa.org/en/latest/user_guide/installation.html

Run Static code analysis for Python Lambda functions
py -m pylint functions/*.py




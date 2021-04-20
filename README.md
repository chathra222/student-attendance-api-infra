# Student Attendance API

Technologies
* Python
* It uses the [Serverless Framework](https://serverless.com/) for deployment
* The application requires an [AWS Rekognition Collection](https://aws.amazon.com/rekognition/). 

## Steps

Install aws cli 
Install serverless framework - (https://serverless.com/framework/docs/getting-started/)

Once you have the Serverless framework installed, you can deploy the application following these commands:

```
git clone https://github.com/arapulido/face-recognition-serverless-app
cd face-recognition-serverless-app
npm install
export AWS_ACCESS_KEY_ID=<>
export AWS_SECRET_ACCESS_KEY=<>
serverless deploy --owner <owner-name>
```

## Usage / Testing

API unit tests
https://docs.python.org/3/library/unittest.html

## Static Code Analysis
Install pylint
http://pylint.pycqa.org/en/latest/user_guide/installation.html

Run Static code analysis for Python Lambda functions
py -m pylint functions/*.py


### Through a web application

There is a [sample web application](https://github.com/arapulido/upload-picture-s3-face-recognition) that will upload a picture to S3 and will called the first function of the pipeline directly, for a more end-to-end user experience. Follow the instructions to deploy and use that application in its [README.md file](https://github.com/arapulido/upload-picture-s3-face-recognition/blob/master/README.md).

### Lambda functions

The workflow of functions will do the following:

* `face-index` will index the face into the Rekognition collection (to find duplicates later).
* `persist-metadata` will store some metadata into a DynamoDB table.
* `face-search` will check if the same face is already part of the Rekognition collection, and will err if that's the case (duplicated face).
* `face-detection` will check if the picture contains 1 face. If it has more than 1 face or no faces, will return an error.
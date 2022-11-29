# Location Data Anomalies

## About this Solution
This solution was built for a chalk talk (FWM 318) at AWS Re:Invent 2022 titled "How to build location-aware workflows to detect data anomalies" delivered by Matt Nightingale and Drishti Arora.

This repository contains a Cloud Formation Template that is intended as quickstart to deploy a anomaly detection workflow for location data. The solution leverages AWS Stepfunctions, AWS Lambda, Amazon S3, AWS Glue DataBrew, AWS Glue, and Amazon Location Service. 


## Solution Architecture
<img width="917" alt="Screen Shot 2022-11-27 at 4 30 43 PM" src="https://user-images.githubusercontent.com/73195085/204168522-595f0ba8-e023-4b87-8925-58e30e677c2e.png">

 
1. An AWS Lambda function copys the source data and AWS Glue Scripts + Dependencies from an external AWS Account (owned by solution author) and copys them into a new Amazon S3 bucket in the deployment AWS Account
2. AWS Step Functions kicks off the anomaly workflow, creating an AWS Glue Data Brew Dataset and Project, which analyzes the source data using a Glue Databrew Recipe to flag anomalies. You can view the recipe [here](https://github.com/aws-samples/location-data-anomalies/blob/main/glue-databrew-recipe.yaml)
3. AWS Glue Data Brew processes the flagged-anomaly-dataset and outputs it to S3, kicking off the AWS Glue ETL job.
4. AWS Glue runs an ETL Job using a python script to call the Amazon Location Service Paces APIs on flagged anomalies in the new dataset. You can view the python script [here](https://github.com/aws-samples/location-data-anomalies/blob/main/glue-etl-script.py)
5. The final dataset, with anomalies identified and Geocoded, are output into S3 as a final, processed dataset

## Design Considerations
### Sample Data

To demonstrate the solution, we prepare and transform a portion of the publically available Yelp dataset from Kaggle, focusing on location data for businesses in Las Vegas, NV.

You can download and analyze the portion of the source dataset that will be used for this solution [by clicking this link](https://location-anomaly-resources.s3.amazonaws.com/artifacts/source/las_vegas_yelp_business.csv), which will also be cloned into a new bucket in your AWS account by deploying the Cloud Formation Template in this repo.

## Deploying the solution 

1. To deploy this solution, simply create a new [cloudformation stack](https://console.aws.amazon.com/cloudformation/home) in your aws account and upload the cloudformationtemplate.yaml file.
<img width="1050" alt="Screen Shot 2022-11-29 at 3 32 14 PM" src="https://user-images.githubusercontent.com/73195085/204671488-f7cb2405-8401-460a-adcf-e8e1bfad02a2.png">

2. Verify the stack has been deployed successdfully.
<img width="1127" alt="Screen Shot 2022-11-29 at 3 36 19 PM" src="https://user-images.githubusercontent.com/73195085/204672155-2035c381-e1e6-4d23-8318-f79d04c48ff1.png">

3. Navigate to [AWS Step Functions](console.aws.amazon.com/states/home?), and Start the execution on the State Machine deployed by the CloudFormation Stack.
<img width="1051" alt="Screen Shot 2022-11-29 at 3 42 20 PM" src="https://user-images.githubusercontent.com/73195085/204672929-1f0a12e6-a599-4c8b-8c80-16ed79670060.png">

4. Once the state machine has executed successfully, navigate to the Amazon S3 bucket deployed by CloudFormation and and view the processed dataset. 
<img width="1074" alt="Screen Shot 2022-11-29 at 3 46 41 PM" src="https://user-images.githubusercontent.com/73195085/204673477-c8958fdc-a20d-4783-8959-7ae81f100ba2.png">

Congratulations! You have successfully processed location data anomalies using AWS Glue, AWS Glue DataBrew, and Amazon Location Service.

Reach out to nghtm@amazon.com with any questions.


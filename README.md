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

##Deploying the solution 

1. To deploy this solution, simply upload the cloudformation.yaml file to your aws account. 


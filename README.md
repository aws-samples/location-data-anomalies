# Location Data Anomalies

## About this Solution
This solution was built for a chalk talk (FWM 318) at AWS Re:Invent 2022 titled "How to build location-aware workflows to detect data anomalies" delivered by Matt Nightingale and Drishti Arora.

This repository contains a Cloud Formation Template that is intended as quickstart to deploy a "Location Data Anomoly Aware" ETL (Extract, Transform, Load) workflow using AWS Stepfunctions, Amazon S3, AWS Glue DataBrew, AWS Glue ETL Jobs (Python), and Amazon Location Service to flag location data anomalies and enrich flagged anomalies with Place Details from Amazon Location Service. 

## Solution Architecture

To demonstrate the solution, we prepare and transform a portion of the publically available ["Yelp dataset from Kaggle"](https://www.kaggle.com/datasets/yelp-dataset/yelp-dataset?select=yelp_academic_dataset_business.json)

<img width="1061" alt="Screen Shot 2022-11-25 at 11 56 57 AM" src="https://user-images.githubusercontent.com/73195085/204029411-ec2dc7ac-be46-4a6e-bdc1-fe40772f2783.png">





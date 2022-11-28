#  Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: MIT-0

#import libraries
import sys
import json
import boto3
import pandas as pd
import io

#import Glue Context
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.dynamicframe import DynamicFrame
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql import functions as F
from pyspark.sql.types import *
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv,
                          ['input_path', 'output_bucket', 's3_output_key', 'location_index'])

#Create clients for S3 and Location Service (Boto3)
location = boto3.client('location')
s3_client = boto3.client('s3')
location_index = args['location_index']

#Get Dataset from S3 location (ouput of Glue DataBrew)
response = s3_client.get_object(Bucket=args['output_bucket'], Key=args['input_path'])
print(response)
status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

#Read CSV into a dataframe with Pandas
data = pd.read_csv(response.get("Body")).dropna(thresh=2)
df = pd.DataFrame(data)
data = data.rename(columns=str.title)
columns = data.columns

#Create Output Columns for Geocoding Results
GeocodedAddress = []
GeocodedPoints = []

#Find Mean Lat/lon values used for Bias Position of Geocoder
mean_long = (data['Longitude'].mean())
mean_lat = (data['Latitude'].mean())

#Create empty values for new coloumns
for index, row in data.iterrows():
    GeocodedAddress.append("")
    GeocodedPoints.append("")

#For each Anomalous Value, Geocode or Reverse Geocode to return alternative results from Amazon Location Service
for index, row in data.iterrows():
    if row.Address_Exists_Flagged == True:
        response = location.search_place_index_for_position(
                    IndexName=location_index,
                    Position=[row.Longitude, row.Latitude])
        json_response = response["Results"]
        x = (json_response[0]["Place"]["Label"])
        y = (json_response[0]["Place"]["Geometry"]["Point"])
        GeocodedAddress[index]=x
        GeocodedPoints[index]=y
    if row.Latitude_Outlier_Flagged == True:
        response = location.search_place_index_for_text(
                    IndexName=location_index,
                    Text= str(row.Address),
                    BiasPosition= [mean_long, mean_lat])
        json_response = response["Results"]
        x = json_response[0]["Place"]["Label"]
        y = json_response[0]["Place"]["Geometry"]["Point"]
        GeocodedAddress[index]=x
        GeocodedPoints[index]=y
    if row.Longitude_Outlier_Flagged == True:
        response = location.search_place_index_for_text(
                    IndexName=location_index,
                    Text= str(row.Address),
                    BiasPosition= [mean_long, mean_lat]
        )
        json_response = response["Results"]
        x = json_response[0]["Place"]["Label"]
        y = json_response[0]["Place"]["Geometry"]["Point"]
        GeocodedAddress[index] = x
        GeocodedPoints[index] = y

#Append Results from Geococoder to new columns
data["GeocodedAddress"] = GeocodedAddress
data["GeocodedPoints"] = GeocodedPoints

#write out to CSV
with io.StringIO() as csv_buffer:
    data.to_csv(csv_buffer, index=False)
    response = s3_client.put_object(
        Bucket=args['output_bucket'], Key=args['s3_output_key'], Body= csv_buffer.getvalue()
    )
    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
    if status == 200:
        print(f"Successful S3 put_object response. Status - {status}")
    else:
        print(f"Unsuccessful S3 put_object response. Status - {status}")




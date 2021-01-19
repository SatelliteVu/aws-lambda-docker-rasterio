# aws-lambda-docker-rasterio
[![standard-readme compliant](https://img.shields.io/badge/standard--readme-OK-green.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

AWS Lambda Container Image with Python Rasterio for querying Cloud Optimised GeoTiffs.

This repository contains an example AWS Lambda Docker image which uses Rasterio to query pixel values from a Cloud Optimised GeoTIFF (COG) stored in an S3 bucket. You can test the function locally using the Lambda Runtime Interface Emulator.

## Table of Contents
- [aws-lambda-docker-rasterio](#aws-lambda-docker-rasterio)
  - [Table of Contents](#table-of-contents)
  - [Background](#background)
  - [Install](#install)
  - [Usage](#usage)
  - [API](#api)
  - [Deploy Container to ECR](#deploy-container-to-ecr)
  - [Deploy lambda](#deploy-lambda)
  - [Issues](#issues)
  - [References](#references)

## Background
At re:Invent 2020 AWS launched support for custom container images to be executed as Lambda functions (see: https://aws.amazon.com/blogs/aws/new-for-aws-lambda-container-image-support/), making the use of Rasterio inside AWS Lambda's much easier and more accessible.


## Install
```sh
docker build -t rasterio .
```

## Usage
The handler function reads the pixel values from a COG within a specified polygon.

The Docker container includes the Lambda Runtime Interface Emulator so you can test the functions by running the images with Docker locally:

```sh
docker run -p 9000:8080 -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY rasterio:latest
```

Then in a separate terminal you can make calls to the service, use `request.py` or curl:

```sh
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations"\
    -d '{
            "raster": "s3://copernicus-dem-30m/Copernicus_DSM_COG_10_N55_00_W006_00_DEM/Copernicus_DSM_COG_10_N55_00_W006_00_DEM.tif",
            "geom": [
                {
                "type": "Polygon",
                "coordinates": [[[-5.2857375145,55.7018595345],[-5.2792572975,55.7018595345],[-5.2792572975,55.7052207941],[-5.2857375145,55.7052207941],[-5.2857375145,55.7018595345]]]
                }
            ]
        }'
```

When hosted on AWS the url simply changes to something like `https://6yz32m631c.execute-api.eu-west-2.amazonaws.com/default/rasterio_demo`

## API
Returns pixels values within specified area.

Requires the following parameters:

- raster: S3 address of the COG to query
- geom: JSON/Fiona polygon geometry object

Example query:

```json
{
  "raster": "s3://copernicus-dem-30m/Copernicus_DSM_COG_10_N55_00_W006_00_DEM/Copernicus_DSM_COG_10_N55_00_W006_00_DEM.tif",
    "geom": [
    {
      "type": "Polygon",
      "coordinates": [
        [
          [
            -5.2857375145,
            55.7018595345
          ],
          [
            -5.2792572975,
            55.7018595345
          ],
          [
            -5.2792572975,
            55.7052207941
          ],
          [
            -5.2857375145,
            55.7052207941
          ],
          [
            -5.2857375145,
            55.7018595345
          ]
        ]
      ]
    }
  ]
}

```

Example response:

```json
"[[[0.0, 0.0, 0.0, 0.4298372268676758, 3.1277780532836914, 3.167654514312744, 3.940603017807007, 8.856860160827637, 14.149166107177734, 19.369218826293945, 21.710126876831055, 28.996673583984375, 34.88554763793945, 41.25983428955078, 48.78239822387695, 56.83858108520508, 65.9479751586914], ...]]"
```

Lambda logs:
```
Init Duration: 0.79 ms  
Duration: 1717.92 ms  
Billed Duration: 1800 ms  
Memory Size: 3008 MB    
Max Memory Used: 3008 MB
```

## Deploy Container to ECR
Have setup a Github action to perform the following:

1. Build Docker image locally
2. Push to Docker repository (AWS ECR Repository)
3. Create Lambda using container image

## Deploy lambda
See this tutorial for more details: https://aws.amazon.com/blogs/aws/new-for-aws-lambda-container-image-support/

Skip to the section starting `In the Lambda console, I click on Create function`. I named ours `rasterio_demo`. Setup a REST API trigger

## Issues
Just an issue with this example most likely, but accepting default permissions on the lambda it appears unable to access the example DEM and fails with ACCESS_DENIED error:
```
"'/vsis3/copernicus-dem-30m/Copernicus_DSM_COG_10_N55_00_W006_00_DEM/Copernicus_DSM_COG_10_N55_00_W006_00_DEM.tif' does not exist in the file system, and is not recognized as a supported dataset name."
```


## References
- https://docs.aws.amazon.com/lambda/latest/dg/python-image.html

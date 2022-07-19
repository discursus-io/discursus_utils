from dagster import op, AssetMaterialization, Output

import boto3
from urllib.request import urlopen, urlretrieve
from io import StringIO
import pandas as pd


################
# Op to save asset to S3
@op(
    required_resource_keys = {
        "aws_client"
    }
)
def save_data_asset(context, df_data_asset, file_path):
    context.log.info("Saving data asset to : " + file_path)

    s3_bucket_name = context.resources.aws_client.get_s3_bucket_name()
    
    s3 = boto3.resource('s3')
    csv_buffer = StringIO()
    df_data_asset.to_csv(csv_buffer, index = False)
    s3.Object(s3_bucket_name, file_path).put(Body=csv_buffer.getvalue())

    return df_data_asset


################
# Op to get asset from S3
@op(
    required_resource_keys = {
        "aws_client"
    }
)
def get_saved_data_asset(context):
    s3_bucket_name = context.resources.aws_client.get_s3_bucket_name()
    filepath = context.op_config["asset_materialization_path"].split("s3://" + s3_bucket_name + "/")[1]

    context.log.info("Getting data asset from S3: " + str(filepath))
    
    s3 = boto3.resource('s3')
    obj = s3.Object(s3_bucket_name, filepath)

    df_data_asset = pd.read_csv(StringIO(obj.get()['Body'].read().decode('utf-8')))

    return df_data_asset


################
# Op to materialize data asset in Dagster
@op(
    required_resource_keys = {
        "aws_client"
    }
)
def materialize_data_asset(context, df_data_asset, file_path):
    context.log.info("Materializing data asset")

    s3_bucket_name = context.resources.aws_client.get_s3_bucket_name()
    asset_key_parent = context.op_config["asset_key_parent"]
    asset_key_child = context.op_config["asset_key_child"]
    asset_description = context.op_config["asset_description"]
    
    # Materialize asset
    yield AssetMaterialization(
        asset_key = [asset_key_parent, asset_key_child],
        description = asset_description,
        metadata={
            "path": "s3://" + s3_bucket_name + "/" + file_path,
            "rows": df_data_asset.index.size
        }
    )
    yield Output(df_data_asset)

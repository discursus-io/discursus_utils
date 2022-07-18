from dagster import op, AssetMaterialization, Output
from dagster_shell import create_shell_command_op
from dagster import file_relative_path

import boto3
from urllib.request import urlopen, urlretrieve
import zipfile
from io import StringIO
import pandas as pd


# Op to save the latest GDELT events to S3
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


# Op to materialize the url metadata as a data asset in Dagster
@op(
    required_resource_keys = {
        "aws_client"
    }
)
def materialize_data_asset(context, df_data_asset, file_path, asset_key_parent, asset_key_child, asset_description):
    context.log.info("Materializing data asset")

    s3_bucket_name = context.resources.aws_client.get_s3_bucket_name()
    
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

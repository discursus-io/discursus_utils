from dagster import op, AssetMaterialization, Output
from dagster_shell import create_shell_command_op
from dagster import file_relative_path

import boto3
from urllib.request import urlopen, urlretrieve
import zipfile
from io import StringIO
import pandas as pd

from discursus_utils import content_auditor

######################
# SCRAPING OPS
######################

# Op to get the meta data from a list of urls
@op(
    required_resource_keys = {
        "aws_client",
        "gdelt_client"
    }
)
def get_meta_data(context, latest_gdelt_events_s3_location):
    content_bot = content_auditor.ContentAuditor(s3_bucket_name, filename)

    # Enhance urls
    context.log.info("Enhancing " + str(len(content_bot.article_urls)) + " articles")
    content_bot.read_url()

    # Create dataframe
    df_gdelt_enhanced_articles = pd.DataFrame (content_bot.site_info, columns = ['mention_identifier', 'page_name', 'file_name', 'page_title', 'page_description', 'keywords'])
    context.log.info("Enhanced " + str(df_gdelt_enhanced_articles['mention_identifier'].size) + " articles")

    return df_gdelt_enhanced_articles




######################
# SAVINGS OPS
######################
# Op to save the latest GDELT events to S3
@op(
    required_resource_keys = {
        "aws_client"
    }
)
def save_urls_with_meta_data(context, df_latest_events, latest_events_url):
    context.log.info("Saving latest events to S3")

    s3_bucket_name = context.resources.aws_client.get_s3_bucket_name()

    latest_events_filename_zip = latest_events_url.split('gdeltv2/')[1]
    latest_events_filename_csv = latest_events_filename_zip.split('.zip')[0]
    latest_events_filedate = latest_events_filename_csv[0:8]
    
    s3 = boto3.resource('s3')
    csv_buffer = StringIO()
    df_latest_events.to_csv(csv_buffer, index = False)
    latest_events_s3_object_location = 'sources/gdelt/' + latest_events_filedate + '/' + latest_events_filename_csv
    s3.Object(s3_bucket_name, latest_events_s3_object_location).put(Body=csv_buffer.getvalue())


    context.log.info("Saved latest events to : " + latest_events_s3_object_location)

    return latest_events_s3_object_location


# Op to materialize the url metadata as a data asset in Dagster
@op(
    required_resource_keys = {
        "aws_client"
    }
)
def materialize_urls_with_meta_datat(context, df_gdelt_enhanced_articles, latest_gdelt_events_s3_location):
    s3_bucket_name = context.resources.aws_client.get_s3_bucket_name()

    # Extracting which file we're enhancing
    filename = latest_gdelt_events_s3_location.splitlines()[-1]

    # Materialize asset
    yield AssetMaterialization(
        asset_key=["sources", "gdelt_articles"],
        description="List of enhanced articles mined from GDELT",
        metadata={
            "path": "s3://" + s3_bucket_name + "/" + filename.split(".")[0] + "." + filename.split(".")[1] + ".enhanced.csv",
            "rows": df_gdelt_enhanced_articles['mention_identifier'].size
        }
    )
    yield Output(df_gdelt_enhanced_articles)

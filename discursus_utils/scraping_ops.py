from dagster import op, AssetMaterialization, Output
from dagster_shell import create_shell_command_op
from dagster import file_relative_path

import boto3
from urllib.request import urlopen, urlretrieve
import zipfile
from io import StringIO
import pandas as pd

from discursus_utils import content_auditor

################
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
from dagster import op, AssetMaterialization, Output

from urllib.request import urlopen, urlretrieve
import pandas as pd

from discursus_utils import content_auditor

################
# Op to get the meta data from a list of urls
@op
def get_meta_data(context, df_urls):
    url_field_index = context.op_config["url_field_index"]
    content_bot = content_auditor.ContentAuditor(df_urls, url_field_index)

    # Enhance urls
    context.log.info("Enhancing " + str(len(content_bot.urls)) + " urls")
    content_bot.read_url()

    # Create dataframe
    df_enhanced_urls = pd.DataFrame(content_bot.site_info, columns = ['mention_identifier', 'page_name', 'file_name', 'page_title', 'page_description', 'keywords'])
    context.log.info("Enhanced " + str(df_enhanced_urls.index.size) + " urls")

    return df_enhanced_urls
from dagster import op, AssetMaterialization, Output

from urllib.request import urlopen, urlretrieve
import pandas as pd

from discursus_utils import web_scraper

################
# Op to get the meta data from a list of urls
@op
def get_meta_data(context, df_urls):
    url_field_index = context.op_config["url_field_index"]
    content_bot = web_scraper.ContentAuditor(df_urls, url_field_index)

    # Enhance urls
    context.log.info("Enhancing " + str(len(content_bot.urls)) + " urls")
    content_bot.read_url()

    # Create dataframe
    column_names = ['mention_identifier', 'page_name', 'file_name', 'page_title', 'page_description', 'keywords']
    df_enhanced_urls = pd.DataFrame(columns = column_names)

    # write meta data
    for dex in content_bot.site_info:
        row = [
            dex['mention_identifier'], 
            dex['name'], 
            dex['filename'],
            dex['title'],
            dex['description'],
            dex['keywords']
        ]
        df_length = len(df_enhanced_urls)
        df_enhanced_urls.loc[df_length] = row
    context.log.info("Enhanced " + str(df_enhanced_urls.index.size) + " urls")

    return df_enhanced_urls
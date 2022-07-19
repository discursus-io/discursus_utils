# discursus GDELT library
This library provides [ops](https://docs.dagster.io/concepts/ops-jobs-graphs/ops) to extend the functionalities of the core framework.

It is part of the [discursus Social Analytics OSS Framework](https://github.com/discursus-io/discursus_core). Please visit the repo for more information. And visit us at [discursus.io] for more context on our mission.

&nbsp;

# How to use this library
Please refer to the [discursus Social Analytics OSS Framework](https://github.com/discursus-io/discursus_core) instructions for how to use a the framework and its libraries.

&nbsp;

# Library Ops
The library includes the following ops.

## scraping_ops.get_meta_data
Mines meta data from a list of urls.

Parameters
- df_urls: A dataframe that includes a column with urls

Configurations
- url_field_index: The index of the urls column. Starts with 0.

## persistence_ops.save_data_asset
Saves data asset to S3.

Resources:
- aws_client: A configured resource for S3.

Parameters
- df_data_asset: The dataframe to be saved to S3.
- file_path: The complete file path where the dataframe will be saved in your S3 bucket.

Configurations
- None required.

## persistence_ops.get_saved_data_asset
Gets data asset from S3.

Resources:
- aws_client: A configured resource for S3.

Parameters
- None required

Configurations
- file_path: The complete file path where the dataframe is saved in your S3 bucket.

## persistence_ops.get_saved_data_asset
Materialize dataframes as data assets in Dagster

Resources:
- aws_client: A configured resource for S3.

Parameters
- df_data_asset: The dataframe to be materialized.
- file_path: The complete file path where the dataframe is saved in your S3 bucket.

Configurations
- asset_key_parent: Name of the asset category.
- asset_key_child: Name of the asset.
- asset_description: Description of the asset.

&nbsp;

# Development of library
- Once improvements have been added to library
- Compile a new version: `python setup.py bdist_wheel`
- Commit branch and PR into new release branch
- Point projects to new release branch
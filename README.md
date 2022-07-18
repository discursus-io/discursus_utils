# discursus GDELT library
This library provides [ops](https://docs.dagster.io/concepts/ops-jobs-graphs/ops) to add functionality to the discursus framework.

## Library description
The library includes the following ops.

### Bla
Bla


# How to use this library
## Core Framework
This library is part of the [discursus Social Analytics OSS Framework](https://github.com/discursus-io/discursus_core). Please visit the repo for more information. And visit us at [discursus.io] for more context on our mission.

## Installation
We assume you are running a Docker file such as the one we have in the [Core repo](https://github.com/discursus-io/discursus_core/blob/release/0.1/Dockerfile_app.REPLACE).

The only thing you need to add is this line that will load the GDELT library to your instance of the social analytics framework.
`RUN pip3 install git+https://github.com/discursus-io/discursus_utils@release/0.1`

## Calling a op
When you call function (a Dagster op) from the library, you will need to pass the resources you configured.

```
aws_configs = config_from_files(['configs/aws_configs.yaml'])
gdelt_configs = config_from_files(['configs/gdelt_configs.yaml'])

my_aws_client = aws_client.configured(aws_configs)
my_gdelt_client = gdelt_resources.gdelt_client.configured(gdelt_configs)

@job(
    resource_defs = {
        'aws_client': my_aws_client,
        'gdelt_client': my_gdelt_client
    }
)
def mine_gdelt_data():
    latest_gdelt_events_s3_location = gdelt_mining_ops.mine_gdelt_events()
```

## Configurations
### Configure the AWS Resource
Create a aws configuration file (`aws_configs.yamls`) in the `configs` section of the core framwork.

```
resources:
  s3:
    config:
      bucket_name: discursus-io
```

Create a AWS resource file (`aws_resource.py`) in the `resources` section of the core framework.

```
from dagster import resource, StringSource

class AWSClient:
    def __init__(self, s3_bucket_name):
        self._s3_bucket_name = s3_bucket_name


    def get_s3_bucket_name(self):
        return self._s3_bucket_name


@resource(
    config_schema={
        "resources": {
            "s3": {
                "config": {
                    "bucket_name": StringSource
                }
            }
        }
    },
    description="A AWS client.",
)
def aws_client(context):
    return AWSClient(
        s3_bucket_name = context.resource_config["resources"]["s3"]["config"]["bucket_name"]
    )
```


# Development of library
- Once improvements have been added to library
- Compile a new version: `python setup.py bdist_wheel`
- Commit branch and PR into new release branch
- Point projects to new release branch
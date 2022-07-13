# discursus_utils
Library of utils for the discursus framework

# How to use this package
## Core Framework
- [Use the core framework](https://github.com/discursus-io/discursus_core)
- install the library in your Docker file: `RUN pip3 install git+https://github.com/discursus-io/discursus_gdelt@release/0.1`


## Calling a function
@job
def extract_url_meta_data():
    url_meta_data = discursus_utils_ops.extract_url_meta_data()
```


# Development of library
- Once improvements have been added to package
- Compile a new version: `python setup.py bdist_wheel`
- Commit branch and PR into new release branch
- Point projects to new release branch
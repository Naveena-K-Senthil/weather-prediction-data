import kfp
from kfp.components import create_component_from_func

from kubernetes.client.models import *
import os

from get_data_test import get_data_test


get_data_component = create_component_from_func(
    get_data_test,
    base_image="quay.io/modh/runtime-images:runtime-cuda-tensorflow-ubi9-python-3.9-2023a-20230817-b7e647e",
    packages_to_install=[]
)


@kfp.dsl.pipeline(name="train_upload_stock_kfp")
def sdk_pipeline():
    get_data_task = get_data_component()
    csv_file = get_data_task.output
    
    print(csv_file)

from kfp_tekton.compiler import TektonCompiler


# DEFAULT_STORAGE_CLASS needs to be filled out with the correct storage class, or else it will default to kfp-csi-s3
os.environ["DEFAULT_STORAGE_CLASS"] = os.environ.get(
    "DEFAULT_STORAGE_CLASS", "gp3"
)
os.environ["DEFAULT_ACCESSMODES"] = os.environ.get(
    "DEFAULT_ACCESSMODES", "ReadWriteOnce"
)
TektonCompiler().compile(sdk_pipeline, __file__.replace(".py", ".yaml"))

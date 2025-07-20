import logging
from PIL import Image
import io
import os
from azure.storage.blob import BlobServiceClient
import azure.functions as func

app = func.FunctionApp()

@app.function_name(name="ExtractMetadataActivity")
@app.activity_trigger(input_name="blob_info")
def extract_metadata(blob_info: dict):
    blob_name = blob_info['blob_name']
    container_name = "images-input"

    # Use environment variable for security
    connection_str = os.getenv("AzureWebJobsStorage")
    if not connection_str:
        logging.error("AzureWebJobsStorage environment variable is missing.")
        return None

    blob_service_client = BlobServiceClient.from_connection_string(connection_str)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_data = blob_client.download_blob().readall()

    image = Image.open(io.BytesIO(blob_data))
    width, height = image.size
    image_format = image.format
    size_kb = len(blob_data) / 1024

    metadata = {
        "name": blob_name,
        "size_kb": round(size_kb, 2),
        "width": width,
        "height": height,
        "format": image_format
    }

    logging.info(f"Extracted metadata: {metadata}")
    return metadata

import azure.functions as func
import azure.durable_functions as df
import logging

async def main(blob: func.InputStream, starter: str):
    client = df.DurableOrchestrationClient(starter)

    # Pass just the name/path to the blob, NOT binary data
    instance_id = await client.start_new("OrchestratorFunction", None, {
        "blob_name": blob.name
    })

    logging.info(f"Started orchestration with ID = '{instance_id}'")

import azure.functions as func
from azure.durable_functions import DurableOrchestrationContext

app = func.FunctionApp()

@app.function_name(name="orchestrator_function")
@app.durable_orchestration_trigger(context_name="context")
def main(context: DurableOrchestrationContext):
    image_info = context.get_input()

    metadata = yield context.call_activity("ExtractMetadataActivity", image_info)

    yield context.call_activity("StoreMetadataActivity", metadata)

    return metadata

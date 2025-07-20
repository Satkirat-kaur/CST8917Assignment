
# Intelligent Image Metadata Extractor - Durable Functions Assignment

## Project Overview

This project uses **Azure Durable Functions** to extract image metadata (width, height, format, size) from image blobs uploaded to Azure Blob Storage and optionally store it in an Azure SQL Database.

---

## Architecture

1. **Blob Trigger Function (`starter_function`)**:
   - Triggered by a new image in `images-input` container.
   - Starts a durable orchestration.

2. **Durable Orchestrator (`orchestrator_function`)**:
   - Calls two activities:
     1. `ExtractMetadataActivity`: Reads image and extracts metadata.
     2. `StoreMetadataActivity`: Logs or stores metadata to Azure SQL.

3. **Activity Functions**:
   - `ExtractMetadataActivity`: Uses `Pillow` to extract metadata.
   - `StoreMetadataActivity`: Mocks or writes metadata to SQL.

---

## Tools and Technologies

- **Azure Functions (Python)** – blob triggers, orchestrators, activities
- **Durable Functions extension**
- **Azure Blob Storage**
- **Azure SQL Database**
- **Python 3.12**
- **VS Code + Azure CLI + Azure Core Tools**

---

## Steps Completed

### 1. Environment Setup
- Created virtual environment `venv`
- Installed required packages:
  ```bash
  pip install azure-functions azure-storage-blob pillow pyodbc
  ```
- `azure-durable-functions` package not found – switched to using `azure-functions-durable`

### 2. Azure Resources
- Created Azure Function App using:
  ```bash
  func init --worker-runtime python
  func new --template "Durable Functions orchestrator"
  ```
- Created:
  - Blob storage container: `images-input`
  - Function App: `cst8917functionapp`
  - Resource Group: `cst8917-rg`
  - SQL Database: `ImageMetadata` table (manually or mocked)

### 3. Blob Trigger & Orchestrator
- Defined the `starter_function` with `@blob_trigger`
- Started orchestration via:
  ```python
  await client.start_new("orchestrator_function", None, blob_data)
  ```

### 4. Extract Metadata Activity
- Downloaded blob using `azure.storage.blob.BlobServiceClient`
- Used `Pillow` to get width, height, format, size

### 5. Store Metadata Activity
- Initially mocked by logging only
- Also attempted to use `pyodbc` to connect to Azure SQL (connection issues not resolved due to deployment limitations)

### 6. Deployment and Debugging
- Published using:
  ```bash
  func azure functionapp publish cst8917functionapp --build remote
  ```
- Faced these errors:
  - `ModuleNotFoundError: azure.durable_functions` (tried multiple fixes)
  - `AttributeError: 'azure.durable_functions' has no attribute 'orchestration_trigger'`
  - Durable triggers not recognized in remote Python 3.12 host

### 7. Final Status
- Blob trigger successfully invoked orchestration
- Metadata extraction worked locally
- Function deployment succeeded, but Durable orchestration failed on cloud host due to module incompatibility

---

## Conclusion

Although the orchestration failed on Azure due to Python module compatibility issues (`azure.durable_functions` not recognized in remote Python 3.12), I completed:

- Full local implementation
- Durable Function setup
- Blob triggering and metadata extraction
- SQL logic prepared
- Multiple troubleshooting attempts, including:
  - Rebuilding virtual environments
  - Trying various package versions
  - Redeploying function apps
  - Using logging to verify which steps were executed

---

## What I Learned

- How to structure a Durable Function App with a blob trigger and orchestrator
- Metadata extraction using `Pillow`
- Challenges of deploying Python Durable Functions on Azure
- Importance of package compatibility and logging for debugging

---

## Suggestions for Improvement

- Use Python 3.10 (LTS) in Azure Functions for better compatibility
- Stick with local development and mocking for unsupported modules
- Try an alternative approach like Logic Apps or Azure Data Factory for robust pipelines

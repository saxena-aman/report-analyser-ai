from dataclasses import dataclass
import time
from openai import OpenAI
import requests
from io import BytesIO
import os

# Retrieve the OpenAI API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

# Step 1: Define Models
@dataclass
class UploadedFile:
    id: str
    bytes: int
    created_at: int
    filename: str
    object: str
    purpose: str
    status: str
    status_details: str

@dataclass
class VectorStoreFile:
    id: str
    created_at: int
    last_error: str
    object: str
    status: str
    usage_bytes: int
    vector_store_id: str
    chunking_strategy: dict
    
class VectorStoreError(Exception):
    """Custom exception for vector store processing errors."""
    pass

def get_uploaded_file(response) -> UploadedFile:
    """Wraps the OpenAI file upload response into an UploadedFile instance."""
    return UploadedFile(
        id=response.id,
        bytes=response.bytes,
        created_at=response.created_at,
        filename=response.filename,
        object=response.object,
        purpose=response.purpose,
        status=response.status,
        status_details=response.status_details
    )

def get_vector_store_file(response) -> VectorStoreFile:
    """Wraps the OpenAI vector store file response into a VectorStoreFile instance."""
    return VectorStoreFile(
        id=response.id,
        created_at=response.created_at,
        last_error=response.last_error,
        object=response.object,
        status=response.status,
        usage_bytes=response.usage_bytes,
        vector_store_id=response.vector_store_id,
        chunking_strategy=response.chunking_strategy.dict()
    )

def check_vector_store_status(vector_store_id: str, file_id: str, timeout: int = 60, interval: int = 5):
    """
    Polls the OpenAI API to check the status of a vector store file.
    
    :param vector_store_id: ID of the vector store.
    :param file_id: ID of the file in the vector store.
    :param timeout: Maximum time to wait for the status to complete (in seconds).
    :param interval: Time interval between checks (in seconds).
    :return: The completed VectorStoreFile object.
    """
    start_time = time.time()

    while True:
        # Retrieve the vector store file status
        vector_store_response = client.beta.vector_stores.files.retrieve(
            vector_store_id=vector_store_id,
            file_id=file_id
        )
        vector_store_file = get_vector_store_file(vector_store_response)
        # Check the status of the vector store file
        print(f"Checking status... Current status: {vector_store_file.status}")

        if vector_store_file.status == "completed":
            print("Vector store file processing completed.")
            return vector_store_file
        elif vector_store_file.status == "cancelled":
            raise VectorStoreError("Vector store file processing was cancelled.")
        elif vector_store_file.status == "failed":
            raise VectorStoreError("Vector store file processing failed.")

        # Check for timeout
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            raise TimeoutError(f"Timed out waiting for vector store file status to complete after {timeout} seconds.")
        
        # Wait before checking again
        time.sleep(interval)
        
def upload_file(s3_url:str):
    response = requests.get(s3_url)
    
    if response.status_code == 200:
        file_content = BytesIO(response.content)
        file_content.name = "file.pdf"
        file_upload_response = client.files.create(
            file=file_content,
            purpose="assistants"
        )
        return get_uploaded_file(file_upload_response)
    else:
        raise VectorStoreError("Failed to download file from S3.")

def upload_file_to_vector_store(uploaded_file:UploadedFile,vs_id:str):
    vector_store_response = client.beta.vector_stores.files.create(
    vector_store_id=vs_id,
    file_id=uploaded_file.id
    )
    return get_vector_store_file(vector_store_response)
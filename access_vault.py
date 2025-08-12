from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.filedatalake import DataLakeServiceClient
import os

load_dotenv()

client_id = os.environ['AZURE_CLIENT_ID']
tenant_id = os.environ['AZURE_TENANT_ID']
client_secret = os.environ['AZURE_CLIENT_SECRET']
vault_url = os.environ['AZURE_VAULT_URL']
storage_account = os.environ['STORAGE_ACCOUNT_NAME']

secret_name = 'custom-data-engineering-pipeline-key'

credentials = ClientSecretCredential(
    client_id=client_id,
    client_secret=client_secret,
    tenant_id=tenant_id
)

secret_client = SecretClient(vault_url=vault_url, credential=credentials)

secret = secret_client.get_secret(secret_name)

print(f"Secret retrieved successfully")

service_client = DataLakeServiceClient(
    account_url=f"https://{storage_account}.dfs.core.windows.net",
    credential=credentials
)

print("Service client intiliazied")
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os
import msal
from fabric_cicd import FabricWorkspace, publish_all_items, unpublish_all_orphan_items

# ---- Config ----
TENANT_ID = os.getenv("AZURE_TENANT_ID", "2800c0a0-70e9-49be-8733-faeaa6aced99")
CLIENT_ID = os.getenv("AZURE_CLIENT_ID", "222b7cc4-e65d-4e09-98ac-35b39f244873")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
WORKSPACE_ID = os.getenv("FABRIC_WORKSPACE_ID", "b8284fa4-3266-4b97-84a6-04e6808c474d")

if not CLIENT_SECRET:
    raise RuntimeError("AZURE_CLIENT_SECRET is not set. Did you configure it in GitHub Secrets?")

ENVIRONMENT = "dev"
REPO_DIR = "."
ITEM_TYPES = ["Lakehouse", "Notebook", "Environment"]

def acquire_fabric_token(tenant_id: str, client_id: str, client_secret: str) -> str:
    """Acquire Fabric-scoped access token via client credentials flow."""
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    scopes = ["https://api.fabric.microsoft.com/.default"]
    app = msal.ConfidentialClientApplication(
        client_id=client_id,
        authority=authority,
        client_credential=client_secret,
    )
    result = app.acquire_token_for_client(scopes=scopes)
    if "access_token" not in result:
        raise RuntimeError(f"Failed to acquire Fabric token: {result}")
    return result["access_token"]

def main():
    # 1) Get token with MSAL
    access_token = acquire_fabric_token(TENANT_ID, CLIENT_ID, CLIENT_SECRET)

    # 2) Pass token directly to FabricWorkspace
    ws = FabricWorkspace(
        workspace_id=WORKSPACE_ID,
        environment=ENVIRONMENT,
        repository_directory=REPO_DIR,
        item_type_in_scope=ITEM_TYPES,
        access_token=access_token   # 👈 force token, no DefaultAzureCredential
    )

    # 3) Deploy
    publish_all_items(ws)
    unpublish_all_orphan_items(ws)

if __name__ == "__main__":
    main()

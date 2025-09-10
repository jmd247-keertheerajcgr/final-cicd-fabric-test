# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os
import time
import msal
from azure.core.credentials import AccessToken
from fabric_cicd import FabricWorkspace, publish_all_items, unpublish_all_orphan_items

# ---- Config (replace with secure secrets loading) ----
TENANT_ID = "2800c0a0-70e9-49be-8733-faeaa6aced99"
CLIENT_ID = "222b7cc4-e65d-4e09-98ac-35b39f244873"
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
os.environ["AZURE_CLIENT_SECRET"] = CLIENT_SECRET
WORKSPACE_ID = "b8284fa4-3266-4b97-84a6-04e6808c474d"
ENVIRONMENT = "dev"  # must match keys in parameter.yml if used
REPO_DIR = "."
ITEM_TYPES = ["Lakehouse", "Notebook", "Environment"]

# ---- Minimal TokenCredential wrapper for a static bearer ----
class StaticTokenCredential:
    def __init__(self, token: str, expires_in: int = 3500):
        self._token = token
        self._exp = int(time.time()) + expires_in
    def get_token(self, *scopes, **kwargs) -> AccessToken:
        return AccessToken(self._token, self._exp)

def acquire_fabric_token(tenant_id: str, client_id: str, client_secret: str, auth_host: str = "https://login.microsoftonline.com") -> str:
    authority = f"{auth_host.rstrip('/')}/{tenant_id}"
    scopes = ["https://api.fabric.microsoft.com/.default"]  # Fabric audience
    app = msal.ConfidentialClientApplication(client_id=client_id, authority=authority, client_credential=client_secret)
    result = app.acquire_token_for_client(scopes=scopes)
    if "access_token" not in result:
        raise RuntimeError(f"Failed to acquire Fabric token: {result}")
    return result["access_token"]

def main():
    # 1) Acquire Fabric-scoped bearer
    access_token = acquire_fabric_token(TENANT_ID, CLIENT_ID, CLIENT_SECRET)

    # 2) Provide it to FabricWorkspace (prefer credential=; fall back to access_token= for older versions)
    cred = StaticTokenCredential(access_token)
    try:
        ws = FabricWorkspace(
            workspace_id=WORKSPACE_ID,
            environment=ENVIRONMENT,
            repository_directory=REPO_DIR,
            item_type_in_scope=ITEM_TYPES,
            credential=cred
        )
    except TypeError:
        ws = FabricWorkspace(
            workspace_id=WORKSPACE_ID,
            environment=ENVIRONMENT,
            repository_directory=REPO_DIR,
            item_type_in_scope=ITEM_TYPES,
            access_token=access_token
        )

    # 3) Deploy
    publish_all_items(ws)
    unpublish_all_orphan_items(ws)

if __name__ == "__main__":
    main()

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from fabric_cicd import FabricWorkspace, publish_all_items, unpublish_all_orphan_items

# ---- Config ----
WORKSPACE_ID = "b8284fa4-3266-4b97-84a6-04e6808c474d"
ENVIRONMENT = "dev"
REPO_DIR = "."
ITEM_TYPES = ["Lakehouse", "Notebook", "Environment"]

def main():
    # 1) Initialize FabricWorkspace (no token passed)
    ws = FabricWorkspace(
        workspace_id=WORKSPACE_ID,
        environment=ENVIRONMENT,
        repository_directory=REPO_DIR,
        item_type_in_scope=ITEM_TYPES
    )

    # 2) Deploy
    publish_all_items(ws)
    unpublish_all_orphan_items(ws)

if __name__ == "__main__":
    main()

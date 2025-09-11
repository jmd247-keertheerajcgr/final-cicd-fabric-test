import argparse
import subprocess
from fabric_cicd import FabricWorkspace, publish_all_items
 
# Parse command-line arguments
parser = argparse.ArgumentParser(description="Run Fabric Workspace Publish")
parser.add_argument('--workspace_id', required=True, help='Fabric Workspace ID')
parser.add_argument('--repo_dir', required=True, help='Path to repository folder')
args = parser.parse_args()
 
workspace_id = args.workspace_id
repo_dir = args.repo_dir
 
print(f"Using workspace ID: {workspace_id}")
print(f"Using repository directory: {repo_dir}")
branch_name = subprocess.check_output(['git', 'branch', '--show-current']).decode().strip()
print(f"Running script from branch: {branch_name}")
 
# 1. Lakehouses & Warehouses
# fw_lake_ware = FabricWorkspace(
#     workspace_id=workspace_id,
#     repository_directory=repo_dir,
#     item_type_in_scope=["Lakehouse", "Warehouse"]
# )
# publish_all_items(fw_lake_ware)
 
# 2. Environments
# fw_env = FabricWorkspace(
#     workspace_id=workspace_id,
#     repository_directory=repo_dir,
#     item_type_in_scope=["Environment"]  
# )
# publish_all_items(fw_env)
 
# # 3. Notebooks
fw_nb = FabricWorkspace(
    workspace_id=workspace_id,
    repository_directory=repo_dir,
    item_type_in_scope=["Notebook"]
)
publish_all_items(fw_nb)
 
# # 4. Pipelines
# fw_pl = FabricWorkspace(
#     workspace_id=workspace_id,
#     repository_directory=repo_dir,
#     item_type_in_scope=["DataPipeline"],
#     environment="PPE"
# )
# publish_all_items(fw_pl)
 
# # 5. Reports / Models (if present)
# fw_reports = FabricWorkspace(
#     workspace_id=workspace_id,
#     repository_directory=repo_dir,
#     item_type_in_scope=["SemanticModel", "Report"],
# )
# publish_all_items(fw_reports)
 
print("Publish completed in dependency-safe order")

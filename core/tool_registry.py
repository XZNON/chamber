from tools.file_tools import fileInput,deleteFile
from tools.shell_tool import runShell

TOOL_REGISTRY = {
    "create_file" : fileInput,
    "delete_file" : deleteFile,
    "shell_execute" : runShell
}

def getTool(name : str):
    tool = TOOL_REGISTRY.get(name)
    if not tool:
        raise ValueError(f"Tool : '{name}' not found in registry")
    return tool
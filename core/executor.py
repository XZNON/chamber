from core.tool_registry import getTool
from core.logger import get_logger
from pathlib import Path
from models.tool_schemas import FileInput,FileSchema
from models.shell_command_schema import ShellCommandSchema

logger = get_logger("Executor")

def executePlan(planSteps : list[dict]):
    results = []
    for step in planSteps:
        action = step['action']
        params = step.get('params',{})
        tool = getTool(action)

        if not tool:
            logger.error(f"Tool : '{action}' not found")
            continue

        try:
            logger.info(f"Executing : {action}")

            if action == "create_file":
                p = Path(params["path"])
                schema = FileInput(
                    filename = p.name,
                    path = str(p.parent) if p.parent!=Path('.') else "./",
                    content=params["content"]
                )
                res = tool(schema)
            elif action == "delete_file":
                schema = FileSchema(
                    **params
                )
                res = tool(schema)
            elif action == "shell_execute":
                schema = ShellCommandSchema(
                    **params
                )
                res = tool(schema)
            else:
                res = tool(**params)
            
            results.append({"action":action,"result":res})
            logger.info(f"{action} -> {res.status if hasattr(res,'status') else 'done'}")
            
        except Exception as e:
            logger.error(f"Error executing {action} : {e}")
    return results

plan = [
  {"action": "create_file", "params": {"path": "test/hello.py", "content": "print('Hello from Chamber!')"}},
  {"action": "shell_execute", "params": {"cmd": "python", "arg": ["test/hello.py"], "shell": False}}
]

executePlan(plan)
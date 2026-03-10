from models.shell_command_schema import ShellCommandSchema
from base_executioner import BaseExecutioner
from models.tool_schemas import FileOutput
from models.chamber_state import ChamberState
from tools.shell_tool import runShell
from core.logger import get_logger
import subprocess
import os

class ShellExecutioner(BaseExecutioner):
    def __init__(self):
        self.logger = get_logger("Shell Executioner")
    
        
    def run_shell(self,state : ChamberState,cmd : str,args = None,cwd = None):
        args = args or []

        schema = ShellCommandSchema(
            cmd = cmd,
            arg = args,
            cwd = cwd
        )

        self.logger.info(f"Running shell command: {cmd} {' '.join(args)}")
        result = runShell(schema)

        return {
            "status" : "success",
            "result" : result
        }
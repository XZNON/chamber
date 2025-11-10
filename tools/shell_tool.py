import subprocess
from models.shell_command_schema import ShellCommandSchema
import os
from models.tool_schemas import FileOutput
from core.logger import get_logger

logger = get_logger("Shell Tool")


def runShell(schema : ShellCommandSchema):
    cwd = schema.cwd or os.getcwd()
    fullCommand = [schema.cmd] + (schema.arg or [])

    try:
        logger.info(f"Executing Shell command: {' '.join(fullCommand)} (cwd = {cwd})")
    
        process = subprocess.Popen(
            fullCommand if not schema.shell else " ".join(fullCommand),
            cwd = schema.cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=schema.shell
        )

        outputLines = []
        for line in process.stdout:
            line = line.strip()
            if line:
                logger.info(f"> {line}")
                outputLines.append(line)
        process.wait()

        if process.returncode == 0:
            logger.info(f"Command succeeded")
        else:
            logger.error(f"Command failed: {process.returncode}")
        
        return "\n".join(outputLines)

    except Exception as e:
        logger.error(f"Exception while executing command: {e}")
        return FileOutput(
            filename="",
            path=cwd,
            status="error",
            message=str(e)
        )        



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
    

        result = subprocess.run(
            fullCommand if not schema.shell else " ".join(fullCommand), 
            cwd=schema.cwd,
            capture_output=schema.captureOutput,
            text=True,
            shell=schema.shell,
        )

        stdout = result.stdout.strip() if result.stdout else ""
        stderr = result.stderr.strip() if result.stderr else ""

        if result.returncode == 0:
            logger.info(f"Command succeeded: {stdout or 'no output'}")
            return FileOutput(
                filename="",
                path=cwd,
                status="success",
                message=stdout or "Command executed successfully."
            )
        else:
            logger.error(f"Command failed: {stderr}")
            return FileOutput(
                filename="",
                path=cwd,
                status="error",
                message=stderr or f"Command failed with exit code {result.returncode}"
            )

    except Exception as e:
        logger.error(f"Exception while executing command: {e}")
        return FileOutput(
            filename="",
            path=cwd,
            status="error",
            message=str(e)
        )        



from models.tool_schemas import FileInput,FileOutput,FileSchema
from core.logger import get_logger
from pathlib import Path
import os

logger = get_logger()

def createFolder(folderName : str,created : list[str]):
    try:
        os.makedirs(folderName,exist_ok=True)
        created.append(folderName)
        logger.info(f"Created directory: {folderName}")
    except Exception as e:
        logger.error(f"Failed to create directory: {folderName}")
        raise

def fileInput(schema : FileInput) -> FileOutput:
    os.makedirs(schema.path,exist_ok=True)
    fullPath = os.path.join(schema.path,schema.filename)

    try:
        with open(fullPath, "w", encoding='utf-8') as f:
            f.write(schema.content)

        logger.info(f"written file successfully : {fullPath}") 
        return FileOutput(
            filename=schema.filename,
            path=schema.path,
            status='success',
            message= f"File '{schema.filename}' written successfuly."
        )
    except Exception as e:
        logger.error(f"Error while writing to {fullPath} : {e}")
        return FileOutput(
            filename=schema.filename,
            path = schema.path,
            status='error',
            message=str(e)
        )

def deleteFile(schema : FileSchema) -> FileOutput:
    p = Path(schema.path)
    try:
        p.unlink()
        logger.info(f"Deleted file successfully: {schema.path}")
        return FileOutput(
            filename=schema.filename,
            path=schema.path,
            status='success',
            message=f"successfully deletedd the {schema.filename}."
        )
    except Exception as e:
        logger.error(f"Error while deleting {schema.path}: {e}")
        return FileOutput(
            filename=schema.filename,
            path=schema.path,
            status='error',
            message=f"error while deleting {schema.filename}: {e}"
        )
    

if __name__ == "main":
    schema = FileInput(
        filename="subrtacter.py",
        path="./generated",
        content="""def add(a, b):
        \"\"\"Adds two numbers together and returns the result.\"\"\"
        return a + b

    if __name__ == "__main__":
        print("Running a test...")
        print(f"The result of 5 + 10 is: {add(5, 10)}")
    """
    )

    fileInput(schema)
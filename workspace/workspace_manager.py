# used to keep track of the whole project: 
# project state(files,folders,project_root),
# safety(overwrites,valid paths),
# file operations(create,read,write,delete)

from tools.file_tools import createFolder,fileInput,deleteFile
from models.tool_schemas import FileInput,FileSchema,FileOutput
from core.logger import get_logger
from pathlib import Path


logger = get_logger("WorkspaceManager")

class WorkspaceManager:

    def __init__(self, root : str = './workspace'):
        self.root = Path(root)
        self.root.mkdir(parents=True,exist_ok=True)

        self.folders = set()
        self.files = set()

        self.scan_workspace()

    def _resolve_path(self,path:str) -> Path:
        fullPath = (self.root / path).resolve()

        if self.root.resolve() not in fullPath.parents and fullPath != self.root.resolve():
            raise ValueError("Path escapes workspace")

        return fullPath
    
    def refresh(self):
        self.scan_workspace()
    
    def scan_workspace(self):
        """scans the workspace and keeps track of all the files and folders"""
        self.files.clear()
        self.folders.clear()

        for path in self.root.rglob("*"):
            relative = path.relative_to(self.root)

            if path.is_dir():
                self.folders.add(str(relative))
            else:
                self.files.add(str(relative))
    
    def create_folder(self,folderPath : str):
        fullPath = self._resolve_path(folderPath)
        fullPath.mkdir(parents= True,exist_ok= True)

        relative = fullPath.relative_to(self.root)
        self.folders.add(str(relative))
        logger.info(f"Workspace created a folder: {fullPath}")

        return str(relative)

    def write_file(self,filePath : str,content : str):
        fullPath = self._resolve_path(filePath)

        fullPath.parent.mkdir(parents=True, exist_ok=True)

        schema = FileInput(
            filename= fullPath.name,
            path = str(fullPath.parent),
            content = content
        )

        result = fileInput(schema)

        if result.status == "success":
            relative = fullPath.relative_to(self.root)
            self.files.add(str(relative))
        
        logger.info(f"Workspace written to folder: {relative}")
        return result
    
    def delete_file(self,filePath:str):
        fullPath = self._resolve_path(filePath)
        
        schema = FileSchema(
            filename=fullPath.name,
            path = str(fullPath)
        )

        result = deleteFile(schema)

        if result.status == "success":
            relative = fullPath.relative_to(self.root)
            self.files.discard(str(relative))
        logger.info(f"Workspace deleted folder: {relative}")
        return result
    
    def read_file(self,filePath : str) -> str:
        fullPath = self._resolve_path(filePath)

        if not fullPath.exists():
            logger.error(f"File does not exist {fullPath}")
            raise FileNotFoundError(filePath)

        with open(fullPath,"r",encoding="utf-8") as f:
            return f.read()
    
    def append_to_file(self,filePath : str,content : str):
        fullPath = self._resolve_path(filePath)

        try:
            with open(fullPath,"a",encoding="utf-8") as f:
                f.write("\n" + content)
            logger.info(f"Workspace appended to file: {relative}")
            relative = fullPath.relative_to(self.root)
            self.files.add(str(relative))
        except Exception as e:
            logger.error(f"Error while appending to file: {str(e)}")
            raise 
    
    def apply_patch(self,filePath : str,content : str):
        fullPath = self._resolve_path(filePath)

        with open(fullPath,"w",encoding="utf-8") as f:
            f.write(content)
        
        relative = fullPath.relative_to(self.root)
        self.files.add(str(relative))
        
        logger.info(f"Patched file: {fullPath}")
        

    def file_exists(self,filePath : str):
        relative = self._resolve_path(filePath).relative_to(self.root)
        return str(relative) in self.files
    

    def folder_exists(self,folderPath : str):
        relative = self._resolve_path(folderPath).relative_to(self.root)
        return str(relative) in self.folders
    
    def list_files(self):
        return list(self.files)

    def list_folders(self):
        return list(self.folders)
    
    def summarize(self):
        return {
            "folders": sorted(self.folders),
            "files": sorted(self.files)
        }
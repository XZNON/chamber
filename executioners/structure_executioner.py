from executioners.base_executioner import BaseExecutioner
from tools.file_tools import createFolder
from core.logger import get_logger
import os

logger = get_logger("Structure Executioner")

class StructureExecutioner(BaseExecutioner):

    def execute(self,goal,state):
        userIntent = state['input'][-1]
        goal = goal.description

        logger.info(f"Structure executioner executing: {goal}")
        # print(f"goal got: {goal}")

        folders = self._infer_folders(userIntent)
        created = []

        for folder in folders:
            try:
                createFolder(folder,created)
            except Exception as e:
                logger.error(f"Failed to create directory: {folder}")
                raise
        
        self._create_readme(userIntent)

        state.setdefault("workspace",{})
        state["workspace"]["structure"] = {
            "directories" : created
        }
                
        logger.info(f"StructuerExecutioner completed successfully")
    
    def _infer_folders(self,userIntent:str) -> list[str]:
        '''
        Infers only top level folders
        '''
        
        folders = []

        folders.append("docs")

        if "website" in userIntent or "frontend" in userIntent or "ui" in userIntent:
            folders.append("frontend")
        
        if "api" in userIntent or "backend" in userIntent or "server" in userIntent:
            folders.append("backend")
        
        if len(folders) == 1:
            folders.append("src")
        
        return list(dict.fromkeys(folders))
    
    def _create_readme(self,userIntent : str):
        if os.path.exists("README.md"):
            return
        
        content = f"# Project\n\n{userIntent.capitalize()}\n"

        try:
            with open("README.md","w",encoding="utf-8") as f:
                f.write(content)
            logger.info(f"Created README.md")
        except Exception as e:
            logger.error(f"Failed to create README.md file: {e}")
            raise
    


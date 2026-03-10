from executioners.base_executioner import BaseExecutioner
from langchain_core.prompts import PromptTemplate
from models.chamber_state import ChamberState
from utils.load_prompt import loadPrompt
from core.logger import get_logger
from core.config import MODEL


######################################################################
###################Executioner to write codes#########################
######################################################################

#   isnt called directly, other executioners use it to write their goals    #
#      has chamber state in it, implements all the commands needed          #

class CodeExecutioner(BaseExecutioner):

    def __init__(self):
        self.model = MODEL
        self.logger = get_logger("code_executioner")
    
    def generate_file(self,state:ChamberState,filePath : str,instructions : str):
        workspace = state['workspace']
        projectSummary = workspace.summarize()
        
        promptTemplate = PromptTemplate(
            template= loadPrompt('prompts/code_exec_prompt1.txt'),
            input_variables= ['projectSummary','instructions','filePath']
        )

        generationPrompt = promptTemplate.format(projectSummary = projectSummary,instructions = instructions,filePath = filePath)
        print(generationPrompt)

        response = self.model.invoke(generationPrompt)

        code = response.content
        res = workspace.write_file(filePath,code)
        self.logger.info(f'Generated a file: {filePath}')

        return res
    
    def modify_file(self,state : ChamberState, filePath:str, instructions:str):
        workspace = state['workspace']
        projectSummary = workspace.summarize()
        currentCode = workspace.read_file(filePath)

        promptTemplate = PromptTemplate(
            template= loadPrompt('prompts/code_exec_prompt2.txt'),
            input_variables=['projectSummary','filePath','currentCode','instructions']
        )
        
        modificaitonPromopt = promptTemplate.format(
            projectSummary = projectSummary,
            filePath = filePath,
            currentCode = currentCode,
            instructions = instructions
        )

        result = self.model.invoke(modificaitonPromopt)

        res = workspace.apply_patch(filePath,result.content)
        self.logger.info(f"Applied patch to file : {filePath}")
        return {"status" : "success" , "file" : filePath}
    
    def append_code(self,state : ChamberState,filePath : str,instructions : str):
        workspace = state['workspace']
        currentCode = workspace.read_file(filePath)

        promptTemplate = PromptTemplate(
            template = loadPrompt('prompts/code_exec_prompt3.txt'),
            input_variables = ['currentCode','instructions']
        )

        appendPrompt = promptTemplate.format(
            currentCode = currentCode,
            instructions = instructions
        )

        response = self.model.invoke(appendPrompt)
        newCode = response.content

        res = workspace.append_to_file(filePath,newCode)
        self.logger.info(f"Changes added to file: {filePath}")
        return {"status" : "success" , "file" : filePath}

test = CodeExecutioner()

# print(test.generate_file('343','sdfsdf','sdfsdf'))
        
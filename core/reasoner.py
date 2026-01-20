from models.chamber_state import ChamberState
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.prompts import PromptTemplate
from models.reasoner_output_schema import ReasonerOutputSchema
from core.logger import get_logger
from core.config import MODEL

logger = get_logger("Reasoner")

def loadPrompt(filepath : str="prompts/reasoner_prompt.txt")->str:
    """Loads system prompt for the reasoner from text file"""
    try:
        with open(filepath,"r",encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Reasoner could not read the prompt")
        return "You are chamber a development reasoning model, output only valid JSON"
        

def reasoner(state : ChamberState) -> ChamberState:
    '''reasoner node, this will get input from the user and device a plan'''
    inpt = state['input'][-1] 

    model = MODEL
    modelWithStructuredOutput = model.with_structured_output(ReasonerOutputSchema,method="function_calling")


    promptTemplate = PromptTemplate(
        template=loadPrompt()
    )
    systemPrompt = promptTemplate.invoke({}).to_string()

    try:
        logger.info(f"Reasoner recieved Input: {inpt}")

        response = modelWithStructuredOutput.invoke([
            {
                "role":"system","content":systemPrompt
            },
            {
                "role":"user","content":inpt
            }
        ])

        logger.info("Reasoner generated Goals successfully")

        return {
            'goals':response.goals,
            "error":None
        }
    except Exception as e:
        logger.error(f"Reasoner Failed: {e}")
        return {
            "goals":[],
            "error":str(e),
            "metadata":{
                "source":"reasoner",
                "status":"failed"
            }
        }
if __name__ == "__main__":
    dummy_state = {"input": ["I want to create a simple full stack shoes selling e commerce website"]}
    result = reasoner(dummy_state)
    print(result)




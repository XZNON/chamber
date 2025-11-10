from langchain_openai import ChatOpenAI
from core.config import OPENAI_API_KEY,GOOGLE_API_KEY
from models.chamber_state import ChamberState
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import AIMessage,HumanMessage,SystemMessage,BaseMessage
from langchain_core.prompts import PromptTemplate
from models.reasoner_output_schema import ReasonerOutputSchema
from utils.get_content import getContent
from core.logger import get_logger
from core.config import OPENAI_API_KEY,GOOGLE_API_KEY

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

    model = ChatOpenAI(model='gpt-4o-mini',api_key=OPENAI_API_KEY,temperature=0.3)
    modelWithStructuredOutput = model.with_structured_output(ReasonerOutputSchema,method="function_calling")
    content = getContent() or "N/A" #give it topic to generate content on

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

        logger.info("Reasoner generated plan successfully")

        return {
            'plan':response.plan,
            "error":None,
            "metadata":{
                "model":"gpt-4o-mini",
                "source":"reasoner"
            }
        }
    except Exception as e:
        logger.error(f"Reasoner Failed: {e}")
        return {
            "plan":[],
            "error":str(e),
            "metadata":{
                "source":"reasoner",
                "status":"failed"
            }
        }
if __name__ == "__main__":
    dummy_state = {"input": ["I want to create a simple frontend using html,js and css to create a page that displays HI"]}
    result = reasoner(dummy_state)
    print(result)




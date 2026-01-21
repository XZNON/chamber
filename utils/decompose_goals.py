#decomposer function
#     -uses LLM to sub divide a goal into atomic subgaols
#     -returns a list of goal objects
from models.reasoner_output_schema import GoalsSchema
from core.config import MODEL
from utils.load_prompt import loadPrompt
from langchain_core.prompts import PromptTemplate

def decomposeGoal(goal : str) -> GoalsSchema:
    '''
    This function takes in a goal string as an argument that needs to be 
    divided further into  subgoals,
    and divides them into subgoals and returns them in the desired output schema

    Maybe it can also ask few questions to the user if the goal is vague, (maybe after v1)
    '''
    
    structModel = MODEL.with_structured_output(GoalsSchema,method='function_calling')

    promptTemplate = PromptTemplate(
        template= loadPrompt("prompts/decomposer_prompt.txt"),
    )

    prompt = promptTemplate.invoke({}).to_string()
    try:
        response  = structModel.invoke([
                {
                    "role":"system","content":prompt
                },
                {
                    "role":"user","content":goal
                }
            ])
        
        return response
    except Exception as e:
        return []


if __name__ == "__main__":
    goal = 'Create APIs for product listing,order placement,user registeration, route for login'

    res = decomposeGoal(goal)

    for g in res.goals:
        print(type(g),g.description)

#decomposer function
#     -uses LLM to sub divide a goal into atomic subgaols
#     -returns a list of goal objects
from models.reasoner_output_schema import GoalsSchema

def decomposeGoal(goal : str) -> GoalsSchema:
    '''
    This function takes in a goal string as an argument that needs to be 
    divided further into  subgoals,
    and divides them into subgoals and returns them in the desired output schema

    Maybe it can also ask few questions to the user if the goal is vague, (maybe after v1)
    '''
    ...



# return this:
# [
#     Goal(description='Create API route for product listing'),
#     Goal(description='Create API route for order placement'),
#     Goal(description='Create API route for user registration'),
#     Goal(description='Create API route for login')
# ]
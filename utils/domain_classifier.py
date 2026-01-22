from core.config import MODEL
from models.domain_schema import BatchClassifyDomain

from dataclasses import dataclass

#use batch classify instead of calling it for every goal, (efficient)
def classifyDomains(goals :list[str]) -> list[str]:
    '''Classify goals into domains in a single batch, order preserved'''

    structModel = MODEL.with_structured_output(BatchClassifyDomain,method='function_calling')

    goalsBlock = "\n".join(f"{i+1}. {goal}" for i,goal in enumerate(goals))
    prompt = f"""
        You are Chamber’s Classifier.

        Your task is to analyze each provided goal and determine its technical domain and whether it requires further decomposition before execution.

        ### DECOMPOSITION CRITERIA:
        Set `needs_decomposition` to `true` if the goal:
        - Uses plural nouns (e.g., "endpoints," "models," "components").
        - Uses broad verbs like "Setup," "Develop," "Implement," or "Design" without a specific singular target.
        - Describes a system with more than one functional responsibility.
        - Is a milestone that will result in the creation of multiple files.

        Set `needs_decomposition` to `false` if the goal:
        - Targets a single file or a single specific function (e.g., "Create the User model," "Define the GET /login route").
        - Is a concrete, singular action that an LLM can complete in a single output.

        ### DOMAIN SELECTION:
        Assign EXACTLY ONE from: [structure, backend, database, api, frontend, ui, styling, testing, code, deployment, unknown].

        example:
        goal:
        -Create the root project directory named weather-web-application. (does not need decomposition as it is a single executable goal)
        -Within the root directory, create an api folder to handle API routes and controllers related to weather data.(needs decomposition)

        ### RULES:
        - Analyze goals independently and preserve original order.
        - No prose, no markdown, no explanations—ONLY valid JSON.
        - The results array length must exactly match the input goals length.

        ### INPUT:
        Goals: {goalsBlock}

        Return JSON in EXACTLY this format:

        {{
        "results": [
            {{
            "domain": "<domain>",
            "needs_decomposition": False
            }}
        ]
        }}
        """

    res = structModel.invoke(prompt)
    # print(res)
    return [{"domain" : item.domain , "needs_decomposition" :item.needs_decomposition} for item in res.results]
    


if __name__ == "__main__":
    goals = ['Add styling and user interface polish to ensure a smooth and attractive user experience','Define database models for shoes, users, orders, and any other required entities','Build user interface components for product display, shopping cart, user authentication, and checkout']
    this = classifyDomains(goals)

    print(this)
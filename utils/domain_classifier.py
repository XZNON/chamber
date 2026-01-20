from core.config import MODEL
from models.domain_schema import BatchClassifyDomain

from dataclasses import dataclass

#use batch classify instead of calling it for every goal, (efficient)
def classifyDomains(goals :list[str]) -> list[str]:
    '''Classify goals into domains in a single batch, order preserved'''

    structModel = MODEL.with_structured_output(BatchClassifyDomain)

    goalsBlock = "\n".join(f"{i+1}. {goal}" for i,goal in enumerate(goals))
    prompt = f"""
        You are a classifier.

        Your task is to analyze each goal and:
        1. Assign EXACTLY ONE domain.
        2. Decide whether the goal requires further decomposition.

        A goal requires decomposition if it:
        - Describes setting up or defining a system or architecture.
        - Involves multiple responsibilities, components, or entities.
        - Is high-level, vague, or cannot be completed in a single concrete step.

        A goal does NOT require decomposition if it:
        - Is a single, atomic action.
        - Can reasonably be completed by one executor in one pass.

        Allowed domains:
        - structure
        - backend
        - database
        - api
        - frontend
        - ui
        - styling
        - testing
        - code
        - deployment
        - unknown

        Rules:
        - Classify each goal independently.
        - Preserve the original order.
        - Return ONLY valid JSON.
        - Do NOT explain your choices.
        - Do NOT include any extra fields.
        - Do NOT include code, commands, tools, or frameworks.
        - The number of results MUST exactly match the number of goals.
        - needs_decomposition MUST be a boolean (true or false).

        Goals:
        {goalsBlock}

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
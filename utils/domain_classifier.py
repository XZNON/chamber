from core.config import MODEL
from models.domain_schema import BatchClassifyDomain

#use batch classify instead of calling it for every goal, (efficient)
def classifyDomains(goals :list[str]) -> list[str]:
    '''Classify goals into domains in a single batch, order preserved'''

    structModel = MODEL.with_structured_output(BatchClassifyDomain)

    goalsBlock = "\n".join(f"{i+1}. {goal}" for i,goal in enumerate(goals))
    prompt = f"""
            You are a classifier.

            Classify EACH goal below into EXACTLY ONE domain.

            Allowed domains:
            - structure
            - backend
            - database
            - api
            - frontend
            - ui
            - styling
            - testing
            - deployment
            - unknown

            Rules:
            - Classify each goal independently.
            - Preserve the order.
            - Return ONLY valid JSON.
            - Do not explain.
            - The number of results MUST match the number of goals.
            - The domain mapping should be correct and accurate

            Goals:
            {goalsBlock}

            Return JSON in this format:
            {{
            "results": [
                {{ "domain": "<domain>" }}
            ]
            }}
        """
    res = structModel.invoke(prompt)

    return [item.domain for item in res.results]


if __name__ == "__main__":
    goals = ['Add styling and user interface polish to ensure a smooth and attractive user experience','Define database models for shoes, users, orders, and any other required entities','Build user interface components for product display, shopping cart, user authentication, and checkout']
    this = classifyDomains(goals)

    print(this)
    
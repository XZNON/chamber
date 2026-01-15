from core.config import MODEL
from models.domain_schema import Domain

def classifyDomain(goalText : str) -> str:
    text = goalText.lower()

    structModel = MODEL.with_structured_output(Domain)
    prompt = f"""
            You are a classifier.

            Classify the following goal into EXACTLY ONE of the allowed domains.

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
            - code
            - unknown

            Rules:
            - Return only valid JSON.
            - Do not explain.
            - Do not include any other fields.

            Goal:
            {goalText}
        """
    res = structModel.invoke(prompt)

    return res


if __name__ == "__main__":
    this = classifyDomain("Add styling and user interface polish to ensure a smooth and attractive user experience")
    print(this)
    
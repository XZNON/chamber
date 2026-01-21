from core.logger import get_logger

logger = get_logger("Load Prompt")

def loadPrompt(filepath : str)->str:
    """Loads system prompt for the reasoner from text file"""
    try:
        with open(filepath,"r",encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Could not read the prompt, {filepath}")
        return "You are chamber a development reasoning model, output only valid JSON"
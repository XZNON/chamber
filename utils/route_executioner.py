from executioners.structure_executioner import StructureExecutioner
from core.logger import get_logger

logger = get_logger("Structure Executioner")

EXECUTIONER_REGISTERY = {
    "setup" : StructureExecutioner(),
    "create" : FileExecutioner(),
    "implement" : CodeExecutioner(),
    "design" : UIExecutioner(),
    "style" : StylingExecutioner(),
    "configure" : ConfigExecutioner()
}

def extractVerb(goal : str):
    return goal.strip().split()[0].lower()

def routeExecutioner(goalDescription : str):
    verb = extractVerb(goalDescription)
    logger.info(f"Routing goal: {goalDescription}")

    if verb not in EXECUTIONER_REGISTERY:
        raise RuntimeError(
            f"No executioner registered for {verb}"
        )
    logger.info(f"Routed to: {EXECUTIONER_REGISTERY[verb].__class__.__name__}")
    return EXECUTIONER_REGISTERY[verb]
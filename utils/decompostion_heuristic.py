def heuristicNeedsDecomposition(goal : str) -> bool:
    text = goal.lower()

    if any(x in text for x in [" and ", ","," as well as ", " also "]):
        return True
    
    if any(x in text for x in [
        "set up",
        "define",
        "design",
        "build",
        "architecture",
        "structure",
        "system",
        "service"
    ]):
        return True

    if any(x in text for x in [
         "polish",
        "improve",
        "optimize",
        "user experience",
        "smooth",
        "attractive"
    ]):
        return True

    return False
from executioners.dummy_executioner import DummyExecutioner
from executioners.structure_executioner import StructureExecutioner

def routeExecutioner(goalDescription : str):

    text = goalDescription.lower()

    if "setup" in text or "structure" in text or "folder" in text or "directory" in text or "project" in text:
        return StructureExecutioner()

    return None
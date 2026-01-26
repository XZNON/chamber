class DummyExecutioner:
    def execute(self,goal,state):
        print(f"[Dummy executioner] Executiong: {goal.description}")
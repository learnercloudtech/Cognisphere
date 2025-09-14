from utils.local_llm import query_local_llm

class SimulationAgent:
    def __init__(self, environment="default", parameters=None):
        self.environment = environment
        self.parameters = parameters or {}
        self.state_log = []

    def simulate_step(self, input_action: str) -> dict:
        if not input_action or len(input_action.strip()) < 5:
            return {"error": "Action too vague to simulate."}

        prompt = (
            f"You are simulating an environment: '{self.environment}'.\n"
            f"Parameters: {self.parameters}\n"
            f"Current action: {input_action}\n"
            "Describe the resulting state change, any NPC reactions, and environmental effects.\n"
            "Keep it structured and game-ready."
        )

        try:
            response = query_local_llm(prompt)
            state = {
                "action": input_action,
                "response": response,
                "parameters": self.parameters
            }
            self.state_log.append(state)
            return state
        except Exception as e:
            return {"error": f"Simulation failed: {str(e)}"}

    def update_environment(self, new_env: str, new_params=None):
        self.environment = new_env
        if new_params:
            self.parameters = new_params

    def refine_simulation(self, previous_state: dict, feedback: str) -> dict:
        prompt = (
            f"The following simulation output needs refinement:\n{previous_state.get('response', '')}\n"
            f"Feedback: {feedback}\n"
            "Improve the realism, coherence, and game logic of the simulation."
        )

        try:
            refined = query_local_llm(prompt)
            updated_state = previous_state.copy()
            updated_state["refined_response"] = refined
            updated_state["feedback"] = feedback
            self.state_log.append(updated_state)
            return updated_state
        except Exception as e:
            return {"error": f"Refinement failed: {str(e)}"}

    def get_state_log(self):
        return self.state_log

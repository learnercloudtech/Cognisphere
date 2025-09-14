from utils.local_llm import query_local_llm

class NPCAgent:
    def __init__(self, persona="neutral", context="", emotion="stable"):
        self.persona = persona
        self.context = context
        self.emotion = emotion
        self.trace = []

    def generate_behavior(self, situation: str) -> str:
        if not situation or len(situation.strip()) < 10:
            return "Insufficient context to generate NPC behavior."

        prompt = (
            f"You are an NPC with the persona: '{self.persona}' and current emotion: '{self.emotion}'.\n"
            f"Context: {self.context}\n"
            f"Situation: {situation}\n"
            "Describe the NPC's next action or dialogue in a way that reflects their persona and adapts to the situation.\n"
            "Keep it concise and game-ready."
        )

        try:
            response = query_local_llm(prompt)
            self.trace.append({
                "situation": situation,
                "response": response,
                "emotion": self.emotion
            })
            return response
        except Exception as e:
            return f"NPC generation failed: {str(e)}"

    def reflect_and_update(self, feedback: str):
        """
        Allows the NPC to reflect on feedback and adjust emotion/persona.
        """
        prompt = (
            f"The NPC received the following feedback: '{feedback}'.\n"
            f"Current persona: '{self.persona}', emotion: '{self.emotion}'.\n"
            "Based on this, suggest a new emotion and persona adjustment."
        )

        try:
            reflection = query_local_llm(prompt)
            # Simple parsing logic (can be replaced with structured output)
            if "emotion:" in reflection and "persona:" in reflection:
                lines = reflection.splitlines()
                for line in lines:
                    if "emotion:" in line:
                        self.emotion = line.split("emotion:")[1].strip()
                    if "persona:" in line:
                        self.persona = line.split("persona:")[1].strip()
            self.trace.append({
                "feedback": feedback,
                "reflection": reflection,
                "updated_emotion": self.emotion,
                "updated_persona": self.persona
            })
            return reflection
        except Exception as e:
            return f"Reflection failed: {str(e)}"

    def get_trace(self):
        return self.trace

from utils.local_llm import query_local_llm

class QuestEngine:
    def __init__(self, theme="fantasy", difficulty="medium"):
        self.theme = theme
        self.difficulty = difficulty
        self.quest_log = []

    def generate_quest(self, objective: str, npc_context: str = "") -> dict:
        if not objective or len(objective.strip()) < 10:
            return {"error": "Objective too vague to generate quest."}

        prompt = (
            f"You are a quest designer for a {self.theme} game.\n"
            f"Design a quest based on the objective: '{objective}'\n"
            f"Difficulty level: {self.difficulty}\n"
            f"NPC context: {npc_context}\n"
            "Break the quest into 3 clear stages with titles and descriptions.\n"
            "Include a reward and a twist if applicable."
        )

        try:
            response = query_local_llm(prompt)
            quest = {
                "objective": objective,
                "theme": self.theme,
                "difficulty": self.difficulty,
                "npc_context": npc_context,
                "response": response
            }
            self.quest_log.append(quest)
            return quest
        except Exception as e:
            return {"error": f"Quest generation failed: {str(e)}"}

    def refine_quest(self, previous_quest: dict, feedback: str) -> dict:
        prompt = (
            f"The following quest needs refinement based on feedback.\n"
            f"Quest:\n{previous_quest.get('response', '')}\n"
            f"Feedback: {feedback}\n"
            "Improve the quest structure, clarity, and engagement. Keep it game-ready."
        )

        try:
            refined = query_local_llm(prompt)
            updated_quest = previous_quest.copy()
            updated_quest["refined_response"] = refined
            updated_quest["feedback"] = feedback
            self.quest_log.append(updated_quest)
            return updated_quest
        except Exception as e:
            return {"error": f"Refinement failed: {str(e)}"}

    def get_quest_log(self):
        return self.quest_log

from utils.local_llm import query_local_llm

class PlannerAgent:
    def run(self, task):
        prompt = (
            f"You are an expert task planner. Break down the high-level task:\n"
            f"'{task}'\n"
            "into exactly 3 clear, actionable subtasks that autonomous agents can execute.\n"
            "List them as:\n1."
        )
        try:
            output = query_local_llm(prompt)
            lines = output.split("\n")
            subtasks = []
            for line in lines:
                clean = line.strip("1234567890.:- ").strip()
                if clean and clean.lower() != "response" and clean not in subtasks:
                    subtasks.append(clean)

            # 🧠 Fallback if LLM fails
            if not subtasks or all("response" in s.lower() for s in subtasks):
                print("⚠️ PlannerAgent fallback triggered.")
                return [
                    "Research common tactical motifs in chess endgames",
                    "Identify endgame positions that highlight tactical ideas",
                    "Design example endgames that teach tactical patterns"
                ]

            return subtasks[:3]
        except Exception as e:
            return [f"Planning failed: {str(e)}"]

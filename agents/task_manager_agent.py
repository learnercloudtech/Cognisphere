class TaskManagerAgent:
    def __init__(self):
        self.task_log = []

    def assign(self, subtask, evaluation):
        """
        Assigns a subtask based on evaluation score.
        Logs metadata and returns structured assignment.
        """
        quality = evaluation.get("quality", 0)
        feedback = evaluation.get("feedback", "No feedback")

        if quality >= 0.75:
            status = "approved"
            message = f"✅ Subtask '{subtask}' approved for execution."
            agent_role = "ExecutorAgent"
        elif quality >= 0.5:
            status = "refine"
            message = f"⚠️ Subtask '{subtask}' needs refinement before execution."
            agent_role = "RefinerAgent"
        else:
            status = "rejected"
            message = f"❌ Subtask '{subtask}' rejected. Replanning required."
            agent_role = "PlannerAgent"

        task_entry = {
            "subtask": subtask,
            "quality": quality,
            "feedback": feedback,
            "status": status,
            "assigned_role": agent_role,
            "message": message
        }

        self.task_log.append(task_entry)
        return task_entry

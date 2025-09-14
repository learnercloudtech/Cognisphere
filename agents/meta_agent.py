from agents.planner_agent import PlannerAgent
from agents.research_agent import ResearchAgent
from agents.summarizer_agent import SummarizerAgent
from agents.evaluator_agent import EvaluatorAgent
from agents.task_manager_agent import TaskManagerAgent

class MetaAgent:
    def __init__(self, task):
        self.task = task
        self.depth = 0
        self.max_depth = 2

        # 🧠 Initialize agents
        self.planner_agent = PlannerAgent()
        self.research_agent = ResearchAgent()
        self.summarizer_agent = SummarizerAgent()
        self.evaluator_agent = EvaluatorAgent()
        self.task_manager_agent = TaskManagerAgent()

    def execute(self):
        context = {}

        # 🔍 Step 1: Planning
        subtasks = self.planner_agent.run(self.task)
        print(f"[PlannerAgent] Subtasks: {subtasks}")

        if not subtasks or all("failed" in s.lower() for s in subtasks):
            return {
                "context": {},
                "score": {
                    "quality": 0.0,
                    "feedback": "PlannerAgent failed to generate valid subtasks."
                }
            }

        # 🔁 Step 2: Agentic Execution Loop
        for subtask in subtasks:
            print(f"\n🔧 Executing subtask: {subtask}")

            try:
                research = self.research_agent.run(subtask)
                summary = self.summarizer_agent.run(research)
                evaluation = self.evaluator_agent.run(summary)
                assignment = self.task_manager_agent.assign(subtask, evaluation)

                context[subtask] = {
                    "research": research,
                    "summary": summary,
                    "evaluation": evaluation,
                    "assignment": assignment
                }

            except Exception as e:
                context[subtask] = {
                    "research": "Agent error",
                    "summary": "",
                    "evaluation": {
                        "quality": 0.0,
                        "feedback": f"Agent failure: {str(e)}"
                    },
                    "assignment": {
                        "status": "error",
                        "assigned_role": "None",
                        "message": f"❌ Subtask '{subtask}' failed due to agent error."
                    }
                }

        # 📊 Step 3: Aggregate Score
        try:
            scores = [c["evaluation"]["quality"] for c in context.values() if isinstance(c["evaluation"], dict)]
            average_quality = sum(scores) / len(scores) if scores else 0.0
        except Exception as e:
            average_quality = 0.0
            print(f"⚠️ Evaluation error: {str(e)}")

        # 🔁 Step 4: Recursive Retry
        if average_quality < 0.7 and self.depth < self.max_depth:
            self.depth += 1
            print(f"\n🔁 Re-running MetaAgent (depth={self.depth}) due to low quality score: {average_quality}")
            return self.execute()

        # ✅ Final Output
        return {
            "context": context,
            "score": {
                "quality": round(average_quality, 2),
                "feedback": "Agent pass complete with evaluations and assignments."
            }
        }

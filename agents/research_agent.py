from utils.web_search import run_langsearch  # 🔄 Updated function name

class ResearchAgent:
    def run(self, subtask):
        query = self.preprocess_query(subtask)
        print(f"[ResearchAgent] Query: {query}")  # 🔍 Debug log
        return run_langsearch(query)

    def preprocess_query(self, subtask):
        """
        Cleans up the subtask prompt to extract a usable search query.
        """
        if "Break down the task" in subtask:
            return subtask.split("Break down the task")[-1].strip(":' ")
        return subtask.strip()

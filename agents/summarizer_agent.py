from utils.local_llm import query_local_llm

class SummarizerAgent:
    def run(self, text):
        if isinstance(text, list):
            text = "\n".join(text)

        if not text or len(text.strip()) < 20:
            return "Not enough content to summarize."

        prompt = f"Summarize the following content:\n{text}"
        try:
            return query_local_llm(prompt)
        except Exception as e:
            return f"Summarization failed: {str(e)}"

import re

class EvaluatorAgent:
    def __init__(self):
        # 🔍 Define semantic anchors for relevance scoring
        self.keywords = ["policy", "impact", "solution", "data", "community", "architecture", "agent", "modular"]

    def run(self, summary):
        """
        Evaluates summary quality based on length, clarity, and semantic relevance.
        Returns a score and feedback for agentic recursion.
        """
        if not summary or len(summary.strip()) < 30:
            return {
                "quality": 0.3,
                "feedback": "Summary too short or vague. Needs refinement."
            }

        clean_summary = re.sub(r"\s+", " ", summary.strip())
        length_score = min(len(clean_summary) / 120, 1.0)

        keyword_hits = sum(1 for word in self.keywords if word in clean_summary.lower())
        keyword_score = keyword_hits / len(self.keywords)

        clarity_score = 1.0 if "." in clean_summary and clean_summary.count(".") >= 2 else 0.5

        final_score = round((length_score + keyword_score + clarity_score) / 3, 2)

        feedback = (
            "✅ Strong summary with relevant insights and structure."
            if final_score > 0.75 else
            "⚠️ Partial coverage. Consider deeper analysis or clearer phrasing."
        )

        return {
            "quality": final_score,
            "feedback": feedback
        }

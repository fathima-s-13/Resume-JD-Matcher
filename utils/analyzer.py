import json
import re
import google.generativeai as genai


ANALYSIS_PROMPT = """You are an expert technical recruiter and career coach.
Analyze this resume against the job description below.

RESUME ({filename}):
{resume_text}

JOB DESCRIPTION:
{jd_text}

Return a JSON object with exactly these fields and nothing else — no preamble, no markdown fences:
{{
  "fit_score": "X/10",
  "recommendation": one of ["Strong Fit", "Good Fit", "Partial Fit", "Weak Fit"],
  "strengths": [list of 3-5 specific strengths relevant to the JD],
  "gaps": [list of 3-5 specific missing skills or experience areas],
  "suggestions": [list of 2-3 actionable suggestions for the candidate to improve fit],
  "summary": "2-3 sentence overall assessment"
}}"""


class GapAnalyzer:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    def analyze(self, resume_text: str, jd_text: str, filename: str) -> dict:
        """Generate structured gap analysis using Gemini."""
        prompt = ANALYSIS_PROMPT.format(
            filename=filename,
            resume_text=resume_text[:3000],
            jd_text=jd_text[:2000]
        )

        try:
            response = self.model.generate_content(prompt)
            raw = response.text.strip()

            # Strip markdown fences if present
            raw = re.sub(r"^```json\s*", "", raw)
            raw = re.sub(r"\s*```$", "", raw)

            return json.loads(raw)

        except json.JSONDecodeError:
            return {
                "fit_score": "N/A",
                "recommendation": "Error",
                "strengths": ["Could not parse response"],
                "gaps": ["Could not parse response"],
                "suggestions": ["Please try again"],
                "summary": "There was an error generating the analysis. Please try again."
            }
        except Exception as e:
            return {
                "fit_score": "N/A",
                "recommendation": "Error",
                "strengths": [],
                "gaps": [],
                "suggestions": [],
                "summary": f"Error: {str(e)}"
            }

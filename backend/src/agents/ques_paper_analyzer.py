from litellm import completion
import os
from dotenv import load_dotenv
import re
import json
from typing import Dict, List, Any, Optional

load_dotenv()

api_key = os.environ["GROQ_API_KEY"]


def _clean_llm_json(raw_output: str) -> dict:
    # Remove markdown-style triple backticks if present
    if raw_output.startswith("```json"):
        raw_output = re.sub(r"^```json\s*|```$", "", raw_output.strip(), flags=re.IGNORECASE)

    # Attempt to parse JSON
    try:
        return json.loads(raw_output)
    except json.JSONDecodeError as e:
        return {"error": "Invalid JSON response", "raw_output": raw_output, "exception": str(e)}
    
def analyze_question_paper(question_paper_text: str) -> Dict[str, Any]:
    """Analyze question paper text using LLM to extract structured information."""
    if not question_paper_text.strip():
        return {"error": "Empty question paper text provided"}
    
    prompt = f"""
    You are an academic question paper analyzer. Analyze the following question paper text and extract structured information in JSON format.

    Extract the following information:
    - academic_session: (string) e.g., "2024-25", "May 2023"
    - subject: (string) subject name if mentioned
    - duration: (string) exam duration if mentioned
    - max_marks: (integer) maximum marks for the paper
    - sections: (array) list of sections with their details
    - question_types: (object) count of different question types (MCQ, descriptive, etc.)
    - topics_covered: (array) list of topics/subjects covered
    - marks_distribution: (object) marks allocated to different sections/question types
    - total_questions: (integer) total number of questions
    - difficulty_analysis: (object) estimated difficulty breakdown

    Question Paper Text:
    {question_paper_text}

    Return ONLY valid JSON without any markdown formatting or explanations.
    """

    try:
        response = completion(
            model="groq/gemma2-9b-it",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            stream=False,
        )

        # Safe chain to avoid attribute errors
        extracted = getattr(response.choices[0].message, "content", "")     #type: ignore
        if extracted is None:
            return {"error": "No response from LLM"}
        extracted = extracted.strip()
        extracted = _clean_llm_json(extracted)

        return json.loads(extracted)
    except json.JSONDecodeError as e:
        return {
            "error": "Failed to parse JSON",
            "raw_output": extracted,        #type: ignore
            "exception": str(e),
            "analysis_status": "failed"
        }
    except Exception as e:
        return {
            "error": f"Analysis failed: {str(e)}",
            "analysis_status": "failed"
        }


def extract_question_patterns(question_paper_text: str) -> Dict[str, Any]:
    """Extract specific question patterns and formats from the question paper."""
    if not question_paper_text.strip():
        return {"error": "Empty question paper text provided"}
    
    prompt = f"""
    Analyze this question paper and identify recurring patterns. Extract:

    1. Question numbering patterns (Q1, Q2, 1., a), etc.)
    2. Instruction patterns ("Attempt all questions", "Choose any 5", etc.)
    3. Marks indication patterns ("[5 marks]", "(10)", etc.)
    4. Section headers and their characteristics
    5. Question formats (Multiple choice, Fill in blanks, Short answer, etc.)

    Question Paper Text:
    {question_paper_text}

    Return analysis in JSON format focusing on structural patterns that repeat across questions.
    """

    try:
        response = completion(
            model="groq/gemma2-9b-it",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            stream=False,
        )

        extracted = getattr(response.choices[0].message, "content", "")     #type: ignore
        if extracted is None:
            return {"error": "No response from LLM"}
        extracted = extracted.strip()
        extracted = _clean_llm_json(extracted)

        return json.loads(extracted)
    except json.JSONDecodeError as e:
        return {"patterns": "Could not extract patterns", "raw_output": extracted, "exception": str(e)}     #type: ignore
    except Exception as e:
        return {"error": f"Pattern extraction failed: {str(e)}"}


def compare_question_papers(papers: List[str]) -> Dict[str, Any]:
    """Compare multiple question papers to identify trends and patterns."""
    if len(papers) < 2:
        return {"error": "At least 2 question papers required for comparison"}

    combined_text = "\n\n--- PAPER SEPARATOR ---\n\n".join(papers)
    
    prompt = f"""
    Compare these multiple question papers and identify:

    1. Common topics that appear across papers
    2. Question format trends over time
    3. Marks distribution patterns
    4. Difficulty progression
    5. Topics that are frequently repeated
    6. New topics that have been introduced
    7. Topics that have been discontinued

    Papers to compare:
    {combined_text}

    Provide analysis in JSON format with insights about trends and patterns.
    """

    try:
        response = completion(
            model="groq/gemma2-9b-it",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            stream=False,
        )

        extracted = getattr(response.choices[0].message, "content", "")     #type: ignore
        if extracted is None:
            return {"error": "No response from LLM"}
        extracted = extracted.strip()
        extracted = _clean_llm_json(extracted)

        return json.loads(extracted)
    except json.JSONDecodeError as e:
        return {"comparison": "Could not analyze papers", "raw_output": extracted, "exception": str(e)}     #type: ignore
    except Exception as e:
        return {"error": f"Comparison failed: {str(e)}", "paper_count": len(papers)}


def predict_next_paper_structure(question_papers: List[str], syllabus_text: Optional[str] = None) -> dict:
    if not question_papers:
        return {"error": "No question papers provided for prediction"}
    
    papers_text = "\n\n--- PAPER SEPARATOR ---\n\n".join(question_papers)
    context = f"Historical Question Papers:\n{papers_text}"
    if syllabus_text:
        context += f"\n\nCurrent Syllabus:\n{syllabus_text}"

    prompt = f"""
    Based on the historical question papers provided{' and current syllabus' if syllabus_text else ''}, predict the structure and likely content of the next question paper.

    Provide predictions for:
    1. Predicted question paper structure and content
    2. Likely question types and their distribution
    3. Topics most likely to appear
    4. Estimated marks distribution
    5. Sections structure
    6. Difficulty level expectations
    7. New topics that might be introduced
    8. Pattern analysis and recommendations

    Return ONLY valid JSON. Do not include any explanations, markdown formatting, or additional text.
    {context}
    """

    try:
        response = completion(
            model="groq/gemma2-9b-it",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            stream=False,
        )

        raw_output = getattr(response.choices[0].message, "content", "").strip()  # type: ignore
        if not raw_output:
            return {"error": "No response from LLM"}

        # Clean and parse the raw output
        cleaned_output = _clean_llm_json(raw_output)
        if "error" in cleaned_output:
            return {
                "prediction": "Could not generate prediction",
                "raw_output": raw_output,
                "exception": cleaned_output.get("exception"),
                "input_papers": len(question_papers),
                "has_syllabus": syllabus_text is not None
            }

        # Format the response
        return format_prediction_response(
            prediction=cleaned_output,
            raw_output=raw_output,
            input_papers=len(question_papers),
            has_syllabus=syllabus_text is not None
        )
    except Exception as e:
        return {
            "error": f"Prediction failed: {str(e)}",
            "input_papers": len(question_papers),
            "has_syllabus": syllabus_text is not None
        }

def format_prediction_response(prediction: dict, raw_output: str, input_papers: int, has_syllabus: bool) -> dict:
    # Parse raw_output into JSON if possible
    try:
        parsed_raw_output = json.loads(raw_output)
    except json.JSONDecodeError:
        parsed_raw_output = raw_output  # Keep as string if parsing fails

    return {
        "prediction": prediction.get("predicted_question_paper_structure_and_content", "Could not generate prediction"),
        "raw_output": parsed_raw_output,
        "likely_question_types_and_distribution": prediction.get("likely_question_types_and_their_distribution", []),
        "topics_most_likely_to_appear": prediction.get("topics_most_likely_to_appear", []),
        "estimated_marks_distribution": prediction.get("estimated_marks_distribution", {}),
        "sections_structure": prediction.get("sections_structure", []),
        "difficulty_level_expectations": prediction.get("difficulty_level_expectations", ""),
        "new_topics_that_might_be_introduced": prediction.get("new_topics_that_might_be_introduced", []),
        "pattern_analysis_and_recommendations": prediction.get("pattern_analysis_and_recommendations", ""),
        "input_papers": input_papers,
        "has_syllabus": has_syllabus
    }

def comprehensive_question_paper_analysis(question_paper_text: str) -> Dict[str, Any]:
    """
    Perform comprehensive analysis combining all the above functions.
    """
    if not question_paper_text.strip():
        return {"error": "Empty question paper text provided"}
    
    basic_analysis = analyze_question_paper(question_paper_text)
    pattern_analysis = extract_question_patterns(question_paper_text)
    
    return {
        "basic_analysis": basic_analysis,
        "pattern_analysis": pattern_analysis,
        "analyzer_version": "1.0"
    }

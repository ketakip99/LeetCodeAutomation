import requests
import time
from google import genai
from config import GEMINI_API_KEY, OPENROUTER_API_KEY, OPENROUTER_MODEL

def get_github_solution(frontend_id):
    """
    Fallback: Fetches a solution from the walkccc/leetcode GitHub repository.
    """
    try:
        # Frontend ID needs to be 4-digit padded (e.g. 1 -> 0001)
        padded_id = f"{int(frontend_id):04d}"
        url = f"https://raw.githubusercontent.com/walkccc/leetcode/main/solutions/python3/{padded_id}.py"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return f"# Solution fetched from GitHub (walkccc/leetcode)\n\n{response.text}"
    except Exception:
        pass
    return None

def get_openrouter_solution(problem_title, problem_content, difficulty):
    """
    Fetches a solution from OpenRouter API.
    """
    if not OPENROUTER_API_KEY:
        return None
        
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/ketakiparanjape/LeetcodeAutomation",
    }
    
    prompt = f"""
    You are an expert software engineer. Generate a clear, efficient Python solution for the following LeetCode problem.
    The solution should follow the standard LeetCode class/function format.
    Include a brief explanation of the time and space complexity.
    
    Problem Title: {problem_title}
    Difficulty: {difficulty}
    
    Problem Description:
    {problem_content}
    
    Return only the python code block and complexity explanation.
    """
    
    data = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            print(f"OpenRouter API error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"OpenRouter exception: {e}")
    return None

def generate_solution(problem_title, problem_content, difficulty, frontend_id):
    """
    Generates a Python solution for the given LeetCode problem.
    Priority: OpenRouter > Gemini > GitHub Fallback
    """
    # 1. Try OpenRouter (Primary)
    print(f"Attempting OpenRouter solution for {problem_title}...")
    or_sol = get_openrouter_solution(problem_title, problem_content, difficulty)
    if or_sol:
        return or_sol

    # 2. Try Gemini (Secondary)
    if GEMINI_API_KEY and "expired" not in GEMINI_API_KEY.lower():
        print(f"Attempting Gemini solution for {problem_title}...")
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        prompt = f"""
        You are an expert software engineer. Generate a clear, efficient Python solution for the following LeetCode problem.
        The solution should follow the standard LeetCode class/function format.
        Include a brief explanation of the time and space complexity.
        
        Problem Title: {problem_title}
        Difficulty: {difficulty}
        
        Problem Description:
        {problem_content}
        
        Return only the python code block and complexity explanation.
        """
        
        for attempt in range(2): # Reduced retries since we have OpenRouter now
            try:
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=prompt
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                error_msg = str(e)
                print(f"Gemini attempt {attempt + 1} failed: {error_msg}")
                if "429" in error_msg:
                    time.sleep(10)
                elif "400" in error_msg and "expired" in error_msg.lower():
                    break 
                else:
                    time.sleep(2)

    # 3. Fallback to GitHub
    print(f"Falling back to GitHub solution for {problem_title}...")
    github_sol = get_github_solution(frontend_id)
    if github_sol:
        return github_sol

    return "# Could not generate/fetch solution. Please check your API keys or LeetCode link.\n\ndef solve():\n    pass"

if __name__ == "__main__":
    # Mock test
    test_title = "Two Sum"
    test_content = "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target."
    test_difficulty = "Easy"
    test_id = "1"
    
    print(f"Generating solution for {test_title}...")
    solution = generate_solution(test_title, test_content, test_difficulty, test_id)
    print(solution)

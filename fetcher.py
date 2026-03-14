import requests
import random
from config import LEETCODE_API_URL
from storage import is_problem_sent

def get_problem_list(limit=50, skip=0, filters={}):
    """
    Fetches a list of problems from LeetCode.
    """
    query = """
    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
      problemsetQuestionList: questionList(
        categorySlug: $categorySlug
        limit: $limit
        skip: $skip
        filters: $filters
      ) {
        total: totalNum
        questions: data {
          acRate
          difficulty
          freqBar
          questionFrontendId
          isFavor
          isPaidOnly
          status
          title
          titleSlug
          topicTags {
            name
            id
            slug
          }
          hasSolution
          hasVideoSolution
        }
      }
    }
    """
    variables = {
        "categorySlug": "",
        "skip": skip,
        "limit": limit,
        "filters": filters
    }
    
    response = requests.post(LEETCODE_API_URL, json={"query": query, "variables": variables})
    if response.status_code == 200:
        return response.json()["data"]["problemsetQuestionList"]["questions"]
    else:
        raise Exception(f"Failed to fetch problems: {response.status_code}, {response.text}")

def get_question_detail(title_slug):
    """
    Fetches the detail (content) of a specific question.
    """
    query = """
    query questionContent($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        content
        mysqlSchemas
        dataSchemas
      }
    }
    """
    variables = {"titleSlug": title_slug}
    response = requests.post(LEETCODE_API_URL, json={"query": query, "variables": variables})
    if response.status_code == 200:
        return response.json()["data"]["question"]["content"]
    else:
        raise Exception(f"Failed to fetch question detail: {response.status_code}, {response.text}")

def fetch_daily_problems(count=5, difficulty=None, tags=[]):
    """
    Selects unique problems based on criteria and historical record.
    """
    filters = {}
    if difficulty:
        filters["difficulty"] = difficulty.upper()
    # Note: Complex tag filtering might require different GraphQL structure, 
    # but we can filter locally or fetch more and sample.
    
    questions = get_problem_list(limit=100, filters=filters)
    
    # Filter out paid-only and already sent
    available = [q for q in questions if not q["isPaidOnly"] and not is_problem_sent(q["titleSlug"])]
    
    if len(available) < count:
        # If not enough, maybe fetch more or relax constraints
        print("Warning: Not enough unique problems found with current filters.")
    
    selected = random.sample(available, min(len(available), count))
    
    # Enrich with content
    for q in selected:
        q["content"] = get_question_detail(q["titleSlug"])
        
    return selected

if __name__ == "__main__":
    # Test fetch
    problems = fetch_daily_problems(count=1, difficulty="Easy")
    for p in problems:
        print(f"Fetched: {p['title']} ({p['difficulty']})")
        # print(p["content"][:200]) # Snippet

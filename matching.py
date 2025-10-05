# matching.py
from typing import List, Dict, Any

"""
This files main purpose to to match students together based on the following cetegories:
    - Courses / Subjects being taken
    - Study Goals
    - Availability 
"""

# Helper Functions

def _courses(user: Dict[str, Any]) -> set:
    return set(user.get("courses") or user.get("subjects") or [])

def _times(user: Dict[str, Any]) -> set:
    return set(user.get("study_times") or user.get("availability") or [])

def _goals(user: Dict[str, Any]) -> set:
    return set(user.get("goals") or [])


# Core Matching Functions
def calculate_match_score(user1: Dict[str, Any], user2: Dict[str, Any]) -> float:
    """
    Calculate how compatible two users are and returns a score from 0-100.
    Categories:
        - Courses: 40%
        - Goals: 30%
        - Availability: 30%
    """

    total_score = 0.0

    # 1. Course Matching (Worth 40% of total match calculations)
    user1_courses = _courses(user1)
    user2_courses = _courses(user2)
    if user1_courses:
        shared_courses = user1_courses & user2_courses
        course_score = (len(shared_courses) / len(user1_courses)) * 40
        total_score += course_score

    # 2. Goals Matching (30%)
    user1_goals = _goals(user1)
    user2_goals = _goals(user2)
    if user1_goals:
        shared_goals = user1_goals & user2_goals
        goal_score = (len(shared_goals) / len(user1_goals)) * 30
        total_score += goal_score

    # 3. Availability Matching (30%)
    user1_times = _times(user1)
    user2_times = _times(user2)
    if user1_times:
        shared_times = user1_times & user2_times
        time_score = (len(shared_times) / len(user1_times)) * 30
        total_score += time_score

    return round(total_score, 2)


def similarity(student1: Dict[str, Any], student2: Dict[str, Any]) -> float:
    """
    Alternative similarity calculation. Gives equal weight to categories helping us test and compare in a simpler way.
    """
    score = 0
    categories = 0  # count how many categories we compare

    # Courses / Subjects
    if _courses(student1) and _courses(student2):
        categories += 1
        common = len(_courses(student1) & _courses(student2))
        avg_len = (len(_courses(student1)) + len(_courses(student2))) / 2
        if avg_len > 0:
            score += (common / avg_len) * 100

    # Goals
    if _goals(student1) and _goals(student2):
        categories += 1
        common = len(_goals(student1) & _goals(student2))
        avg_len = (len(_goals(student1)) + len(_goals(student2))) / 2
        if avg_len > 0:
            score += (common / avg_len) * 100

    # Availability
    if _times(student1) and _times(student2):
        categories += 1
        common = len(_times(student1) & _times(student2))
        avg_len = (len(_times(student1)) + len(_times(student2))) / 2
        if avg_len > 0:
            score += (common / avg_len) * 100

    # Avoid division by zero
    if categories == 0:
        return 0.0

    return round(score / categories, 2)


# Match Utilities
def find_matches(current_user: Dict[str, Any],
                 all_users: List[Dict[str, Any]],
                 min_score: float = 20.0) -> List[Dict[str, Any]]:
    """
    Find all matches for the current_user in the user list.
    Only include matches above the min_score threshold.
    Returns list of dicts with: user, score, shared_courses, shared_times
    """
    matches = []

    for other in all_users:
        # Skip self (by id if present, else by name)
        if current_user.get("id") == other.get("id"):
            continue
        if current_user.get("name") == other.get("name"):
            continue

        score = calculate_match_score(current_user, other)

        if score >= min_score:
            matches.append({
                "user": other,
                "score": score,
                "shared_courses": list(_courses(current_user) & _courses(other)),
                "shared_times": list(_times(current_user) & _times(other))
            })

    # Sort highest score first
    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches


def get_top_matches(current_user: Dict[str, Any],
                    all_users: List[Dict[str, Any]],
                    limit: int = 10) -> List[Dict[str, Any]]:
    # Return only the top N matches for the current user.
    return find_matches(current_user, all_users, min_score=0.0)[:limit]


def filter_matches_by_course(matches: List[Dict[str, Any]], course: str) -> List[Dict[str, Any]]:
    # Filter matches to only include users in a specific course.
    return [m for m in matches if course in _courses(m["user"])]


def filter_matches_by_time(matches: List[Dict[str, Any]], time_slot: str) -> List[Dict[str, Any]]:
    # Filter matches to only include users available in a specific time slot.
    return [m for m in matches if time_slot in _times(m["user"])]


def get_match_statistics(current_user: Dict[str, Any], all_users: List[Dict[str, Any]]) -> Dict[str, Any]:
    # Return summary statistics about matches for one user.
    matches = find_matches(current_user, all_users, min_score=0.0)

    if not matches:
        return {
            "total_users": len(all_users) - 1,
            "total_matches": 0,
            "good_matches": 0,
            "avg_score": 0,
            "best_match_score": 0,
            "courses_with_matches": len(_courses(current_user))
        }

    scores = [m["score"] for m in matches]
    good_matches = [m for m in matches if m["score"] >= 50]

    return {
        "total_users": len(all_users) - 1,
        "total_matches": len([m for m in matches if m["score"] >= 20]),
        "good_matches": len(good_matches),
        "avg_score": round(sum(scores) / len(scores), 1),
        "best_match_score": max(scores),
        "courses_with_matches": len(_courses(current_user))
    }


def match_all_students(all_users: List[Dict[str, Any]], top_n: int = 3) -> Dict[str, List]:
    """
    Match every student in the list with others.
    Returns dictionary: { student_name: [top matches...] }
    """
    results = {}
    for u in all_users:
        results[u.get("name")] = find_matches(u, all_users)[:top_n]
    return results

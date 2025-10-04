# matching.py

def calculate_match_score(user1, user2):
    """
    Calculate how compatible two users are.
    Returns a score from 0-100.

    Args:
        user1/user2 (dict): Dictionary with user data

    Returns:
        float: Match score (0-100)
    """
    total_score = 0

    # 1. Course Matching (40%)
    user1_courses = set(user1.get("subjects", []))
    user2_courses = set(user2.get("subjects", []))
    shared_courses = user1_courses & user2_courses

    if user1_courses:
        course_score = (len(shared_courses) / len(user1_courses)) * 40
        total_score += course_score

    # 2. Goals Matching (30%)
    user1_goals = set(user1.get("goals", []))
    user2_goals = set(user2.get("goals", []))
    shared_goals = user1_goals & user2_goals

    if user1_goals:
        goal_score = (len(shared_goals) / len(user1_goals)) * 30
        total_score += goal_score

    # 3. Availability Matching (30%)
    user1_times = set(user1.get("availability", []))
    user2_times = set(user2.get("availability", []))
    shared_times = user1_times & user2_times

    if user1_times:
        time_score = (len(shared_times) / len(user1_times)) * 30
        total_score += time_score

    return round(total_score, 2)


def find_matches(user, all_users, top_n=3):
    """
    Find top matches for a single user.

    Args:
        user (dict): The user to match
        all_users (list): List of user dictionaries
        top_n (int): Number of best matches to return

    Returns:
        list: List of (other_user, score) tuples
    """
    scores = []
    for other in all_users:
        if other["name"] != user["name"]:  # don't match with self
            score = calculate_match_score(user, other)
            scores.append((other["name"], score))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_n]


def match_all_students(all_users, top_n=3):
    """
    Run matching for an entire cohort.

    Args:
        all_users (list): List of all student dictionaries
        top_n (int): Number of matches per student

    Returns:
        dict: {student_name: [(match_name, score), ...]}
    """
    results = {}
    for user in all_users:
        results[user["name"]] = find_matches(user, all_users, top_n)
    return results


# Sample Test Run

if __name__ == "__main__":
    students = [
        {
            "name": "Alice",
            "subjects": ["COMP 1701", "MATH 1200", "GNED 1101"],
            "goals": ["Exam prep", "Assignments"],
            "availability": ["Mon 10:00", "Mon 10:30", "Wed 11:00", "Fri 13:00"]
        },
        {
            "name": "Bob",
            "subjects": ["COMP 1701", "MATH 1200", "GNED 1101"],
            "goals": ["Exam prep", "Assignments"],
            "availability": ["Mon 10:00", "Mon 10:30", "Wed 11:00", "Fri 13:00"]
        },
        {
            "name": "Charlie",
            "subjects": ["DATA 2721", "MATH 1200", "GNED 1401"],
            "goals": ["Exam prep"],
            "availability": ["Mon 10:00", "Wed 11:00", "Thu 14:30"]
        }
    ]

    matches = match_all_students(students, top_n=2)
    for student, match_list in matches.items():
        print(f"\nBest matches for {student}:")
        for partner, score in match_list:
            print(f"  {partner} (Score: {score})")

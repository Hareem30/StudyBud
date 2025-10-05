# test_matching.py
from matching import similarity  # ✅ import similarity

def test_perfect_match():
    user1 = {
        'id': 0,
        'name': 'Alice',
        'subjects': ['CS101', 'MATH201'],
        'availability': ['Morning'],
        'goals': ['Group study']
    }
    user2 = {
        'id': 1,
        'name': 'Bob',
        'subjects': ['CS101', 'MATH201'],
        'availability': ['Morning'],
        'goals': ['Group study']
    }
    score = similarity(user1, user2)  # ✅ correct call
    print(f"Perfect match test: {score}% (expected: 100%)")
    assert score == 100.0

def test_no_match():
    user1 = {
        'id': 0,
        'name': 'A',
        'subjects': ['CS101'],
        'availability': ['Morning'],
        'goals': ['Group study']
    }
    user2 = {
        'id': 1,
        'name': 'B',
        'subjects': ['PHYS101'],
        'availability': ['Night'],
        'goals': ['Solo']
    }
    score = similarity(user1, user2)  # ✅ also use similarity here
    print(f"No match test: {score}% (expected: 0%)")
    assert score == 0.0

if __name__ == "__main__":
    test_perfect_match()
    print("✓ perfect test passed")
    test_no_match()
    print("✓ no-match test passed")

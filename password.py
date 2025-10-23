import re

def check_password_strength(password):
    """
    Checks the strength of a password based on length, uppercase, digits, and special characters.
    Returns a score (0-4) and strength level.
    """
    score = 0

    # Check length
    if len(password) >= 8:
        score += 1

    # Check for uppercase
    if re.search(r'[A-Z]', password):
        score += 1

    # Check for digits
    if re.search(r'\d', password):
        score += 1

    # Check for special characters
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1

    # Determine strength
    if score <= 1:
        strength = "weak"
    elif score <= 3:
        strength = "medium"
    else:
        strength = "strong"

    return score, strength

if __name__ == "__main__":
    password = input("Enter a password to check its strength: ")
    score, strength = check_password_strength(password)
    print(f"Password score: {score}/4")
    print(f"Password strength: {strength}")

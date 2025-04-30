import secrets
import string

def generate_secure_password(length=24):
    """
    Generate a highly secure cryptographic password.
    Ensures at least one lowercase, uppercase, digit, and special character.
    """
    if length < 12:
        raise ValueError("Password length should be at least 12 characters for high security.")

    alphabet = string.ascii_letters + string.digits + string.punctuation

    # Ensure at least one character from each category
    password = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice(string.punctuation),
    ]

    # Fill the rest of the password length with random choices
    password += [secrets.choice(alphabet) for _ in range(length - 4)]

    # Shuffle to prevent predictable placement
    secrets.SystemRandom().shuffle(password)

    return ''.join(password)

if __name__ == "__main__":
    # Example CLI usage
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate a highly secure cryptographic password."
    )
    parser.add_argument(
        "-l", "--length", type=int, default=24, help="Password length (default: 24)"
    )
    args = parser.parse_args()

    print(generate_secure_password(args.length))

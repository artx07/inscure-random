import random
import time

def generate_insecure_password(seed: int, length: int = 12) -> str:
    """Generate an insecure random password based on a given seed."""
    random.seed(seed)  # Use the provided seed to initialize the random number generator
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def demonstrate_insecure_random_attack(approx_seed: int, length: int = 12, range_seconds: int = 5) -> str:
    """
    Demonstrate an attack on an insecure random password generator.
    
    :param approx_seed: The approximate UNIX time when the password was generated.
    :param length: The length of the password to generate.
    :param range_seconds: The range of seconds around the approximate seed to consider.
    :return: The matching password and seed if found, otherwise None.
    """
    print(f"Attempting to crack the password generated around seed: {approx_seed} within +/- {range_seconds} seconds")

    # Try all possible seeds in the range around the approximate seed
    for offset in range(-range_seconds, range_seconds + 1):
        seed = approx_seed + offset
        guessed_password = generate_insecure_password(seed, length)

        print(f"Trying seed {seed}: {guessed_password}")

    print("Password cracking attempt finished.")
    return None

if __name__ == "__main__":
    # Accept user input for the approximate seed time
    approx_seed = int(input("Enter the approximate UNIX time seed (e.g., 1693058390): "))
    range_seconds = int(input("Enter the range of seconds to consider around the approximate seed (e.g., 5): "))

    # Demonstrate the attack using the provided approximate seed
    demonstrate_insecure_random_attack(approx_seed, length=12, range_seconds=range_seconds)

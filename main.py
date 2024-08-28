from fastapi import FastAPI, HTTPException, Request, Response,Form
from fastapi.middleware.cors import CORSMiddleware
import random,time
import smtplib 
import secrets


app = FastAPI()


SMTP_SERVER = 'localhost'
SMTP_PORT = 1025



def send_email(to_email: str, new_password: str):
    """Send an email with the new password."""
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            #server.starttls()
            #server.login(SMTP_USERNAME, SMTP_PASSWORD)
            from_email = 'no-reply@example.com'
            message = f"Subject: Password Reset\n\nYour new 'random' password: {new_password}"
            server.sendmail(from_email,to_email, message)
    except Exception as e:
        print(f"Failed to send email: {e}")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #better load with http server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/reset-password/")
async def reset_password(request: Request,response: Response , email: str = Form(...)):
    #data = await request.json()
    #email = data.get("email")
    
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    
    
    
    """Generate random password"""
    # Seed random number generator with the current UNIX time
    #we can use this for conversion of your time https://www.unixtimestamp.com/
    seed = int(time.time())
    global seed_global
    seed_global = seed #This is for create get access to the seed in all the code xd
    random.seed(seed)
    
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    password = ''.join(random.choice(characters) for _ in range(20))
    print(f"Generated password with seed {seed}: {password}")  



    # Send the new password to the email address
    send_email(email, password)
    global email_client
    global password_client

    email_client = email.strip()
    password_client = password.strip()


    response.headers["Time"] = str(seed) #Explain about the header with the response and show some examples
   
    return {"message": "If the email exists in our system, a new password has been sent."}


@app.post("/login")
async def login(request: Request,response: Response , email: str = Form(...),password:str = Form(...)):
    response.headers["Time"] = str(seed_global)
    
    if email.strip() == email_client.strip() and password.strip() == password_client.strip():
        print("Access grated")
        return ("Access grated")

    else:
        print("Access wrong, bad password or email")
        return("Access wrong, bad password or email")
    








if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

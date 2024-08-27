from fastapi import FastAPI, HTTPException, Request, Response,Form
from fastapi.middleware.cors import CORSMiddleware
import random,time
import smtplib 

app = FastAPI()


# Email settings (configure these as needed)
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
    
    
    
    """Generate an insecure random password based on UNIX time."""
    # Seed random number generator with the current UNIX time
    seed = int(time.time())
    random.seed(seed)
    
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    password = ''.join(random.choice(characters) for _ in range(12))
    print(f"Generated password with seed {seed}: {password}")  # Debugging: shows how the password is generated



    # Send the new password to the email address
    send_email(email, password)
    response.headers["Time"] = str(seed)
   
    return {"message": "If the email exists in our system, a new password has been sent."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

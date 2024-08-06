from flask import Flask, render_template, request, jsonify
import re
import random
import string
import secrets

app = Flask(__name__)

# Function to generate a strong password
def generate_password(length=12):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password

# Function to check password criteria
def check_criteria(password):
    criteria = {
        "length": len(password) >= 8,
        "lowercase": re.search(r'[a-z]', password) is not None,
        "uppercase": re.search(r'[A-Z]', password) is not None,
        "digit": re.search(r'\d', password) is not None,
        "special": re.search(r'[!@#$%^&*(),.?":{}|<>]', password) is not None
    }
    return criteria

# Function to suggest a password based on criteria
def suggest_password(password, criteria):
    additions = ""
    if not criteria["uppercase"]:
        additions += random.choice(string.ascii_uppercase)
    if not criteria["special"]:
        additions += random.choice(string.punctuation)
    if not criteria["digit"]:
        additions += random.choice(string.digits)
    
    # Ensure total length is at least 8 characters
    if len(password) + len(additions) < 8:
        additions += ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=8 - len(password) - len(additions)))
    
    return password + additions

# Function to assess password strength
def password_strength(username, password):
    criteria = check_criteria(password)
    criteria_met = sum(criteria.values())
    
    if criteria_met == 5:
        strength = "Very Strong"
    elif criteria_met == 4:
        strength = "Strong"
    elif criteria_met == 3:
        strength = "Moderate"
    else:
        strength = "Weak"

    feedback = (
    f"Password strength: {strength}<br>\n"
    f"Criteria:<br>\n"
    f"- Length (8+ characters): {'Met' if criteria['length'] else 'Not Met'}<br>\n"
    f"- Lowercase letter: {'Met' if criteria['lowercase'] else 'Not Met'}<br>\n"
    f"- Uppercase letter: {'Met' if criteria['uppercase'] else 'Not Met'}<br>\n"
    f"- Digit: {'Met' if criteria['digit'] else 'Not Met'}<br>\n"
    f"- Special character: {'Met' if criteria['special'] else 'Not Met'}<br>\n"
)


    if criteria_met < 5:
        feedback += f"<br>Suggested Password: {suggest_password(password, criteria)}"
    
    return feedback

# Render the password strength checker form
@app.route('/')
def index():
    return render_template('index.html')

# Handle password strength check request
@app.route('/password_strength', methods=['POST'])
def password_strength_route():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username.lower() in password.lower():
        return jsonify({"feedback": "Password should not contain the username or any part of it. Please enter a different password."})
    
    return jsonify({"feedback": password_strength(username, password)})

# Generate a random password route
@app.route('/generate_password', methods=['GET'])
def generate_password_route():
    password = generate_password()
    return jsonify({"password": password})

if __name__ == '__main__':
    app.run(debug=True)
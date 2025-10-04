from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'hackathon-secret-key-2025'

# Store users in a list (simple database)
users = []

# Home page
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Create user from form data
        user = {
            'id': len(users),
            'name': request.form['name'],
            'email': request.form['email'],
            'year': request.form['year'],
            'major': request.form['major'],
            'courses': request.form.getlist('courses[]'),
            'study_times': request.form.getlist('study_times[]'),
            'study_style': request.form['study_style'],
            'noise_preference': request.form['noise_preference'],
            'bio': request.form.get('bio', ''),
            'created_at': datetime.now().isoformat()
        }
        
        users.append(user)
        session['user_id'] = user['id']
        
        return redirect(url_for('profile'))
    
    return render_template('signup.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('signup'))
    
    user_id = session['user_id']
    user = users[user_id]
    
    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5000)
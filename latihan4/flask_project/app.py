from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/monitoring')
def monitoring():
    user = {
        "name": "John Doe",
        "progress": 75,
        "recommendation": "Belajar List dan Dictionary"
    }
    stats = {
        "total_exercises": 30,
        "total_recommendations": 5,
        "mastered_materials": 10
    }
    return render_template('monitoring.html', user=user, stats=stats)

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Menggunakan port lain jika perlu


from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ranking.db'
db = SQLAlchemy(app)

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    correct_answers = db.Column(db.Integer, nullable=False)

db.create_all()

@app.route('/submit', methods=['POST'])
def submit_result():
    data = request.json
    new_result = Result(username=data['username'], correct_answers=data['correct_answers'])
    db.session.add(new_result)
    db.session.commit()
    return jsonify({"message": "Result submitted successfully!"}), 201

@app.route('/ranking', methods=['GET'])
def get_ranking():
    results = Result.query.order_by(Result.correct_answers.desc()).limit(10).all()
    ranking = [{"username": result.username, "correct_answers": result.correct_answers} for result in results]
    return jsonify(ranking), 200

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def calculate_macros(gender, age, height, weight, goal_weight, activity_level):
    if gender == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    tdee = bmr * float(activity_level)

    # Assuming a caloric deficit of 500 calories/day for weight loss
    goal_calories = tdee - 500

    # Protein: 2g/kg of current body weight
    protein = 2 * weight

    # Fats: 25% of total calories, 1g = 9 calories
    fats = (goal_calories * 0.25) / 9

    # Carbs: Remaining calories, 1g = 4 calories
    carbs = (goal_calories - (protein * 4) - (fats * 9)) / 4

    return {
        "calories": round(goal_calories),
        "protein": round(protein),
        "fats": round(fats),
        "carbs": round(carbs)
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    gender = data['gender']
    age = int(data['age'])
    height = float(data['height'])
    weight = float(data['weight'])
    goal_weight = float(data['goalWeight'])
    activity_level = data['activityLevel']

    macros = calculate_macros(gender, age, height, weight, goal_weight, activity_level)
    return jsonify(macros)

if __name__ == '__main__':
    app.run(debug=True)

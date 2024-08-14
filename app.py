from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def calculate_macros(gender, age, height_cm, weight_kg, goal_weight_kg, activity_level):
    if gender == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    tdee = bmr * float(activity_level)

    # Assuming a caloric deficit of 500 calories/day for weight loss
    goal_calories = tdee - 500

    # Protein: 2g/kg of current body weight
    protein = 2 * weight_kg

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
    height_feet = int(data['heightFeet'])
    height_inches = int(data['heightInches'])
    weight_lbs = float(data['weight'])
    goal_weight_lbs = float(data['goalWeight'])
    activity_level = data['activityLevel']

    # Convert height to cm and weight to kg
    height_cm = (height_feet * 30.48) + (height_inches * 2.54)
    weight_kg = weight_lbs / 2.205
    goal_weight_kg = goal_weight_lbs / 2.205

    macros = calculate_macros(gender, age, height_cm, weight_kg, goal_weight_kg, activity_level)
    return jsonify(macros)

if __name__ == '__main__':
    app.run(debug=True)

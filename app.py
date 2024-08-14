from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def calculate_macros(gender, age, height_cm, weight_kg, goal_weight_kg, activity_level, target_weeks):
    if gender == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    tdee = bmr * float(activity_level)

    # Calculate calorie deficit for reaching the goal weight in the target weeks
    # 1 lb of body weight is approximately 3500 calories
    weight_change = weight_kg - goal_weight_kg
    weekly_deficit = weight_change * 3500 / target_weeks
    daily_deficit = weekly_deficit / 7

    goal_calories = tdee - daily_deficit

    # Protein: 2g/kg of current body weight
    protein = 2 * weight_kg

    # Fats: 25% of total calories, 1g = 9 calories
    fats = (goal_calories * 0.25) / 9

    # Carbs: Remaining calories, 1g = 4 calories
    carbs = (goal_calories - (protein * 4) - (fats * 9)) / 4

    return {
        "bmr": round(bmr),
        "tdee": round(tdee),
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
    target_weeks = int(data['targetWeeks'])

    # Convert height to cm and weight to kg
    height_cm = (height_feet * 30.48) + (height_inches * 2.54)
    weight_kg = weight_lbs / 2.205
    goal_weight_kg = goal_weight_lbs / 2.205

    macros = calculate_macros(gender, age, height_cm, weight_kg, goal_weight_kg, activity_level, target_weeks)
    return jsonify(macros)

if __name__ == '__main__':
    app.run(debug=True)

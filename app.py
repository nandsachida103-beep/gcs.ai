from flask import Flask, request, jsonify
import data

app = Flask(__name__)

def get_answer(query):
    query_lower = query.lower()

    # Teachers
    if "teacher" in query_lower or "teachers" in query_lower or "teacher kaun" in query_lower:
        answer = "👨‍🏫 Senior Teachers:\n"
        for t in data.senior_teachers:
            extra = f" ({t['extra']})" if "extra" in t else ""
            answer += f"- {t['name']} – {t['subject']}, {t.get('qualification','')}{extra}\n"
        answer += "\n🧒 Junior Teachers:\n"
        for t in data.junior_teachers:
            answer += f"- {t['name']} – {t.get('subject','')}\n"
        answer += "\n🛎 Non-Teaching Staff:\n"
        for k, v in data.non_teaching_staff.items():
            answer += f"- {k}: {v}\n"
        return answer

    # Subject-specific (e.g., Chemistry)
    for t in data.senior_teachers:
        if t['subject'].lower() in query_lower:
            extra = f" ({t['extra']})" if "extra" in t else ""
            return f"{t['subject']} teacher is {t['name']}, {t.get('qualification','')}{extra}"

    # School timings
    if "timing" in query_lower or "time" in query_lower:
        answer = "School Timings:\n"
        for k, v in data.school_info["section_timings"].items():
            answer += f"- {k}: {v}\n"
        answer += f"- General Timing: {data.school_info['general_timing']}"
        return answer

    # Class 11 students
    if "class 11" in query_lower or "11th" in query_lower:
        answer = "Class 11 Students:\nBoys:\n"
        answer += ", ".join(data.class_11["boys"]) + "\nGirls:\n"
        answer += ", ".join(data.class_11["girls"]) + "\n"
        answer += f"Fees:\n- School Fee: ₹{data.class_11_fees['school_fee']}/month\n- Coaching Fee: ₹{data.class_11_fees['coaching_fee']}/month"
        return answer

    # Annual sports
    if "annual sports" in query_lower or "sports" in query_lower:
        return f"Annual Sports Competition is held in {data.events['Annual Sports']}"

    # Science exhibition
    if "science exhibition" in query_lower:
        return f"Science Exhibition Date: {data.events['Science Exhibition']}, Head: {data.senior_teachers[0]['name']}"

    # Best players
    if "best player" in query_lower or "cricket" in query_lower or "volleyball" in query_lower:
        return f"Best Cricket & Volleyball player of all time is {data.best_players['cricket']}"

    # Default fallback
    contacts_str = ", ".join(data.contacts)
    return f"Sorry, I don't have information about that. Please contact the school or call on {contacts_str}"

@app.route("/")
def home():
    return "Welcome to GCS AI! Ask me anything about Gurukul Convent School."

@app.route("/ask", methods=["POST"])
def ask():
    user_query = request.json.get("query", "")
    answer = get_answer(user_query)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)

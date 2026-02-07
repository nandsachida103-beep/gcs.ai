from flask import Flask, render_template, request, jsonify
from data import GCS_data

app = Flask(__name__)

contact_numbers = ["9838421968","8317001959","7518249280"]

# Language detection
def detect_language(query):
    for ch in query:
        if '\u0900' <= ch <= '\u097F':
            return "hi"
    return "en"

# Keywords
keywords = {
    "principal": ["principal","principal ka naam","principal kaun hai","principal name"],
    "director": ["director","director ka naam","director kaun hai"],
    "vice_principal": ["vice principal","up-principal","vice principal ka naam"],
    "system_manager": ["system manager","system manager ka naam"],
    "senior_chemistry": ["chemistry teacher","senior chemistry teacher","chemistry ka teacher"],
    "senior_biology": ["biology teacher","senior biology teacher","biology ka teacher"],
    "senior_physics": ["physics teacher","senior physics teacher","physics ka teacher"],
    "senior_math": ["math teacher","mathematics teacher","senior math teacher","ganit teacher"],
    "senior_english": ["english teacher","senior english teacher"],
    "senior_hindi": ["hindi teacher","senior hindi teacher"],
    "junior_math": ["junior math teacher","junior mathematics teacher","junior ganit teacher"],
    "junior_pe": ["junior pe teacher","physical education teacher","pe sir"],
    "junior_english": ["junior english teacher"],
    "junior_science": ["junior science teacher","science teacher"],
    "junior_sanskrit_art_hindi": ["sanskrit teacher","art teacher","junior hindi teacher","sweta ma’am"],
    "junior_other": ["other junior teachers","junior teachers"],
    "class_11_boys":["class 11 boys","class 11 ke ladke","11th boys"],
    "class_11_girls":["class 11 girls","class 11 ki ladkiyan","11th girls"],
    "class_11_monitor":["class 11 monitor","class 11 ka monitor"],
    "class_11_fees":["class 11 fees","11th fees","fees","tuition"],
    "final_exam":["final exam","class 11 exam","11th exam"],
    "science_exhibition":["science exhibition","science mela","vigyan pradarshani"],
    "infrastructure":["infrastructure","school facilities","lab","computer lab"],
    "transport":["transport","bus","van","school route"],
    "admission_documents":["admission documents","required documents","school admission"],
    "house_system":["house system","school houses","ghar"],
    "sports_activities":["sports","games","activities","extra curricular"],
    "best_player":["best player","cricket player","volleyball player","behtareen khiladi"],
    "school_address":["school address","school ka address"],
    "school_timings":["school timings","school ka samay","school timing"]
}

# Function to get answer
def get_answer(query):
    query = query.lower()
    lang = detect_language(query)

    # Loop through keywords
    for key, kwlist in keywords.items():
        if any(k in query for k in kwlist):
            # Map key to data
            if key=="principal":
                return GCS_data["management"]["principal"] if lang=="en" else f"प्रधानाचार्य: {GCS_data['management']['principal']}"
            if key=="director":
                return GCS_data["management"]["director"] if lang=="en" else f"निदेशक: {GCS_data['management']['director']}"
            if key=="vice_principal":
                return GCS_data["management"]["vice_principal"] if lang=="en" else f"उप-प्रधानाचार्य: {GCS_data['management']['vice_principal']}"
            if key=="system_manager":
                return GCS_data["management"]["system_manager"] if lang=="en" else f"सिस्टम प्रबंधक: {GCS_data['management']['system_manager']}"
            if key=="senior_chemistry":
                return GCS_data["teachers"]["senior"]["Chemistry"] if lang=="en" else "कुलदीप कुमार"
            if key=="senior_biology":
                return GCS_data["teachers"]["senior"]["Biology"] if lang=="en" else "विभा मैडम"
            if key=="senior_physics":
                return GCS_data["teachers"]["senior"]["Physics"] if lang=="en" else "मनीष मिश्रा"
            if key=="senior_math":
                return GCS_data["teachers"]["senior"]["Mathematics"] if lang=="en" else "मनोज द्विवेदी"
            if key=="senior_english":
                return GCS_data["teachers"]["senior"]["English"] if lang=="en" else "मोहसिन खान"
            if key=="senior_hindi":
                return GCS_data["teachers"]["senior"]["Hindi"] if lang=="en" else "कंचन शुक्ला"
            if key=="junior_math":
                return GCS_data["teachers"]["junior"]["Mathematics"] if lang=="en" else "हर्षित अग्रहरी और सुनील सर"
            if key=="junior_pe":
                return GCS_data["teachers"]["junior"]["Physical Education"] if lang=="en" else "सेहबल सर"
            if key=="junior_english":
                return GCS_data["teachers"]["junior"]["English"] if lang=="en" else "प्रिया मैडम"
            if key=="junior_science":
                return GCS_data["teachers"]["junior"]["Science"] if lang=="en" else "पूजा मैडम"
            if key=="junior_sanskrit_art_hindi":
                return GCS_data["teachers"]["junior"]["Sanskrit/Art/Hindi"] if lang=="en" else "स्वेता मैडम"
            if key=="junior_other":
                return GCS_data["teachers"]["junior"]["Other"] if lang=="en" else "आशा मैडम, लक्ष्मी मैडम और अन्य जूनियर कक्षा के शिक्षक"
            if key=="class_11_boys":
                return ", ".join(GCS_data["class_11"]["boys"]) if lang=="en" else "कक्षा 11 के लड़के: " + ", ".join(GCS_data["class_11"]["boys"])
            if key=="class_11_girls":
                return ", ".join(GCS_data["class_11"]["girls"]) if lang=="en" else "कक्षा 11 की लड़कियाँ: " + ", ".join(GCS_data["class_11"]["girls"])
            if key=="class_11_monitor":
                return GCS_data["class_11"]["monitor"] if lang=="en" else "कक्षा 11 के मॉनिटर: " + GCS_data["class_11"]["monitor"]
            if key=="class_11_fees":
                f = GCS_data["class_11"]["fees"]
                return f"School Fee: ₹{f['school_fee']}/month, Coaching Fee: ₹{f['coaching_fee']}/month" if lang=="en" else f"स्कूल शुल्क: ₹{f['school_fee']}/महीना, कोचिंग शुल्क: ₹{f['coaching_fee']}/महीना"
            if key=="final_exam":
                exams = ", ".join(GCS_data["academics"]["final_exam"])
                return f"{exams}; Start: {GCS_data['academics']['exam_start']}" if lang=="en" else f"{exams}; शुरू: {GCS_data['academics']['exam_start']}"
            if key=="science_exhibition":
                se = GCS_data["science_exhibition"]
                return f"Date: {se['date']}, Head: {se['head']}, Supporting: {', '.join(se['supporting_members'])}" if lang=="en" else f"विज्ञान प्रदर्शनी: तिथि: {se['date']}, प्रमुख: {se['head']}, सहयोगी: {', '.join(se['supporting_members'])}"
            if key=="infrastructure":
                infra = ", ".join(GCS_data["infrastructure"])
                return infra if lang=="en" else "स्कूल की सुविधाएँ: " + infra
            if key=="transport":
                t = GCS_data["transport"]
                v = t["vehicles"]
                r = ", ".join(t["routes"])
                return f"Vehicles: Buses-{v['buses']}, Vans-{v['vans']}, Force Vehicle-{v['force_vehicle']}; Routes: {r}" if lang=="en" else f"वाहन: बस-{v['buses']}, वैन-{v['vans']}, फोर्स वाहन-{v['force_vehicle']}; मार्ग: {r}"
            if key=="admission_documents":
                docs = ", ".join(GCS_data["admission_documents"])
                return docs if lang=="en" else "आवश्यक दस्तावेज़: " + docs
            if key=="house_system":
                houses = ", ".join(GCS_data["house_system"])
                return houses if lang=="en" else "हाउस सिस्टम: " + houses
            if key=="sports_activities":
                sports = ", ".join(GCS_data["sports_activities"]["sports"])
                extra = ", ".join(GCS_data["sports_activities"]["extra_curricular"])
                return f"Sports: {sports}; Activities: {extra}" if lang=="en" else f"खेल: {sports}; गतिविधियाँ: {extra}"
            if key=="best_player":
                return GCS_data["best_players"]["all_time"] if lang=="en" else "सर्वश्रेष्ठ खिलाड़ी: " + GCS_data["best_players"]["all_time"]
            if key=="school_address":
                return GCS_data["address"] if lang=="en" else "स्कूल का पता: " + GCS_data["address"]
            if key=="school_timings":
                t = GCS_data["school_details"]["timings"]
                return f"General: {t['general']}, Nursery-UKG: {t['nursery_ukg']}, Class I-XII: {t['class_i_xii']}" if lang=="en" else f"सामान्य समय: {t['general']}, नर्सरी-UKG: {t['nursery_ukg']}, कक्षा I-XII: {t['class_i_xii']}"

    # Fallback
    return f"Sorry, I don't have information. Please visit the school or contact on {', '.join(contact_numbers)}" if lang=="en" else f"माफ़ कीजिए, मुझे जानकारी नहीं है। कृपया स्कूल जाएँ या इन नंबरों पर संपर्क करें: {', '.join(contact_numbers)}"

# Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["GET"])
def ask():
    query = request.args.get("query","")
    answer = get_answer(query)
    return jsonify({"query": query, "answer": answer})

if __name__=="__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify
from data import GCS_data

app = Flask(__name__)

# Contact numbers for fallback
contact_numbers = ["9838421968", "8317001959", "7518249280"]

# Keywords mapping for English, Hindi, Hinglish
keywords = {
    # Management
    "principal": {
        "keywords": ["principal", "principal ka naam", "principal kaun hai", "principal name"],
        "answer": {
            "en": GCS_data["management"]["principal"],
            "hi": f"प्रधानाचार्य: {GCS_data['management']['principal']}"
        }
    },
    "director": {
        "keywords": ["director", "director ka naam", "director kaun hai"],
        "answer": {
            "en": GCS_data["management"]["director"],
            "hi": f"निदेशक: {GCS_data['management']['director']}"
        }
    },
    "vice_principal": {
        "keywords": ["vice principal", "vice principal ka naam", "up-principal", "up-principal kaun hai"],
        "answer": {
            "en": GCS_data["management"]["vice_principal"],
            "hi": f"उप-प्रधानाचार्य: {GCS_data['management']['vice_principal']}"
        }
    },
    "system_manager": {
        "keywords": ["system manager", "system manager ka naam"],
        "answer": {
            "en": GCS_data["management"]["system_manager"],
            "hi": f"सिस्टम प्रबंधक: {GCS_data['management']['system_manager']}"
        }
    },

    # Senior Teachers
    "senior_chemistry": {
        "keywords": ["chemistry teacher", "senior chemistry teacher", "chemistry ka teacher", "rasaayan shikshak"],
        "answer": {
            "en": "Kuldeep Kumar",
            "hi": "कुलदीप कुमार"
        }
    },
    "senior_biology": {
        "keywords": ["biology teacher", "senior biology teacher", "biology ka teacher", "jeev vigyan shikshak"],
        "answer": {
            "en": "Vibha Ma’am",
            "hi": "विभा मैडम"
        }
    },
    "senior_physics": {
        "keywords": ["physics teacher", "senior physics teacher", "physics ka teacher", "bhoutik shikshak"],
        "answer": {
            "en": "Manish Mishra",
            "hi": "मनीष मिश्रा"
        }
    },
    "senior_math": {
        "keywords": ["mathematics teacher", "senior math teacher", "math ka teacher", "ganit shikshak"],
        "answer": {
            "en": "Manoj Dwivedi",
            "hi": "मनोज द्विवेदी"
        }
    },
    "senior_english": {
        "keywords": ["english teacher", "senior english teacher", "english ka teacher"],
        "answer": {
            "en": "Mohsin Khan",
            "hi": "मोहसिन खान"
        }
    },
    "senior_hindi": {
        "keywords": ["hindi teacher", "senior hindi teacher", "hindi ka teacher", "hindi shikshak"],
        "answer": {
            "en": "Kanchan Shukla",
            "hi": "कंचन शुक्ला"
        }
    },

    # Junior Teachers
    "junior_math": {
        "keywords": ["junior math teacher", "junior mathematics teacher", "junior ganit teacher", "junior maths sir"],
        "answer": {
            "en": "Harshit Agrahari and Sunil Sir",
            "hi": "हर्षित अग्रहरी और सुनील सर"
        }
    },
    "junior_pe": {
        "keywords": ["junior pe teacher", "junior physical education teacher", "pe sir", "physical education ka teacher"],
        "answer": {
            "en": "Sehbal Sir",
            "hi": "सेहबल सर"
        }
    },
    "junior_english": {
        "keywords": ["junior english teacher", "english ka teacher", "junior english sir", "english teacher junior"],
        "answer": {
            "en": "Priya Ma’am",
            "hi": "प्रिया मैडम"
        }
    },
    "junior_science": {
        "keywords": ["junior science teacher", "science ka teacher", "science sir", "junior science sir"],
        "answer": {
            "en": "Pooja Ma’am",
            "hi": "पूजा मैडम"
        }
    },
    "junior_sanskrit_art_hindi": {
        "keywords": ["sanskrit teacher", "art teacher", "junior hindi teacher", "sweta ma’am"],
        "answer": {
            "en": "Sweta Ma’am",
            "hi": "स्वेता मैडम"
        }
    },
    "junior_other": {
        "keywords": ["other junior teachers", "junior teachers", "all junior teachers", "class teachers"],
        "answer": {
            "en": "Asha Ma’am, Laxmi Ma’am and other junior-class teachers",
            "hi": "आशा मैडम, लक्ष्मी मैडम और अन्य जूनियर कक्षा के शिक्षक"
        }
    },

    # Class 11
    "class_11_boys": {
        "keywords": ["class 11 boys", "class 11 ke ladke", "11th ke boys"],
        "answer": {
            "en": ", ".join(GCS_data["class_11"]["boys"]),
            "hi": "कक्षा 11 के लड़के: " + ", ".join(GCS_data["class_11"]["boys"])
        }
    },
    "class_11_girls": {
        "keywords": ["class 11 girls", "class 11 ki ladkiyan", "11th ke girls"],
        "answer": {
            "en": ", ".join(GCS_data["class_11"]["girls"]),
            "hi": "कक्षा 11 की लड़कियाँ: " + ", ".join(GCS_data["class_11"]["girls"])
        }
    },
    "class_11_monitor": {
        "keywords": ["class 11 monitor", "class 11 ka monitor", "11th ka monitor"],
        "answer": {
            "en": GCS_data["class_11"]["monitor"],
            "hi": f"कक्षा 11 के मॉनिटर: {GCS_data['class_11']['monitor']}"
        }
    },

    # Exams
    "final_exam": {
        "keywords": ["final exam", "class 11 exam", "11th exam", "aakhri pariksha"],
        "answer": {
            "en": ", ".join(GCS_data["academics"]["final_exam"]) + f"; Start: {GCS_data['academics']['exam_start']}",
            "hi": "फाइनल परीक्षा: " + ", ".join(GCS_data["academics"]["final_exam"]) + f"; शुरू: {GCS_data['academics']['exam_start']}"
        }
    },

    # Science Exhibition
    "science_exhibition": {
        "keywords": ["science exhibition", "science mela", "vigyan pradarshani"],
        "answer": {
            "en": f"Date: {GCS_data['science_exhibition']['date']}, Head: {GCS_data['science_exhibition']['head']}, Supporting: {', '.join(GCS_data['science_exhibition']['supporting_members'])}",
            "hi": f"विज्ञान प्रदर्शनी: तिथि: {GCS_data['science_exhibition']['date']}, प्रमुख: {GCS_data['science_exhibition']['head']}, सहयोगी: {', '.join(GCS_data['science_exhibition']['supporting_members'])}"
        }
    },

    # Fees
    "class_11_fees": {
        "keywords": ["class 11 fees", "11th fees", "fees", "tuition"],
        "answer": {
            "en": f"School Fee: ₹{GCS_data['class_11']['fees']['school_fee']}/month, Coaching Fee: ₹{GCS_data['class_11']['fees']['coaching_fee']}/month",
            "hi": f"स्कूल शुल्क: ₹{GCS_data['class_11']['fees']['school_fee']}/महीना, कोचिंग शुल्क: ₹{GCS_data['class_11']['fees']['coaching_fee']}/महीना"
        }
    },

    # Infrastructure
    "infrastructure": {
        "keywords": ["infrastructure", "school facilities", "school infrastructure", "school lab", "computer lab"],
        "answer": {
            "en": ", ".join(GCS_data["infrastructure"]),
            "hi": "स्कूल की सुविधाएँ: " + ", ".join(GCS_data["infrastructure"])
        }
    },

    # Transport
    "transport": {
        "keywords": ["transport", "school bus", "van", "school vehicle", "school route"],
        "answer": {
            "en": f"Vehicles: Buses-{GCS_data['transport']['vehicles']['buses']}, Vans-{GCS_data['transport']['vehicles']['vans']}, Force Vehicle-{GCS_data['transport']['vehicles']['force_vehicle']}; Routes: {', '.join(GCS_data['transport']['routes'])}",
            "hi": f"वाहन: बस-{GCS_data['transport']['vehicles']['buses']}, वैन-{GCS_data['transport']['vehicles']['vans']}, फोर्स वाहन-{GCS_data['transport']['vehicles']['force_vehicle']}; मार्ग: {', '.join(GCS_data['transport']['routes'])}"
        }
    },

    # Admission
    "admission_documents": {
        "keywords": ["admission documents", "documents required", "school admission", "pravesh ke liye documents"],
        "answer": {
            "en": ", ".join(GCS_data["admission_documents"]),
            "hi": "आवश्यक दस्तावेज़: " + ", ".join(GCS_data["admission_documents"])
        }
    },

    # House system
    "house_system": {
        "keywords": ["house system", "school houses", "ghar", "house name"],
        "answer": {
            "en": ", ".join(GCS_data["house_system"]),
            "hi": "हाउस सिस्टम: " + ", ".join(GCS_data["house_system"])
        }
    },

    # Sports and activities
    "sports_activities": {
        "keywords": ["sports", "games", "extra curricular", "activities", "sports activities", "khel", "gatividhi"],
        "answer": {
            "en": f"Sports: {', '.join(GCS_data['sports_activities']['sports'])}; Activities: {', '.join(GCS_data['sports_activities']['extra_curricular'])}",
            "hi": f"खेल: {', '.join(GCS_data['sports_activities']['sports'])}; गतिविधियाँ: {', '.join(GCS_data['sports_activities']['extra_curricular'])}"
        }
    },

    # Best Player
    "best_player": {
        "keywords": ["best player", "best cricket player", "cricket player", "volleyball player", "behtareen khiladi"],
        "answer": {
            "en": GCS_data["best_players"]["all_time"],
            "hi": f"सर्वश्रेष्ठ खिलाड़ी: {GCS_data['best_players']['all_time']}"
        }
    },

    # School Address & Timings
    "school_address": {
        "keywords": ["school address", "school ka address", "school kaha hai"],
        "answer": {
            "en": GCS_data["address"],
            "hi": f"स्कूल का पता: {GCS_data['address']}"
        }
    },
    "school_timings": {
        "keywords": ["school timings", "school ka samay", "school timing", "school kab khulta hai"],
        "answer": {
            "en": f"General: {GCS_data['school_details']['timings']['general']}, Nursery-UKG: {GCS_data['school_details']['timings']['nursery_ukg']}, Class I-XII: {GCS_data['school_details']['timings']['class_i_xii']}",
            "hi": f"सामान्य समय: {GCS_data['school_details']['timings']['general']}, नर्सरी-UKG: {GCS_data['school_details']['timings']['nursery_ukg']}, कक्षा I-XII: {GCS_data['school_details']['timings']['class_i_xii']}"
        }
    }
}

def detect_language(query):
    # Detect Hindi via Unicode range; Hinglish via keywords
    for ch in query:
        if '\u0900' <= ch <= '\u097F':
            return "hi"
    return "en"

@app.route("/")
def home():
    return "Welcome to GCS AI Helpdesk! Ask any question about Gurukul Convent School."

@app.route("/ask", methods=["GET"])
def ask():
    query = request.args.get("query", "").lower()
    lang = detect_language(query)

    for key, value in keywords.items():
        if any(k in query for k in value["keywords"]):
            return jsonify({"query": query, "answer": value["answer"][lang]})

    # Fallback with contact numbers
    fallback_msg = {
        "en": f"Sorry, I don't have information on that. Please visit the school or contact on {', '.join(contact_numbers)}.",
        "hi": f"माफ़ कीजिए, मुझे इस विषय में जानकारी नहीं है। कृपया स्कूल जाएँ या इन नंबरों पर संपर्क करें: {', '.join(contact_numbers)}."
    }

    return jsonify({"query": query, "answer": fallback_msg[lang]})

if __name__ == "__main__":
    app.run(debug=True)

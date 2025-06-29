from jsonschema import validate, ValidationError,Draft7Validator
from pymongo import MongoClient
import requests

client = MongoClient("mongodb+srv://robin:VkplmHD1loRCTahp@cluster0.it781.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["medical_database"]
patient_collection = db["cases"]


@app.route('/insert_case', methods=['POST'])
def insert_case():
    try:
        data = request.json
        case_metadata = generate_json(data)
        error_list = validate_json(case_metadata)
        if error_list:
            return jsonify({"error: missing fields": error_list}), 500
        result = patient_collection.insert_one(case_metadata)
        return jsonify({"message": "Case inserted successfully", "id": str(result.inserted_id)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


if _name_ == '_main_':
    app.run(debug=True, host='0.0.0.0', port=5000)








#************  helper funcs ***************#

def generate_json(data):
    case_metadata = {
        "מס משימה": data.get("מס משימה", "5678"),
        "מס ניידת": data.get("מס ניידת", "1234"),
        "תאריך": data.get("תאריך", "23/10/2024"),
        "פרטי המטופל": data.get("פרטי המטופל", {}),
        "פרטי האירוע": data.get("פרטי האירוע", {}),
        "פירוט המקרה": data.get("פירוט המקרה", {}),
        "מדדים": data.get("מדדים", []),
        "טיפולים": data.get("טיפולים", []),
        "טיפול תרופתי": data.get("טיפול תרופתי", []),
        "פינוי": data.get("פינוי", {}),
    }
    return case_metadata

def validate_json(document):

    schema ={
    "type": "object",
    "required": ["מס משימה", "מס ניידת", "תאריך", "פרטי המטופל", "פרטי האירוע", "פירוט המקרה", "מדדים", "טיפולים", "טיפול תרופתי", "פינוי"],
    "properties": {
        "מס משימה": {"type": "string"},
        "מס ניידת": {"type": "string"},
        "תאריך": {"type": "string"},
        "פרטי המטופל": {
        "type": "object",
        "required": ["סוג תעודה", "גיל", "מין"],
        "properties": {
            "סוג תעודה": {"type": "string"},
            "גיל": {"type": "integer"},
            "שם האב": {"type": "string"},
            "מייל": {"type": "string"},
            "מין": {"type": "string"},
            "ת. לידה": {"type": "string"},
            "קופת חולים": {"type": "string"},
            "כתובת": {"type": "string"},
            "שם מלא": {"type": "string"},
            "טלפון": {"type": "string"},
            "ישוב": {"type": "string"}
        }
        },
        "פרטי האירוע": {
        "type": "object",
        "required": ["כתובת", "מקום האירוע", "עיר"],
        "properties": {
            "כתובת": {"type": "string"},
            "מקום האירוע": {"type": "string"},
            "עיר": {"type": "string"}
        }
        },
        "פירוט המקרה": {
        "type": "object",
        "required": ["המקרה שנמצא", "תלונה עיקרית", "אנמנזה", "סטטוס המטופל"],
        "properties": {
            "המקרה שנמצא": {"type": "string"},
            "תלונה עיקרית": {"type": "string"},
            "אנמנזה": {"type": "string"},
            "סטטוס המטופל": {"type": "string"},
            "רקע רפואי": {"type": "string"},
            "רגישויות": {"type": "string"},
            "תרופות קבועות": {"type": "string"}
        }
        },
        "מדדים": {
        "type": "array",
        "items": {
            "type": "object",
            "required": ["זמן בדיקה", "הכרה", "נשימה"],
            "properties": {
            "זמן בדיקה": { "type": "string" },
                "הכרה": { "type": "string" },
                "נשימה": { "type": "string" },
                "קצב נשימה": { "type": "string" },
                "דופק": { "type": "string" },
                "דופק לדקה": { "type": "string" },
                "מצב העור": { "type": "string" },
                "סרגל כאב": { "type": "string" },
                "האזנה": { "type": "string" },
                "ריאה ימין": { "type": "string" },
                "ריאה שמאל": { "type": "string" },
                "ETCO2": { "type": "string" },
                "קצב לב": { "type": "string" },
                "אישונים": { "type": "string" },
                "ציון גלזגו": { "type": "string" }       
                }
            }
        }
        },
        "טיפולים": {
        "type": "array",
        "items": {
            "type": "object",
            "required": ["זמן", "טיפול שניתן"],
            "properties": {
            "זמן": {"type": "string"},
            "טיפול שניתן": {"type": "array", "items": {"type": "string"}}
            }
        }
        },
        "טיפול תרופתי": {
        "type": "array",
        "items": {
            "type": "object",
            "required": ["זמן", "תרופה"],
            "properties": {
            "זמן": {"type": "string"},
            "תרופה": {"type": "array", "items": {"type": "string"}}
            }
        }
        },
        "פינוי": {
        "type": "object",
        "required": ["אופן הפינוי", "יעד הפינוי", "שם בית החולים"],
        "properties": {
            "אופן הפינוי": {"type": "string"},
            "יעד הפינוי": {"type": "string"},
            "שם בית החולים": {"type": "string"},
            "מחלקה": {"type": "string"},
            "שם המקבל ביעד הפינוי": {"type": "string"}
        }
        }
    }
    
    try:
        validate(instance=document, schema=schema)
        print("Document is valid. Proceeding to insert.")
        # Insert into MongoDB here
    except ValidationError as e:
        validator = Draft7Validator(schema)
        errors = list(validator.iter_errors(document))
        error_list=[]
        for error in errors:
            if error.validator == "required":
                for field in error.schema["required"]:
                    if field not in error.instance:
                        error_list.append(field[::-1])
        if error_list:
            return ( error_list)

    return ([])
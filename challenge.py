import json
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

#sample clinical trials data
clinical_trials = [
    {
        "nctId": "NCT001",
        "title": "Trial for Diabetes and Hypertension",
        "inclusion_criteria": "Inclusion: Patients with both diabetes and hypertension. Age between 40 and 60 years.",
        "exclusion_criteria": "Exclusion: Patients with a history of cardiovascular disease or on insulin therapy."
    },
    {
        "nctId": "NCT002",
        "title": "Diabetes Treatment Study for Elderly Patients",
        "inclusion_criteria": "Inclusion: Patients diagnosed with diabetes. Age 65 and above.",
        "exclusion_criteria": "Exclusion: Patients with uncontrolled hypertension or severe kidney disease."
    },
    {
        "nctId": "NCT003",
        "title": "Heart Disease Study for Middle-Aged Patients",
        "inclusion_criteria": "Inclusion: Patients with a confirmed diagnosis of heart disease. Age between 45 and 55 years.",
        "exclusion_criteria": "Exclusion: Patients on blood thinners, or with diabetes."
    },
    {
        "nctId": "NCT004",
        "title": "Cancer Immunotherapy Study",
        "inclusion_criteria": "Inclusion: Patients with any type of solid tumor cancer. Age between 18 and 70 years.",
        "exclusion_criteria": "Exclusion: Patients who have previously undergone chemotherapy or have autoimmune disorders."
    },
    {
        "nctId": "NCT005",
        "title": "Osteoporosis Study for Post-Menopausal Women",
        "inclusion_criteria": "Inclusion: Post-menopausal women diagnosed with osteoporosis. Age 50 and above.",
        "exclusion_criteria": "Exclusion: Patients on hormone replacement therapy or with a history of breast cancer."
    },
    {
        "nctId": "NCT006",
        "title": "COVID-19 Vaccine Trial for Adults",
        "inclusion_criteria": "Inclusion: Adults aged 18 and above, with no history of COVID-19 vaccination.",
        "exclusion_criteria": "Exclusion: Patients with any pre-existing respiratory condition or those on immunosuppressive therapy."
    },
    {
        "nctId": "NCT007",
        "title": "Asthma Study for Children",
        "inclusion_criteria": "Inclusion: Children diagnosed with moderate to severe asthma. Age between 6 and 17 years.",
        "exclusion_criteria": "Exclusion: Children with any other chronic respiratory conditions or on long-term steroid treatment."
    },
    {
        "nctId": "NCT008",
        "title": "Mental Health Study for Adolescents",
        "inclusion_criteria": "Inclusion: Adolescents diagnosed with depression or anxiety. Age between 13 and 18 years.",
        "exclusion_criteria": "Exclusion: Adolescents with a history of self-harm or currently on antidepressant medications."
    }
]

#sample patients data
patients_data = [
    {
        "id": "patient1",
        "age": 45,
        "gender": "Male",
        "conditions": ["diabetes", "hypertension"],
        "medications": ["Metformin"] 
    },
    {
        "id": "patient2",
        "age": 70,
        "gender": "Female",
        "conditions": ["diabetes"],
        "medications": []  
    },
    {
        "id": "patient3",
        "age": 50,
        "gender": "Male",
        "conditions": ["heart disease", "diabetes"],
        "medications": [] 
    },
    {
        "id": "patient4",
        "age": 55,
        "gender": "Female",
        "conditions": ["osteoporosis"],
        "medications": ["hormone replacement therapy"] 
    },
    {
        "id": "patient5",
        "age": 30,
        "gender": "Male",
        "conditions": ["cancer"],
        "medications": [] 
    },
    {
        "id": "patient6",
        "age": 40,
        "gender": "Female",
        "conditions": ["covid-19"],
        "medications": [] 
    },
    {
        "id": "patient7",
        "age": 12,
        "gender": "Male",
        "conditions": ["asthma"],
        "medications": [] 
    },
    {
        "id": "patient8",
        "age": 15,
        "gender": "Female",
        "conditions": ["depression"],
        "medications": []  
    },
    {
        "id": "patient9",
        "age": 67,
        "gender": "Male",
        "conditions": ["diabetes", "kidney disease"],
        "medications": []  
    },
    {
        "id": "patient10",
        "age": 35,
        "gender": "Female",
        "conditions": ["hypertension"],
        "medications": [] 
    }
]


#parses the age
def parse_age_range(inclusion_criteria):
    min_age, max_age = 0, 120 
    
    if "age between" in inclusion_criteria.lower():
        age_part = inclusion_criteria.lower().split("age between")[1].split("years")[0].strip()
        min_age, max_age = map(int, age_part.split("and"))
    elif "age above" in inclusion_criteria.lower():
        min_age = int(inclusion_criteria.lower().split("age above")[1].split("years")[0].strip())
    elif "age below" in inclusion_criteria.lower():
        max_age = int(inclusion_criteria.lower().split("age below")[1].split("years")[0].strip())
    
    return min_age, max_age

#function that goes through the various inclusion and exclusion criteria to check if the patient is eligible
def is_patient_eligible(patient_data, trial):
    inclusion_criteria = trial['inclusion_criteria'].lower()
    exclusion_criteria = trial['exclusion_criteria'].lower()

    min_age, max_age = parse_age_range(inclusion_criteria)
    if not (min_age <= patient_data['age'] <= max_age):
        return False
    
    conditions_inclusion = [cond.lower() for cond in patient_data['conditions']]
    if not any(cond in inclusion_criteria for cond in conditions_inclusion):
        return False
    
    if any(cond in exclusion_criteria for cond in conditions_inclusion):
        return False
    if any(med.lower() in exclusion_criteria for med in patient_data['medications']):
        return False
    
    return True

#matching patients algorithm that first checks if patient is eligible, and if so appends the trial information for that patient
def match_patients_to_trials(patients_data, clinical_trials):
    eligible_patients = []

    for patient in patients_data:
        patient_id = patient['id']
        patient_eligible_trials = []
        
        for trial in clinical_trials:
            if is_patient_eligible(patient, trial):
                patient_eligible_trials.append({
                    "trialId": trial['nctId'],
                    "trialName": trial['title'],
                    "eligibilityCriteriaMet": "Matched inclusion and exclusion criteria"
                })
        
        eligible_patients.append({
            "patientId": patient_id,
            "eligibleTrials": patient_eligible_trials
        })

    return eligible_patients


def export_to_json(output_data, filename="eligible_patients.json"):
    with open(filename, 'w') as outfile:
        json.dump(output_data, outfile, indent=4)


#sets up the google sheets API and sharing with the email
def google_sheets_setup(email):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file("/Users/mihikarao/Downloads/Tumerik_Challenge/creds1.json", scopes=scope) #path to the credentials file, replace with your specific path
    client = gspread.authorize(creds)
    
    sheet = client.create("Matched Patients Clinical Trials")
    
    sheet.share(email, perm_type='user', role='writer')
    
    return sheet

def export_to_google_sheet(matched_patients,email):
    sheet = google_sheets_setup(email)
    worksheet = sheet.get_worksheet(0)
    worksheet.update('A1', [[ "Hello, World!" ]])

    rows = []
    for patient in matched_patients:
        patient_id = patient['patientId']
        for trial in patient['eligibleTrials']:
            rows.append({
                "Patient ID": patient_id,
                "Trial ID": trial['trialId'],
                "Trial Name": trial['trialName'],
                "Eligibility Criteria Met": trial['eligibilityCriteriaMet']
            })
    
    df = pd.DataFrame(rows)
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

email = "mihikasrao@gmail.com" #change this to the email that will have the google sheets
matched_patients = match_patients_to_trials(patients_data, clinical_trials)
export_to_json(matched_patients)
export_to_google_sheet(matched_patients,email)

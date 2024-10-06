# Matched Patients Clinical Trials

## Project Goal

The goal of this project is to match a set of patients to clinical trails based on medical conditions, age, and medications, following the inclusion and exclusion criteria defined by each clinical trial. After matching the patients to relevant clinical trials, the results are saved as a JSON file and expored to a Google Sheet for easy access. 

## Requirements

To run this project you need to have the following dependencies installed. The required Python libraries are listed in requirements.txt. 

Required Libraries: 
gspread: For interacting with Google Sheets API 

google-auth: For authenticating with Google services using a service account. 

pandas: For working wtih DataFrames to structure and export data to Google Sheets

json: For exporting and manipulating JSON data

## Setup

1. **Enable the Google Sheets API**: 
    - Go to the [Google Cloud Console](https://console.cloud.google.com/).
    - Navigate to **API & Services > Credentials**. 
    - Enable the **Google Sheets API**. 

2. **Create a Service Account**: 
    - Go to **IAM & Admin > Service Accounts**. 
    - Create a new service account and download the **JSON key file** ('creds.json'). 
    - Place the 'creds.json' file in the project directory. 

3. **Grant Access to the Google Sheets**: 
    - After the service account is created, get the service account email
    - Share the sheets with this email, giving it edit access.

## Patient & Clinical Trial Data
The project uses a predfined list of patients and clinical trials. Patients have attributes such as age, conditions, and medications, while trials have inclusion_criteria and exclusion_criteria. Based on these criteria, patients are matched to eligible trials. 


## Execution
Run: python challenge.py 

After the matching process is complete, the export_to_json() function saves the matched data as a JSON file (eligible_patients.json) in the project directory. 

The functione export_to_google_sheet() creates a new sheet and writes the matched data into the worksheet. 

# Note
Would have liked to scrape the clinicaltrials.gov website to get the actual relevant clinical trials data. I used mock data in this project to simulate the actual clinical trials data, but if I was able to use the clinicaltrials.gov API, I would have done the algorithm in a similar way. Additionally, would have wanted to use the provided dataset for the project, but was unable to do so due to merging process taking a lot of memory. The plan was to merge the data within the dataset based on patient ID, and some datasets didn't have a patient ID or were named something different, so I would merge based on the patient identifying factor. From there, I would complete the algorithm similarly by isolating the age, gender, etc. and run it through my matching algorithm. In the future, I would also take into account geographic location, severity of case, and other factors when deciding how to match patients up to clinical trials. 

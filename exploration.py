# %%
import sys
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

print(sys.version_info)
# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %%
slr_fields = [
	#"You have also been informed by the client that the following baseline characteristics need to be extracted:",
	"Number of patients recruited by trial per treatment arm",
	"Patient gender: Male (number, proportion), Female (number, proportion)",
	"Age (mean or median, measure of data spread e.g., standard deviation)",
	"Body mass index (mean or median, measure of data spread e.g., range)",
	"Patient race (number/proportion): White; Native American or Alaska Native; Asian; Black or African American; Native Hawaiian or Other Pacific Islander",
	"Disease duration (mean or median, measure of spread, units)",
	"Location and extent of disease (number/proportion):Left side; Extensive or pancolitis; Limited to rectum",
	"Number of acute UC episodes in the past year (mean or median, measure of spread)",
	"Adapted Mayo score (mean or median, measure of spread)",
	"Adapted Mayo score category (number, proportion): ≤ 7, > 7",
	"Previous medication use (number, proportion): Immunosuppressants; Aminosalicylates; Corticosteroids.",
	#"And that the following clinical outcomes need to be extracted:",
	"Proportion of patients1 with a clinical response at all reported timepoints between 8 and 26 weeks",
	"Proportion of patients with a clinical and endoscopic response at all reported timepoints between 8 and 26 weeks",
	"Proportion of patients2 with any adverse event (AE)",
	"Proportion of patients with any treatment-emergent adverse event (TEAE)."
]

print(slr_fields)
# %%


import os
import pdfplumber

# Read pdf files in the docs folder
docs_folder = "docs"
pdf_files = [f for f in os.listdir(docs_folder) if f.endswith('.pdf')]
print(f"Found {len(pdf_files)} PDF files in {docs_folder} folder")

# Example of reading a PDF file
# Uncomment and modify as needed for your specific use case

pdf_dict = {}

for pdf_file in pdf_files:
    with pdfplumber.open(docs_folder + "/" + pdf_file) as pdf:
        full_text = ""
        for page in pdf.pages:
            words = page.extract_words()
            line = ""
            last_top = None
            for word in words:
                # Start a new line if y-position changes significantly
                if last_top is not None and abs(word['top'] - last_top) > 3:
                    full_text += line.strip() + "\n"
                    line = ""
                line += word['text'] + " "
                last_top = word['top']
            full_text += line.strip() + "\n"  # flush last line of the page
        pdf_dict[pdf_file] = full_text


# %%
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

# Initialize the text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    # separators=["\n\n", "\n", " ", ""]
)

# Chunk the texts in pdf_dict
documents = []
for filename, text in pdf_dict.items():
	chunks = text_splitter.split_text(text)

	for j, chunk in enumerate(chunks):
	    documents.append(
	        Document(
	            page_content=chunk,
	            metadata={"filename": filename, "chunk_id": j}
	        )
	    )



# %%
from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings

# Initialize embeddings
embeddings = OllamaEmbeddings(
    model="oscardp96/medcpt-article",
    base_url="http://192.168.1.215:11434"
)

# %%

import shutil
import os

persist_dir = "./chroma_db6"

# Use Chroma.from_documents instead of from_texts
vectorstore = Chroma.from_documents(
    documents,
    embedding=embeddings,
    persist_directory=persist_dir
)

print("Embeddings for multiple documents created and stored in Chroma.")

# %%
# query_text = chunked_texts['UC_Louis_2024.pdf'][0]
#
print(slr_fields[0])
embedding_vector = embeddings.embed_query(slr_fields[0])

results = vectorstore.similarity_search_by_vector(embedding_vector)
# print(results)
# %%

results = vectorstore.similarity_search(
    slr_fields[0],
    k=10,
    filter={"filename": "UC_Louis_2024.pdf"}
)

for r in results:
    print(r.page_content[:100])
    # Enrollment for the maintenance trial was conducted at 238clinicalcentersin37countriesfromAugust28,2018,toMarch
    # 30,2022,withthefinalfollow-uponApril11,2023( Figure2 ).
    # Inclusion and Exclusion Criteria
    # Patients eligible for the induction trial (1) were 18 years to 80
    # aPharmaceuticals,Lilly,MSD,Novartis,Pfizer,Roche,SamsungBioepsis,StelicInstitute,Research
    # a,andTillotts.DrHisamatsureportedreceivingresearchgrantsfromAbbVie,AlfresaPharma,BostonScientific,
    # 7Withdrew consent
    # 2Experienced an adverse event
    # 1Lost to follow-up
    # 1Logistical problem (geopolitical restrictions)
    # 2Other reasons
    # 165 Completed 52 wk of therapy193 Randomized to receive 180 mg of risankizumab
    # administered subcutaneously
    # 179 Received intervention as randomized
    # 14Had a clinical response before 24 wk
    # with risankizumab administeredintraveneouslyc
    # 179 Included in primary efficacy analysis12Discontinued treatment after the first dose
    # 5Lack of efficacy
    # 3Withdrew consent
    # 3Experienced an adverse event
    # 0Lost to follow-up
    # 0Logistical problem (geopolitical restrictions)
    # 1Other reason
    # 167 Completed 52 wk of therapy196 Randomized to receive placebo administered
    # subcutaneously
    # 183 Received intervention as randomized
    # 13Had a clinical response before 24 wk
    # with risankizumab administeredintraveneouslyc
    # 183 Included in primary efficacy analysis18Discontinued treatment after the first dose
    # 5Lack of efficacy
    # 5Withdrew consent
    # 1Experienced an adverse event
    # 1Lost to follow-up
    # (alltreatmentsadministeredsubcutaneously),548hadanad-equate clinical response to risankizumab at 12 weeks duringtheinductiontria
    # landthesepatientswereincludedinthepri-maryefficacypopulation(179inthe180mgofrisankizumabgroup, 186 in the 360 mg of risankizumab
    #  group, and 183in the placebo group [no longer receiving risankizumab])(Figure 2). Among these 548 patients (aged 40.9 [SD, 14.0
    # ]years;313[57.1%]weremale;and407[74.3%]wereWhite)withanadequateclinicalresponsetorisankizumab,167/179(93%)in the 180 mg of risan
    # kizumab group, 165/186 (89%) in the360mgofrisankizumabgroup,and165/183(90%)inthepla-cebogroup(nolongerreceivingrisankizumab)comp
    # leted52-weekfollow-up.
    # Of those included in the primary efficacy population,
    # 503/975 patients (52%) in the induction trial and 411/548patients (75%) in the maintenance trial had a history ofintolerance or
    # inadequate response to advanced therapies(Table 1 ). At week 0 in the maintenance trial, 44/179
    # Randomization was stratified by history of inadequate re-sponse to advanced therapy (yes, no), last risankizumab in-ductiondose(
    # 600mg,1200mg,1800mgadministeredintra-venously),andclinicalremissionstatus(perlocalevaluation)at the last visit of the induction
    # trial (yes, no). Although pa-tientswithanadequateclinicalresponsetotreatmentwithri-sankizumabateitherweeks12or24wereincludedinth
    # esafetyoutcomes analysis, only randomized patients who (1) re-ceived at least 1 dose of the study drug and (2) had an ad-equatec
    # linicalresponsetorisankizumabadministeredintra-venously after 12 weeks of treatment were included in theprimaryefficacyanalysisf
    # orthemaintenancetrial.
    # Randomizationwasperformedusingweb-basedinterac-
    # tiveresponsetechnology(EndpointClinical,version3.0)withblockrandomizationmethods.Theblockrandomizationsched-
    # resultsforthecategoricaloutcomesarebasedonnonresponderimputationwhileincorporatingmultipleimputationtohandlemissingdataduetologi
    # sticalrestrictionsbecauseoftheCOVID-19pandemicorgeopoliticalrestrictions.Theresultsforthecontinuousoutcomesarebasedonreturntobas
    # elinemultipleimputation.
    # bCalculatedusingtheMantel-Haenszelcommonratedifferencewithnonresponderimputationwhileincorporatingmultipleimputationtohandlemiss
    # ingdataduetologisticalrestrictionsbecauseoftheCOVID-19pandemicorgeopoliticalrestrictionsforthecategoricaloutcomesandusinganalysi
    # sofcovarianceormixed-effectmodelandarepeated-measuresmethodwithreturntobaselinemultipleimputationforthecontinuousoutcomes.
    # cAllcomparisonswerestatisticallysignificantaccordingtohierarchicaltesting.
    # 4Withdrew consent
    # 2Experienced an adverse event
    # 1Lack of efficacy
    # 1Had COVID-19 infection
    # 4Other reasons1Logistical restrictions because
    # of COVID-19 pandemic
    # 650 Included in primary efficacy analysisc637 Completed therapy to 12 wk325 Randomized to receive placebo
    # administered intravenously
    # 325 Received intervention as randomized
    # 27Discontinued treatment after the first dose
    # 6Withdrew consent
    # 12Experienced an adverse event
    # 5Lack of efficacy
    # 0Had COVID-19 infection
    # 4Other reasons0Logistical restrictions because
    # of COVID-19 pandemic
    # 325 Included in primary efficacy analysisc298 Completed therapy to 12 wkaDeterminationofeligibilitywas
    # madeattheclinicalsitesatthetimeofenrollment.Thespecificreasonsfornotmeetingscreeningcriteriawerenotcollected.
    # bThe2:1randomizationwasstratified
    # bythenumberofpriorbiologicaldrugs(0or1vs>1)eachpatientreceivedthatproducedaninadequateresponse,currentuseofsteroids(yesvsno),and
    # adaptedMayoscore( /H113497vs>7).
    # cThepatientsincludedintheprimary
    # Original Investigation RisankizumabforUlcerativeColitis
    # At 12-week follow-up in the induction trial and at 52-
    # week follow-up in the maintenance trial, the prespecifiedsecondary outcomes were (1) clinical response, which wasdetermined usin
    # g the adapted Mayo score (a decrease of≥30% and ≥2 points from baseline and a decrease in rectalbleeding score of ≥1 or an absol
    # ute rectal bleeding score of≤1),(2)clinicalresponsedeterminedusingthepartialadaptedMayo score (in the induction trial only at we
    # ek 4; decrease of



# %%



print(pdf_dict.items())
# %%
#
from ollama import Client

client = Client(
  host='http://192.168.1.215:11434',
  headers={'x-some-header': 'some-value'}
)



# -----------------------------
# Example retrieved passages from vector DB
# -----------------------------
retrieved_passages = [
    "Study X enrolled 248 patients. Mean age 56.4 years, 52% male...",
    "BMI average 29.8 kg/m^2. Disease duration 10 years..."
]

# -----------------------------
# Schema & domain augmentation
# -----------------------------
schema_info = """
Return JSON only with keys: study_id, sample_size, mean_age, percent_male, bmi, disease_duration_years
"""

domain_augmentation = "Typical age range 30-75, BMI 20-40, percent male 0-100"

context = "\n\n".join([schema_info, domain_augmentation] + retrieved_passages)

# -----------------------------
# Query Ollama
# -----------------------------
# ollama_client = client.generate(model='meditron', prompt='Why is the sky blue?') ##(model="meditron")  # or your local model #medllama2
query = f"Extract baseline characteristics from the following text:\n{context}"

response = client.generate(model='meditron:latest', prompt=query) #ollama_client.generate(query)

# %%


response["response"]

# %%

import ollama

# Point to remote Ollama server
client = ollama.Client(host="http://192.168.1.215:11434")

response = client.chat(
    model="gpt-oss",
    messages=[{"role": "user", "content": query}]
)

# print(response['message']['content'])

# context
# %%
#
response.message.content


# %%
# from langchain.embeddings import OpenAIEmbeddings  # for vector DB
# from langchain.vectorstores import FAISS
# from pydantic import BaseModel, Field, confloat, conint
# from typing import Optional

# -----------------------------
# Pydantic schema
# -----------------------------
# class BaselineCharacteristics(BaseModel):
#     study_id: str
#     sample_size: conint(gt=0)
#     mean_age: Optional[confloat(gt=0, lt=120)]
#     percent_male: Optional[confloat(ge=0, le=100)]
#     bmi: Optional[confloat(gt=0, lt=100)]
#     disease_duration_years: Optional[confloat(gt=0)]

# -----------------------------
# Validate with Pydantic
# -----------------------------
# baseline = BaselineCharacteristics.parse_raw(response.text)
# print(baseline.json(indent=2))
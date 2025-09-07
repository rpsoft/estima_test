# %%
# %load_ext autoreload
# %autoreload 1

# %aimport retrieve

# %%
import processData

processData.document_files.sort()
# %%
import retrieve


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

extracted_data = {}
for filename in processData.document_files:

	# filename = "UC_Louis_2024_suppl.txt"

	rags = []
	for field in slr_fields:
		print(f"{filename} -- {field}")
		res = retrieve.perform_rag(field, filename, processData.vectorstore, k=5)
		rags.append({"field":field,"result":res["response"].message.content, "context":res["context"]})


	extracted_data[filename] = rags

	# break


# %%
#

import json


with open('extracted_data.json', 'w') as f:
    json.dump(extracted_data, f)

# %%
import formatOutput


# %%

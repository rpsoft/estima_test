
import ollama
import os
from dotenv import load_dotenv

# Load variables from .env into environment
load_dotenv()

# Load variables from .env into environment

def perform_rag(slr_field, filename, vectorstore, k=1):
	results = vectorstore.similarity_search(
			    slr_field,
			    k=k,
			    filter={"filename": filename}
			)


	contents = [doc.page_content for doc in results]

	context = "\n\n".join(contents)

	formatInstructions = """
		Extract the relevant information from the text and format it as a JSON object.

		Rules:
		1. Use nested objects for related data. Example:
		   { "participants": { "placebo": 200, "treatment": 600 } }
		2. Respond ONLY with a JSON object. No explanations, no markdown, no ```json fences.
		3. If nothing is found, return {}.
		4. Always include an "explain" field describing what was extracted. Or why nothing was found.
		5. Ensure the JSON is valid (double quotes, commas, colons).
		6. JSON must start with { and end with }.
		7. All numeric values must be numbers, not strings.

		Example output to follow exactly:

		{
		  "participants": {
		    "high_dose": 27,
		    "low_dose": 26,
		    "placebo": 53
		  },
		  "explain": "The participant counts per arm were inferred from the disposition table row 'Did not complete the study/phase' in the provided excerpt. The table lists the number of patients who did not complete the study for each group along with percentages: 8 (29.6%), 4 (15.4%), 12 (22.6%). Solving 8/0.296 ≈ 27, 4/0.154 ≈ 26, and 12/0.226 ≈ 53 gives the size of each arm. These correspond to the high-dose, low-dose, and placebo arms, respectively, totaling 106 randomized participants."
		}
	"""

	# print(formatInstructions)

	query = f"Extract {slr_field} \n from the text:\n{context} following these instructions \n {formatInstructions} . "

	client = ollama.Client(host=os.getenv("OLLAMA_URL", "localhost:11434"))

	response = client.chat(
	    model= os.getenv("GEN_MODEL", "gpt-oss" ),
	    messages=[{"role": "user", "content": query}]
	)

	return({"response": response, "context": context})


## class BaselineCharacteristics(BaseModel):
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

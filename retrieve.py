
import ollama

# Load variables from .env into environment

def perform_rag(slr_field, filename, vectorstore):
	results = vectorstore.similarity_search(
			    slr_field,
			    k=10,
			    filter={"filename": filename}
			)


	contents = [doc.page_content for doc in results]

	context = "\n\n".join(contents)

	formatInstructions = """Extract the relevant information from the text and format it as a clean JSON object with the following rules:

							1. Structure related data using nested objects. Example:
							   { "participants": { "placebo": 200, "treatment": 600 } }

							2. Always respond **only** with a JSON object. Do not include any extra text, explanation, or markdown.

							3. Include an "explain" field in the JSON object if you need to provide context or reasoning for the extracted values.

							4. Ensure the JSON is valid and can be parsed by Python (use proper quotes, colons, commas, etc.).

							5. If a piece of data is missing or not found, omit the field or use an empty object for that section. If no relevant data exists at all, respond with an empty JSON object: {}

							6. The JSON output must **start with {** and **end with }**. Do not include ```json or any other formatting characters.

							7. All numeric values should be numbers, not strings, unless explicitly textual.

							"""

	# print(formatInstructions)

	query = f"Extract {slr_field} from the following text:\n{context}. \n {formatInstructions}"

	client = ollama.Client(host="http://192.168.1.215:11434")

	response = client.chat(
	    model="gpt-oss",
	    messages=[{"role": "user", "content": query}]
	)

	return(response)


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

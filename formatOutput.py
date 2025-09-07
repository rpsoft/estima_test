# %%
import pandas as pd
import json

with open("extracted_data.json", "r") as f:
    extracted_data = json.load(f)

# Flatten the extracted_data dictionary so each filename is a single row
def flatten_dict(d, parent_key='', sep='.'):
	items = []
	if isinstance(d, dict):
		for k, v in d.items():
			new_key = f"{parent_key}{sep}{k}" if parent_key else k
			if isinstance(v, dict):
				items.extend(flatten_dict(v, new_key, sep=sep).items())
			elif isinstance(v, list):
				for idx, item in enumerate(v):
					if isinstance(item, dict):
						items.extend(flatten_dict(item, f"{new_key}[{idx}]", sep=sep).items())
					else:
						items.append((f"{new_key}[{idx}]", item))
			else:
				items.append((new_key, v))
	else:
		items.append((parent_key, d))
	return dict(items)

records = []
for filename, fields in extracted_data.items():
	row = {"filename": filename}
	for entry in fields:
		try:
			result_data = json.loads(entry["result"])
			flat_result = flatten_dict(result_data)
		except Exception:
			flat_result = {"result_raw": entry["result"]}
		# Use the field name as the key for this result
		field_key = entry["field"]
		# If flat_result has multiple keys, nest under field_key
		if len(flat_result) == 1 and "result_raw" in flat_result:
			row[field_key] = flat_result["result_raw"]
		else:
			for k, v in flat_result.items():
				row[f"{field_key}.{k}"] = v
	records.append(row)

df = pd.DataFrame(records)
df

records = []
for filename, fields in extracted_data.items():
	for entry in fields:
		try:
			result_data = json.loads(entry["result"])
			flat_result = flatten_dict(result_data)
		except Exception:
			flat_result = {"result_raw": entry["result"]}
		record = {
			"filename": filename,
			"field": entry["field"],
			# "context": entry["context"],
		}
		record.update(flat_result)
		records.append(record)

df = pd.DataFrame(records)

df.drop(columns=["explain"], errors='ignore', inplace=True)

df.to_csv("extracted_data.csv", index=True)

# %% Class definition
class LLMComparator:
    from llm_comparator import types
    def __init__(self):
        pass

    def create_comparison_json(self, file_1: str, file_2: str, query_key: str = "prompt", response_key: str = "answer") -> types.JsonDict:
        """Create a JSON object for the LLM Comparator from two files (JSONL or CSV)."""

        import json
        import csv
        import os

        def load_jsonl(file_path):
            with open(file_path, 'r') as f:
                return [json.loads(line) for line in f]

        def load_csv(file_path):
            with open(file_path, 'r') as f:
                reader = csv.DictReader(f)
                return [row for row in reader]

        def load_file(file_path):
            if file_path.endswith('.jsonl'):
                return load_jsonl(file_path)
            elif file_path.endswith('.csv'):
                return load_csv(file_path)
            else:
                raise ValueError("Unsupported file format. Please provide a .jsonl or .csv file.")

        data1 = load_file(file_1)
        data2 = load_file(file_2)

        # Assuming per_example_generator, clusters are defined elsewhere
        per_example_generator = []
        for input_1, input_2 in zip(data1, data2):
            per_example_generator.append((input_1, input_2))

        # File name without folder and extension is model name
        model1_name = os.path.basename(file_1).rsplit('.', 1)[0]
        model2_name = os.path.basename(file_2).rsplit('.', 1)[0]

        # Create the JSON object
        return {
            'metadata': {'custom_fields_schema': []},
            'models': [{'name': model1_name}, {'name': model2_name}],
            'examples': [
                {
                    'input_text': input_1[query_key],
                    'tags': [],
                    'output_text_a': input_1[response_key],
                    'output_text_b': input_2[response_key],
                    "score": 0.0,
                    "individual_rater_scores": [],
                }
                for input_1, input_2 in per_example_generator
            ]
        }

    def write(self, comparison_result: types.JsonDict, file_path: str) -> str:
        """Write the comparison JSON object to a file."""
        import json
        with open(file_path, 'w') as f:
            json.dump(comparison_result, f)
        return file_path

    def show_in_llm_comparator(self, comparison_json_path:str):
        """
        Open the LLM Comparator in a web browser with the comparison JSON file.
        """
        if comparison_json_path.startswith('http'):
            import webbrowser
            url = f"https://pair-code.github.io/llm-comparator/?results_path={comparison_json_path}"
            webbrowser.open(url)
        else:
            raise ValueError("Please provide a valid http url")

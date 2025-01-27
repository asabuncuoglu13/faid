from faid.logging import (
    get_model_log_file_path,
    get_risk_register_log_path,
    get_model_entry,
    add_model_entry,
    add_data_entry,
    get_data_entry,
    get_risk_entry,
    add_risk_entry,
)

class EntityLookup:
    def __init__(self):
        self.lookup_table = self.load_data()

    def load_data(self):
        return [
            {"is_array": "1", "model": "data", "model_p": "model_parameters", "data": "", "data_p": "", "risk": "", "risk_p": "", "usecase": "", "usecase_p": "", "transparency": "", "transparency_p": ""},
            {"is_array": "0", "model": "description", "model_p": "data", "data": "summary", "data_p": "", "risk": "", "risk_p": "", "usecase": "", "usecase_p": "", "transparency": "", "transparency_p": ""},
            {"is_array": "0", "model": "link", "model_p": "data", "data": "dataset_link", "data_p": "", "risk": "", "risk_p": "", "usecase": "", "usecase_p": "", "transparency": "", "transparency_p": ""},
            {"is_array": "0", "model": "sensitive", "model_p": "data", "data": "sensitivity_types", "data_p": "", "risk": "", "risk_p": "", "usecase": "", "usecase_p": "", "transparency": "", "transparency_p": ""},
            {"is_array": "0", "model": "sensitive", "model_p": "data", "data": "sensitivity_types", "data_p": "", "risk": "", "risk_p": "", "usecase": "", "usecase_p": "", "transparency": "", "transparency_p": ""},
            {"is_array": "1", "model": "risks", "model_p": "considerations", "data": "risks", "data_p": "", "risk": "risks", "risk_p": "", "usecase": "", "usecase_p": "", "transparency": "", "transparency_p": ""},
            {"is_array": "0", "model": "name", "model_p": "risks", "data": "name", "data_p": "risks", "risk": "description", "risk_p": "risks", "usecase": "", "usecase_p": "", "transparency": "", "transparency_p": ""},
            {"is_array": "0", "model": "mitigation_strategy", "model_p": "risks", "data": "mitigation_strategy", "data_p": "risks", "risk": "mitigation", "risk_p": "risks", "usecase": "", "usecase_p": "", "transparency": "", "transparency_p": ""}
        ]

    def find_entity(self, key, value):
        results = []
        for row in self.lookup_table:
            if row.get(key) == value:
                results.append(row)
        return results

model_file_path = get_model_log_file_path()
risk_file_path = get_risk_register_log_path()

def sync_model_to_risk():
    model_risks = get_model_entry("considerations").get('risks', [])
    
    # Sync the related entities
    for i, risk in enumerate(model_risks):
       add_risk_entry({
            'description': risk.get('name', ''),
            'impact': '',  # Add logic to determine impact if needed
            'likelihood': '',  # Add logic to determine likelihood if needed
            'mitigation': risk.get('mitigation_strategy', '')
        }, key='risks')

def sync_model_to_data():
    model_data = get_model_entry("data")
    add_data_entry({
        "summary": model_data.get('description', ''),
        "dataset_link": model_data.get('link', ''),
        "sensitivity_types": model_data.get('sensitive', ''),
    })

def sync_model_to_usecase():
    # Implement the logic to sync model to usecase
    pass

def sync_data_to_model():
    data_entry = {
        "description" : get_data_entry("summary"),
        "link" : get_data_entry("dataset_link"),
        "sensitive" : get_data_entry("sensitivity_types"),
        "graphics" : "",
    }
    add_model_entry(data_entry, key='data', filename=model_file_path)

def sync_data_to_risk():
    data_entry = get_data_entry(key='risks')

    for entry in data_entry:
        dr = {
            'description': entry.get('name', ''),
            'impact': '',  # Add logic to determine impact if needed
            'likelihood': '',  # Add logic to determine likelihood if needed
            'mitigation': entry.get('mitigation_strategy', '')
        }
        add_risk_entry(dr, key='risks')

def sync_data_to_transparency():
    # Implement the logic to sync data to transparency
    pass

def sync_risk_to_model():
    risk_entry = get_risk_entry(key='risks')
    model_risks = risk_entry.get('risks', [])
    
    # Sync the related entities
    for i, risk in enumerate(model_risks):
        add_model_entry({
            'name': risk.get('description', ''),
            'mitigation_strategy': risk.get('mitigation', '')
        }, key='considerations', filename=model_file_path)

def sync_risk_to_data():
    risk_entry = get_risk_entry(key='risks')
    data_risks = risk_entry.get('risks', [])

    for i, risk in enumerate(data_risks):
        add_data_entry({
            'name': risk.get('description', ''),
            'mitigation_strategy': risk.get('mitigation', '')
        }, key='risks')

def sync_risk_to_transparency():
    # Implement the logic to sync risk to transparency
    pass

def sync_model_to_transparency():
    # Implement the logic to sync model to transparency
    pass

def sync_usecase_to_model():
    # Implement the logic to sync usecase to model
    pass

def sync_usecase_to_data():
    # Implement the logic to sync usecase to data
    pass

def sync_usecase_to_transparency():
    # Implement the logic to sync usecase to transparency
    pass


"""
if __name__ == "__main__":
    entity_lookup = EntityLookup()

    # Example usage
    key = 'model'
    value = 'data'
    results = entity_lookup.find_entity(key, value)
    
    for result in results:
        print(result)

"""
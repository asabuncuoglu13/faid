from faid.logging import (
    get_model_log_file_path,
    get_risk_register_log_path,
    get_model_entry,
    add_model_entry,
    add_data_entry,
    get_data_entry,
    get_risk_entries,
    add_risk_entry,
    get_transparency_record,
    add_transparency_entry
)

model_file_path = get_model_log_file_path()
risk_file_path = get_risk_register_log_path()

def sync_model_to_risk():
    model_risks = get_model_entry("considerations").get('risks', [])
    
    # Sync the related entities
    for i, risk in enumerate(model_risks):
       add_risk_entry(description= risk.get('name', ''), 
                      impact= '',  # Add logic to determine impact if needed
                      likelihood= '',  # Add logic to determine likelihood if needed
                      mitigation= risk.get('mitigation_strategy', '')
                      )

def sync_model_to_data():
    model_data = get_model_entry("data")
    add_data_entry("summary", model_data.get('description', ''))
    add_data_entry("dataset_link", model_data.get('link', ''))
    add_data_entry("protected_characteristics", model_data.get('sensitive', ''))

def sync_model_to_usecase():
    # Implement the logic to sync model to usecase
    pass

def sync_data_to_model():
    data_entry = {
        "description" : get_data_entry("summary"),
        "link" : get_data_entry("dataset_link"),
        "sensitive" : get_data_entry("protected_characteristics"),
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
    risk_entry = get_risk_entries()
    model_risks = risk_entry.get('risks', [])
    
    # Sync the related entities
    for i, risk in enumerate(model_risks):
        add_model_entry({
            'name': risk.get('description', ''),
            'mitigation_strategy': risk.get('mitigation', '')
        }, key='considerations', filename=model_file_path)

def sync_risk_to_data():
    risk_entry = get_risk_entries()
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
    model_info = get_model_entry()
    model_data = model_info.get('model_parameters', '').get('data', '')
    datasets = "".join([data.get('description', '') for data in model_data])
    dataset_purposes = "".join([data.get('purpose', '') for data in model_data])

    transparency_model_specification = {
        "model_name": model_info.get('name', ''),
        "model_version": "Name: " + model_info.get('version', '').get('name', '') + " | Date: " + model_info.get('version', '').get('date', '') + " | Diff: " + model_info.get('version', '').get('diff', ''),
        "model_task": model_info.get('overview', ''),
        "model_input": model_info.get('model_parameters', '').get('input_format', ''),
        "model_output": model_info.get('model_parameters', '').get('output_format', ''),
        "model_architecture": model_info.get('model_parameters', '').get('model_architecture', ''),
        "model_performance": model_info.get('qualitative_analysis', '').to_string(),
        "datasets": datasets,
        "dataset_purposes": dataset_purposes
    }

    add_transparency_entry(key="model_specification", entry=transparency_model_specification)

    
def sync_usecase_to_model():
    # Implement the logic to sync usecase to model
    pass

def sync_usecase_to_data():
    # Implement the logic to sync usecase to data
    pass

def sync_usecase_to_transparency():
    # Implement the logic to sync usecase to transparency
    pass
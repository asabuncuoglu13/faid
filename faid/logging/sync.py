from faid.logging import (
    get_model_log_file_path,
    get_risk_register_log_path,
    ModelCard,
    DataCard,
    get_model_entry,
    get_data_entry,
    get_risk_entries,
    add_risk_entry,
    add_transparency_entry
)

model_file_path = get_model_log_file_path()
risk_file_path = get_risk_register_log_path()

def sync_model_to_risk():
    """
    Sync the risk field in the model metadata to the risk register
    """
    model_risks = get_model_entry("considerations").get('risks', [])
    
    # Sync the related entities
    for i, risk in enumerate(model_risks):
       add_risk_entry(description= risk.get('name', ''), 
                      impact= '',  # Add logic to determine impact if needed
                      likelihood= '',  # Add logic to determine likelihood if needed
                      mitigation= risk.get('mitigation_strategy', '')
                      )
       
def sync_model_to_transparency():
    """
    Sync the related information in the model metadata to the transparency log
    """
    # Implement the logic to sync model to transparency
    model_info = get_model_entry()
    model_details = model_info.get('model_details', '')
    model_data = model_info.get('model_parameters', '').get('data', '')
    datasets = "".join([data.get('description', '') for data in model_data])
    dataset_purposes = "".join([data.get('purpose', '') for data in model_data])

    transparency_model_specification = {
        "model_name": model_details.get('name', ''),
        "model_version": "Name: " + model_details.get('version', '').get('name', '') + " | Date: " + model_details.get('version', '').get('date', '') + " | Diff: " + model_details.get('version', '').get('diff', ''),
        "model_task": model_details.get('overview', ''),
        "model_input": model_info.get('model_parameters', '').get('input_format', ''),
        "model_output": model_info.get('model_parameters', '').get('output_format', ''),
        "model_architecture": model_info.get('model_parameters', '').get('model_architecture', ''),
        "model_performance": model_info.get('qualitative_analysis', ''),
        "datasets": datasets,
        "dataset_purposes": dataset_purposes
    }

    add_transparency_entry(key="model_specification", entry=transparency_model_specification)

def sync_data_to_model():
    """
    Add the current data metadata to the model metadata
    """
    data_entry = {
        "description" : get_data_entry("description").get("summary", ''),
        "link" : get_data_entry("description").get("dataset_link"),
        "sensitive" : get_data_entry("sensitive_data").get("protected_characteristics"),
        "graphics" : "",
        "purpose" : get_data_entry("collection_protocol").get("data_use_cases"),
    }
    model_card = ModelCard()
    data_entries = model_card.get_model_parameters().get('data', [])
    # if data_entry not in data_entries:
    data_entries.append(data_entry)
    model_card.set_model_parameters({"data" : data_entries})
    model_card.save()

def sync_data_to_risk():
    """
    Sync the risk field in the data metadata to the risk register
    """
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
    """
    Sync the related information in the data metadata to the transparency recording
    """
    description = get_data_entry(key='description')
    content = get_data_entry(key='content')
    descriptive_statistics = get_data_entry(key='descriptive_statistics')
    sensitive_data = get_data_entry(key='sensitive_data')
    collection_protocol = get_data_entry(key='collection_protocol')
    transparency_data_specification = {
        "source_data_name": description.get("name"),
        "data_modality": content.get("primary_data_modality"),
        "data_description": content.get("description"),
        "data_quantities": content.get("dataset_snapshot").get('total_records', ''),
        "sensitive_attributes": sensitive_data.get("protected_characteristics"),
        "data_completeness_and_representative_ness": descriptive_statistics.get("has_missing_values", ''),
        "source_data_url": description.get("dataset_link"),
        "data_collection": collection_protocol.get("data_collection", ''),
        "data_cleaning": "",  # Add logic if needed
        "data_sharing_agreements": "",  # Add logic if needed
        "data_access_and_storage": ""  # Add logic if needed
    }
    add_transparency_entry(key="data_specification", entry=transparency_data_specification)
    
def sync_risk_to_model():
    """
    Add the current risks to the model metadata
    """
    risk_entries = get_risk_entries()
    risks = []
    # Sync the related entities
    ids = risk_entries.keys()
    for id in ids:
        risk = risk_entries[id]
        risks.append({
            'name': risk.get('description', ''),
            'mitigation_strategy': risk.get('mitigation', '')
        })

    model_card = ModelCard()
    existing_risks = model_card.get_considerations().get('risks', [])
    existing_risks.extend(risks)
    model_card.set_considerations({"risks" : existing_risks})
    model_card.save()

def sync_risk_to_data():
    """
    Add the current risks to the data metadata"
    """
    risk_entries = get_risk_entries()
    data_card = DataCard()

    ids = risk_entries.keys()
    for id in ids:
        risk = risk_entries[id]
        data_card.add_risk({
            'name': risk.get('description', ''),
            'mitigation_strategy': risk.get('mitigation', '')
        })
    
    data_card.save()

def sync_risk_to_transparency():
    """
    Sync the related information in the risk register to the transparency recording
    """
    risk_entries = get_risk_entries()
    print(risk_entries)

    impact_assessment = "The project risks has the following impact descriptions: \n"
    risk_description = "The project risks has the following descriptions: \n"
    mitigation_strategies = "The project listed the following mitigation strategies: \n"

    ids = risk_entries.keys()
    for id in ids:
        risk = risk_entries[id]
        impact_assessment += risk.get('impact', '')
        risk_description += risk.get('description', '')
        mitigation_strategies += risk.get('mitigation', '')

    add_transparency_entry(
        key="risks_mitigations_and_impact_assessments", 
        entry={"impact_assessment": impact_assessment, 
               "risks_and_mitigations": mitigation_strategies + "\n\n" + risk_description
               })
from . import app, experiment_dao, generic_dao, study_dao
from flask import request, jsonify, json

@app.route('/create_dataset', methods=['POST'])
def create_datasets():
    dataset_data = request.json
    dataset = dataset_data.get('dataset', {})
    accession = dataset_data.get('sample_id', '')
    dataset_id = dataset_data.get('dataset_id', '')
    data_dataset_experiment = json.dump(dataset_data)
    try:
        temp_dataset_node = generic_dao.get_node(data_dataset_experiment.__getattribute__("dataset_id"))
        if temp_dataset_node is not None:
            response_data = {"error" : "A dataset with this ID already exists in the database"}
            return jsonify(response_data), 500
    except Exception as e:
        pass
    created_dataset_result = generic_dao.create_node(node_type='Dataset', data=data_dataset_experiment)
    rel_result = generic_dao.relationship_builder(parent_node_type='Sample', child_node_type='Dataset', parent_identifier=accession, child_identifier= dataset_id)
    response_data = {
        "message" : f"Dataset node {dataset_id} for sample {accession}"
    }
    return jsonify(response_data),200

@app.route("/update_dataset/<dataset_id>", methods=['PUT'])
def update_datasets(dataset_id):
    dataset_data = request.json
    try:
        update_result = generic_dao.update_node(node_type='Dataset', identifier=dataset_id, updated_data=dataset_data)
        if update_datasets:
            response_data = {
                "message" : "Dataset node updated successfully"
            }
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(response_data), 200


@app.route("/get_dataset/<dataset_id>", methods=['GET'])
def get_dataset(dataset_id):
    res_get_dataset = generic_dao.get_node(node_type='Dataset', identifier=dataset_id)
    if res_get_dataset:
        return jsonify(res_get_dataset), 200
    return jsonify(res_get_dataset), 500

@app.route("/delete_dataset/<dataset_id>", methods=['DELETE'])
def delete_dataset(dataset_id):
    deletion_success = generic_dao.delete_node(node_type="Dataset",identifier=dataset_id)
    if deletion_success:
        return jsonify({"message": f"Dataset id: {dataset_id} deleted successfully"}), 200
    return jsonify({"error": f"Unable to delete Dataset id: {dataset_id}"}), 500

@app.route("/get_sample/<dataset_id>", methods=['GET'])
def get_sample_dataset(dataset_id):
    sample_json = genericDao.get_node("dataset",dataset_id)
    sample_json_dumped = json.dump(sample_json)
    parent_sample_id = sample_json_dumped.__getitem__("sample_id")
    get_sample_res = generic_dao.get_node(node_type="Sample", identifier=parent_sample_id)
    if get_sample_dataset:
        return jsonify(get_sample_dataset), 200
    return jsonify( {"message": f"Could not find sample attached to dataset {dataset_id}"}), 500


# routes/patient_routes.py
from flask import Blueprint, request, jsonify
from models.patient import Patient
from extensions import db

patient_bp = Blueprint('patient_bp', __name__, url_prefix='/patients')


# GET all patients
@patient_bp.route('/', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    return jsonify([{
        "id": p.id,
        "full_name": p.full_name,
        "phone_number": p.phone_number,
        "email": p.email,
        "age": p.age,
        "gender": p.gender
    } for p in patients])


# GET one patient by ID
@patient_bp.route('/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"message": "Patient not found"}), 404
    return jsonify({
        "id": patient.id,
        "full_name": patient.full_name,
        "phone_number": patient.phone_number,
        "email": patient.email,
        "age": patient.age,
        "gender": patient.gender
    })


# POST - create new patient
@patient_bp.route('/', methods=['POST'])
def create_patient():
    data = request.json
    new_patient = Patient(
        full_name=data.get('full_name'),
        phone_number=data.get('phone_number'),
        email=data.get('email'),
        age=data.get('age'),
        gender=data.get('gender')
    )
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({"message": "Patient created", "id": new_patient.id}), 201


# PUT - update patient
@patient_bp.route('/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"message": "Patient not found"}), 404

    data = request.json
    patient.full_name = data.get('full_name', patient.full_name)
    patient.phone_number = data.get('phone_number', patient.phone_number)
    patient.email = data.get('email', patient.email)
    patient.age = data.get('age', patient.age)
    patient.gender = data.get('gender', patient.gender)

    db.session.commit()
    return jsonify({"message": "Patient updated"})


# DELETE patient
@patient_bp.route('/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"message": "Patient not found"}), 404

    db.session.delete(patient)
    db.session.commit()
    return jsonify({"message": "Patient deleted"})

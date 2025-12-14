"""
MongoDB connection and operations for Visit History feature.

This module handles MongoDB operations for storing visit history records.
Visit history is stored in MongoDB (unstructured data) while appointments
are stored in PostgreSQL (structured data) - demonstrating polyglot persistence.
"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from decouple import config
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)

# MongoDB connection settings from environment variables
# Note: Password should be URL-encoded if it contains special characters
# Example: Vigi@Expo49 should be Vigi%40Expo49
MONGODB_URI = config(
    'MONGODB_URI',
    default='mongodb+srv://VigilantEye:Vigi%40Expo49@cluster0.pomckdi.mongodb.net/?appName=Cluster0'
)
MONGODB_DB_NAME = config('MONGODB_DB_NAME', default='clinic_appointment')
MONGODB_COLLECTION_NAME = config('MONGODB_COLLECTION_NAME', default='visit_history')

# Global MongoDB client (singleton pattern)
_mongo_client = None
_mongo_db = None


def get_mongo_client():
    """
    Get or create MongoDB client connection.
    Uses singleton pattern to reuse connection.
    
    Returns:
        MongoClient: MongoDB client instance
        
    Raises:
        ConnectionFailure: If unable to connect to MongoDB
    """
    global _mongo_client
    
    if _mongo_client is None:
        try:
            _mongo_client = MongoClient(
                MONGODB_URI,
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                connectTimeoutMS=10000,
                socketTimeoutMS=10000
            )
            # Test connection
            _mongo_client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    return _mongo_client


def get_mongo_db():
    """
    Get MongoDB database instance.
    
    Returns:
        Database: MongoDB database instance
    """
    global _mongo_db
    
    if _mongo_db is None:
        client = get_mongo_client()
        _mongo_db = client[MONGODB_DB_NAME]
    
    return _mongo_db


def get_visit_history_collection():
    """
    Get the visit history collection from MongoDB.
    
    Returns:
        Collection: MongoDB collection for visit history
    """
    db = get_mongo_db()
    return db[MONGODB_COLLECTION_NAME]


def insert_visit_history(appointment_id, patient_id, doctor_id, visit_date, 
                         notes=None, prescription=None):
    """
    Insert a new visit history record into MongoDB.
    
    Args:
        appointment_id (int): PostgreSQL appointment ID
        patient_id (int): Patient user ID
        doctor_id (int): Doctor user ID
        visit_date (str or datetime): Date of the visit
        notes (str, optional): Doctor's notes
        prescription (str or list, optional): Prescription information
        
    Returns:
        dict: Inserted document with _id
    """
    collection = get_visit_history_collection()
    
    # Convert visit_date to datetime if needed
    if isinstance(visit_date, str):
        try:
            visit_date = datetime.fromisoformat(visit_date.replace('Z', '+00:00'))
        except ValueError:
            # If ISO format fails, try simple date parsing
            try:
                visit_date = datetime.strptime(visit_date, '%Y-%m-%d')
            except ValueError:
                visit_date = datetime.now()
    elif isinstance(visit_date, date) and not isinstance(visit_date, datetime):
        # If it's a date object, convert to datetime
        visit_date = datetime.combine(visit_date, datetime.min.time())
    elif not isinstance(visit_date, datetime):
        visit_date = datetime.now()
    
    visit_record = {
        'appointment_id': appointment_id,
        'patient_id': patient_id,
        'doctor_id': doctor_id,
        'visit_date': visit_date,
        'notes': notes or '',
        'prescription': prescription or '',
        'created_at': datetime.utcnow()
    }
    
    result = collection.insert_one(visit_record)
    visit_record['_id'] = result.inserted_id
    
    logger.info(f"Visit history inserted for appointment {appointment_id}")
    return visit_record


def get_visit_history_by_patient(patient_id):
    """
    Get all visit history records for a specific patient.
    
    Args:
        patient_id (int): Patient user ID
        
    Returns:
        list: List of visit history documents
    """
    collection = get_visit_history_collection()
    
    # Query MongoDB for patient's visit history, sorted by visit_date descending
    cursor = collection.find(
        {'patient_id': patient_id}
    ).sort('visit_date', -1)
    
    # Convert ObjectId to string for JSON serialization
    records = []
    for doc in cursor:
        doc['_id'] = str(doc['_id'])
        # Convert datetime to ISO format string
        if isinstance(doc.get('visit_date'), datetime):
            doc['visit_date'] = doc['visit_date'].isoformat()
        if isinstance(doc.get('created_at'), datetime):
            doc['created_at'] = doc['created_at'].isoformat()
        records.append(doc)
    
    return records


def get_visit_history_by_doctor(doctor_id):
    """
    Get all visit history records for appointments handled by a specific doctor.
    
    Args:
        doctor_id (int): Doctor user ID
        
    Returns:
        list: List of visit history documents
    """
    collection = get_visit_history_collection()
    
    # Query MongoDB for doctor's visit history, sorted by visit_date descending
    cursor = collection.find(
        {'doctor_id': doctor_id}
    ).sort('visit_date', -1)
    
    # Convert ObjectId to string for JSON serialization
    records = []
    for doc in cursor:
        doc['_id'] = str(doc['_id'])
        # Convert datetime to ISO format string
        if isinstance(doc.get('visit_date'), datetime):
            doc['visit_date'] = doc['visit_date'].isoformat()
        if isinstance(doc.get('created_at'), datetime):
            doc['created_at'] = doc['created_at'].isoformat()
        records.append(doc)
    
    return records


def get_all_visit_history():
    """
    Get all visit history records (for admins).
    
    Returns:
        list: List of all visit history documents
    """
    collection = get_visit_history_collection()
    
    # Query all records, sorted by visit_date descending
    cursor = collection.find().sort('visit_date', -1)
    
    # Convert ObjectId to string for JSON serialization
    records = []
    for doc in cursor:
        doc['_id'] = str(doc['_id'])
        # Convert datetime to ISO format string
        if isinstance(doc.get('visit_date'), datetime):
            doc['visit_date'] = doc['visit_date'].isoformat()
        if isinstance(doc.get('created_at'), datetime):
            doc['created_at'] = doc['created_at'].isoformat()
        records.append(doc)
    
    return records


def get_visit_history_by_appointment(appointment_id):
    """
    Get visit history for a specific appointment.
    
    Args:
        appointment_id (int): PostgreSQL appointment ID
        
    Returns:
        dict or None: Visit history document or None if not found
    """
    collection = get_visit_history_collection()
    
    doc = collection.find_one({'appointment_id': appointment_id})
    
    if doc:
        doc['_id'] = str(doc['_id'])
        # Convert datetime to ISO format string
        if isinstance(doc.get('visit_date'), datetime):
            doc['visit_date'] = doc['visit_date'].isoformat()
        if isinstance(doc.get('created_at'), datetime):
            doc['created_at'] = doc['created_at'].isoformat()
    
    return doc


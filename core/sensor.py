import time
import random
import json

def get_sensor_reading(device_id="sensor-device-01"):
    return {
        "deviceId": device_id,
        "temperature": round(random.uniform(60, 120), 2),
        "pressure": round(random.uniform(14, 16), 2),
        "vibration": round(random.uniform(0, 5), 2),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }

def is_anomaly(reading, threshold=100):
    """Returns True if temperature exceeds the threshold."""
    return reading["temperature"] > threshold

def validate_reading(reading):
    """Validates that a sensor reading has all required fields with correct types."""
    required_fields = {
        "deviceId": str,
        "temperature": (int, float),
        "pressure": (int, float),
        "vibration": (int, float),
        "timestamp": str
    }
    for field, expected_type in required_fields.items():
        if field not in reading:
            return False, f"Missing field: {field}"
        if not isinstance(reading[field], expected_type):
            return False, f"Invalid type for {field}"
    return True, "Valid"
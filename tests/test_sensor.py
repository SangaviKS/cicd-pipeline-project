import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.sensor import get_sensor_reading, is_anomaly, validate_reading

def test_get_sensor_reading_returns_dict():
    reading = get_sensor_reading()
    assert isinstance(reading, dict)

def test_get_sensor_reading_has_required_fields():
    reading = get_sensor_reading()
    expected_fields = {"deviceId", "temperature", "pressure", "vibration", "timestamp"}
    assert expected_fields.issubset(reading.keys())

def test_temperature_within_expected_range():
    reading = get_sensor_reading()
    assert 60 <= reading["temperature"] <= 120

def test_pressure_within_expected_range():
    reading = get_sensor_reading()
    assert 14 <= reading["pressure"] <= 16

def test_vibration_within_expected_range():
    reading = get_sensor_reading()
    assert 0 <= reading["vibration"] <= 5

def test_device_id_default():
    reading = get_sensor_reading()
    assert reading["deviceId"] == "sensor-device-01"

def test_device_id_custom():
    reading = get_sensor_reading(device_id="sensor-device-02")
    assert reading["deviceId"] == "sensor-device-02"

def test_is_anomaly_detects_high_temperature():
    reading = {"temperature": 105}
    assert is_anomaly(reading) == True

def test_is_anomaly_ignores_normal_temperature():
    reading = {"temperature": 85}
    assert is_anomaly(reading) == False

def test_is_anomaly_custom_threshold():
    reading = {"temperature": 90}
    assert is_anomaly(reading, threshold=80) == True

def test_validate_reading_accepts_valid_data():
    reading = get_sensor_reading()
    is_valid, message = validate_reading(reading)
    assert is_valid == True

def test_validate_reading_rejects_missing_field():
    reading = {"deviceId": "sensor-01", "temperature": 75.0}
    is_valid, message = validate_reading(reading)
    assert is_valid == False
    assert "Missing field" in message

def test_validate_reading_rejects_wrong_type():
    reading = {
        "deviceId": "sensor-01",
        "temperature": "not-a-number",
        "pressure": 15.0,
        "vibration": 2.0,
        "timestamp": "2026-06-15T10:00:00Z"
    }
    is_valid, message = validate_reading(reading)
    assert is_valid == False
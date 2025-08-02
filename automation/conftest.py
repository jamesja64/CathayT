import pytest
import requests
import json
from datetime import datetime

# 測試配置
BASE_URL = "https://api.practicesoftwaretesting.com"

@pytest.fixture(scope="session")
def api_base_url():
    """API基礎URL"""
    return BASE_URL

@pytest.fixture(scope="session")
def session():
    """建立HTTP會話"""
    session = requests.Session()
    session.headers.update({
        'Content-Type': 'application/json',
        'User-Agent': 'Cathay-API-Test/1.0'
    })
    return session

@pytest.fixture
def test_data():
    """測試資料"""
    return {
        "valid_message": {
            "name": "Test User",
            "subject": "API Test",
            "message": "This is a test message for API testing.",
            "email": "test@example.com"
        },
        "invalid_message": {
            "name": "",
            "subject": "",
            "message": "",
            "email": "invalid-email"
        },
        "price_ranges": [
            {"min": 1, "max": 78},
            {"min": 1, "max": 100},
            {"min": 10, "max": 50}
        ]
    }

def pytest_configure(config):
    """pytest配置"""
    config.addinivalue_line(
        "markers", "p1: 高優先級測試案例"
    )
    config.addinivalue_line(
        "markers", "p2: 中優先級測試案例"
    )
    config.addinivalue_line(
        "markers", "p3: 低優先級測試案例"
    ) 
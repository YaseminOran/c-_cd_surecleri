#!/usr/bin/env python3
"""
Basit Flask App Testleri - CI/CD Pipeline için
Sadece çalışan temel testler
"""

import pytest
import json
import sys
import os

# Src dizinini path'e ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import app

@pytest.fixture
def client():
    """Test client fixture"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestBasicEndpoints:
    """Temel endpoint testleri"""
    
    def test_home_endpoint(self, client):
        """Ana sayfa endpoint'ini test et"""
        response = client.get('/')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['service'] == 'CI/CD Example API'
        assert data['version'] == '1.0.0'
        assert data['status'] == 'running'
    
    def test_health_endpoint(self, client):
        """Sağlık kontrolü endpoint'ini test et"""
        response = client.get('/health')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['status'] in ['healthy', 'unhealthy']
        assert 'model_loaded' in data
    
    def test_predict_endpoint_valid(self, client):
        """Geçerli prediction endpoint'ini test et"""
        test_data = {'value': 50}
        response = client.post('/predict',
                             data=json.dumps(test_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert 'prediction' in data
        assert 'status' in data
        assert data['status'] == 'success'
    
    def test_predict_endpoint_invalid(self, client):
        """Geçersiz prediction endpoint'ini test et"""
        test_data = {'invalid': 'data'}
        response = client.post('/predict',
                             data=json.dumps(test_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        
        assert data['status'] == 'error'
    
    def test_metrics_endpoint(self, client):
        """Metrics endpoint'ini test et"""
        response = client.get('/metrics')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert 'total_predictions' in data
        assert 'uptime_seconds' in data
    
    def test_404_endpoint(self, client):
        """Olmayan endpoint'i test et"""
        response = client.get('/nonexistent')
        
        assert response.status_code == 404
        data = response.get_json()
        
        assert data['status'] == 'error'
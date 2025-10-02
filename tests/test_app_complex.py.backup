#!/usr/bin/env python3
"""
Flask App Testleri - CI/CD Pipeline için
API endpoint'lerini test eder
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
        yield client

class TestAppEndpoints:
    """App endpoint testleri"""
    
    def test_home_endpoint(self, client):
        """Ana sayfa endpoint'ini test et"""
        response = client.get('/')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['service'] == 'CI/CD Example API'
        assert data['version'] == '1.0.0'
        assert data['status'] == 'running'
        assert 'endpoints' in data
        assert 'timestamp' in data
    
    def test_health_endpoint(self, client):
        """Sağlık kontrolü endpoint'ini test et"""
        response = client.get('/health')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['status'] in ['healthy', 'unhealthy']
        assert 'model_loaded' in data
        assert 'timestamp' in data
        assert data['version'] == '1.0.0'
    
    def test_predict_endpoint_valid_data(self, client):
        """Geçerli veri ile tahmin endpoint'ini test et"""
        test_data = {
            'value': 75,
            'name': 'Test User'
        }
        
        response = client.post('/predict',
                              data=json.dumps(test_data),
                              content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert 'prediction' in data
        assert 'confidence' in data
        assert 'model_version' in data
        assert data['status'] == 'success'
        assert 'timestamp' in data
        assert data['input_value'] == 75
    
    def test_predict_endpoint_minimal_data(self, client):
        """Minimal veri ile tahmin endpoint'ini test et"""
        test_data = {}
        
        response = client.post('/predict',
                              data=json.dumps(test_data),
                              content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert 'prediction' in data
        assert 'confidence' in data
        assert data['status'] == 'success'
    
    def test_predict_endpoint_invalid_data(self, client):
        """Geçersiz veri ile tahmin endpoint'ini test et"""
        test_data = {
            'value': 150  # Range dışı
        }
        
        response = client.post('/predict',
                              data=json.dumps(test_data),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        
        assert data['status'] == 'error'
        assert 'error' in data
    
    def test_predict_endpoint_no_json(self, client):
        """JSON olmayan veri ile tahmin endpoint'ini test et"""
        response = client.post('/predict',
                              data='not json',
                              content_type='text/plain')
        
        assert response.status_code == 400
        data = response.get_json()
        
        assert data['status'] == 'error'
        assert 'Content-Type' in data['error']
    
    def test_metrics_endpoint(self, client):
        """Metrikler endpoint'ini test et"""
        # Önce bir tahmin yap
        test_data = {'value': 50}
        client.post('/predict',
                   data=json.dumps(test_data),
                   content_type='application/json')
        
        # Metrikleri kontrol et
        response = client.get('/metrics')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert 'total_predictions' in data
        assert 'uptime_seconds' in data
        assert 'model_version' in data
        assert 'timestamp' in data
        assert data['total_predictions'] >= 1
    
    def test_404_endpoint(self, client):
        """Olmayan endpoint'i test et"""
        response = client.get('/nonexistent')
        
        assert response.status_code == 404
        data = response.get_json()
        
        assert data['status'] == 'error'
        assert 'bulunamadı' in data['error']
        assert 'available_endpoints' in data

class TestAppIntegration:
    """Integration testleri"""
    
    def test_full_prediction_flow(self, client):
        """Tam tahmin akışını test et"""
        # 1. Health check
        health_response = client.get('/health')
        assert health_response.status_code == 200
        
        # 2. Prediction
        test_data = {'value': 60}
        predict_response = client.post('/predict',
                                     data=json.dumps(test_data),
                                     content_type='application/json')
        assert predict_response.status_code == 200
        
        # 3. Metrics check
        metrics_response = client.get('/metrics')
        assert metrics_response.status_code == 200
        
        metrics_data = metrics_response.get_json()
        assert metrics_data['total_predictions'] >= 1
    
    def test_multiple_predictions(self, client):
        """Birden fazla tahmin test et"""
        test_values = [10, 25, 50, 75, 90]
        
        predictions = []
        for value in test_values:
            test_data = {'value': value}
            response = client.post('/predict',
                                 data=json.dumps(test_data),
                                 content_type='application/json')
            assert response.status_code == 200
            predictions.append(response.get_json()['prediction'])
        
        # Tüm tahminler alındı mı kontrol et
        assert len(predictions) == len(test_values)
        
        # Tahminler 0-1 arasında mı kontrol et
        for pred in predictions:
            assert 0 <= pred <= 1
    
    def test_concurrent_requests(self, client):
        """Eş zamanlı istekleri test et (basit)"""
        import threading
        import time
        
        results = []
        
        def make_request():
            test_data = {'value': 50}
            response = client.post('/predict',
                                 data=json.dumps(test_data),
                                 content_type='application/json')
            results.append(response.status_code)
        
        # 5 thread ile eş zamanlı istek
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Tüm thread'lerin bitmesini bekle
        for thread in threads:
            thread.join()
        
        # Tüm istekler başarılı mı kontrol et
        assert len(results) == 5
        assert all(status == 200 for status in results)

class TestAppPerformance:
    """Performance testleri"""
    
    def test_prediction_response_time(self, client):
        """Tahmin response süresini test et"""
        import time
        
        test_data = {'value': 50}
        
        start_time = time.time()
        response = client.post('/predict',
                              data=json.dumps(test_data),
                              content_type='application/json')
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 1.0  # 1 saniyeden az olmalı

if __name__ == '__main__':
    # Testleri doğrudan çalıştır
    import subprocess
    import sys
    
    print("🧪 App testleri çalıştırılıyor...")
    result = subprocess.run([sys.executable, '-m', 'pytest', __file__, '-v'], 
                           capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)
    
    if result.returncode == 0:
        print("✅ Tüm testler başarılı!")
    else:
        print("❌ Bazı testler başarısız!")
    
    sys.exit(result.returncode)
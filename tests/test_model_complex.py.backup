#!/usr/bin/env python3
"""
Model Testleri - CI/CD Pipeline için
Model fonksiyonlarını test eder
"""

import pytest
import sys
import os
import time

# Src dizinini path'e ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from model import SimpleModel

class TestSimpleModel:
    """SimpleModel testleri"""
    
    def test_model_initialization(self):
        """Model başlatılması test et"""
        model = SimpleModel()
        
        assert model.model_version == "1.0.0"
        assert model.prediction_count == 0
        assert model.last_prediction_time is None
        assert model.is_loaded == True
        assert model.created_at > 0
    
    def test_model_predict_with_value(self):
        """Value ile tahmin test et"""
        model = SimpleModel()
        test_data = {'value': 50}
        
        result = model.predict(test_data)
        
        assert 'prediction' in result
        assert 'confidence' in result
        assert 'model_version' in result
        assert 0 <= result['prediction'] <= 1
        assert 0 <= result['confidence'] <= 1
        assert result['model_version'] == "1.0.0"
        assert model.prediction_count == 1
        assert model.last_prediction_time is not None
    
    def test_model_predict_without_value(self):
        """Value olmadan tahmin test et"""
        model = SimpleModel()
        test_data = {}
        
        result = model.predict(test_data)
        
        assert 'prediction' in result
        assert 'confidence' in result
        assert 0 <= result['prediction'] <= 1
        assert model.prediction_count == 1
    
    def test_model_predict_edge_cases(self):
        """Edge case'leri test et"""
        model = SimpleModel()
        
        # Test case 1: Value = 0
        result = model.predict({'value': 0})
        assert 0 <= result['prediction'] <= 1
        
        # Test case 2: Value = 100
        result = model.predict({'value': 100})
        assert 0 <= result['prediction'] <= 1
        
        # Test case 3: Negative value
        result = model.predict({'value': -10})
        assert 0 <= result['prediction'] <= 1
        
        # Test case 4: Large positive value
        result = model.predict({'value': 1000})
        assert 0 <= result['prediction'] <= 1
    
    def test_model_predict_invalid_value(self):
        """Geçersiz value ile test et"""
        model = SimpleModel()
        
        # String value
        with pytest.raises(ValueError):
            model.predict({'value': 'invalid'})
    
    def test_model_health_check(self):
        """Model sağlık kontrolü test et"""
        model = SimpleModel()
        
        # Başlangıçta healthy olmalı
        assert model.is_healthy() == True
        
        # Error simüle et
        model.simulate_error()
        assert model.is_healthy() == False
        
        # Recover et
        model.recover()
        assert model.is_healthy() == True
    
    def test_model_statistics(self):
        """Model istatistiklerini test et"""
        model = SimpleModel()
        
        # Başlangıç durumu
        assert model.get_prediction_count() == 0
        assert model.get_uptime() >= 0
        assert model.get_last_prediction_time() is None
        assert model.get_version() == "1.0.0"
        
        # Tahmin yap
        model.predict({'value': 50})
        
        # İstatistikler güncellenmiş olmalı
        assert model.get_prediction_count() == 1
        assert model.get_last_prediction_time() is not None
    
    def test_model_multiple_predictions(self):
        """Birden fazla tahmin test et"""
        model = SimpleModel()
        
        predictions = []
        for i in range(10):
            result = model.predict({'value': i * 10})
            predictions.append(result['prediction'])
        
        # Tüm tahminler valid olmalı
        assert len(predictions) == 10
        assert all(0 <= p <= 1 for p in predictions)
        assert model.get_prediction_count() == 10
    
    def test_model_uptime(self):
        """Model uptime test et"""
        model = SimpleModel()
        
        initial_uptime = model.get_uptime()
        
        # Kısa süre bekle
        time.sleep(0.1)
        
        later_uptime = model.get_uptime()
        
        assert later_uptime >= initial_uptime
    
    def test_model_reset_stats(self):
        """İstatistik sıfırlama test et"""
        model = SimpleModel()
        
        # Birkaç tahmin yap
        model.predict({'value': 50})
        model.predict({'value': 75})
        
        assert model.get_prediction_count() == 2
        assert model.get_last_prediction_time() is not None
        
        # İstatistikleri sıfırla
        model.reset_stats()
        
        assert model.get_prediction_count() == 0
        assert model.get_last_prediction_time() is None

class TestModelPerformance:
    """Model performance testleri"""
    
    def test_prediction_speed(self):
        """Tahmin hızını test et"""
        model = SimpleModel()
        
        start_time = time.time()
        
        # 100 tahmin yap
        for i in range(100):
            model.predict({'value': i})
        
        end_time = time.time()
        total_time = end_time - start_time
        avg_time = total_time / 100
        
        # Her tahmin 10ms'den az sürmeli
        assert avg_time < 0.01
        assert total_time < 1.0
    
    def test_memory_usage(self):
        """Bellek kullanımı test et (basit)"""
        model = SimpleModel()
        
        # Çok sayıda tahmin yap
        for i in range(1000):
            model.predict({'value': i % 100})
        
        # Model hala çalışıyor olmalı
        assert model.is_healthy()
        assert model.get_prediction_count() == 1000
    
    def test_concurrent_predictions(self):
        """Eş zamanlı tahminleri test et"""
        import threading
        
        model = SimpleModel()
        results = []
        errors = []
        
        def make_prediction(value):
            try:
                result = model.predict({'value': value})
                results.append(result)
            except Exception as e:
                errors.append(str(e))
        
        # 10 thread ile eş zamanlı tahmin
        threads = []
        for i in range(10):
            thread = threading.Thread(target=make_prediction, args=(i * 10,))
            threads.append(thread)
            thread.start()
        
        # Tüm thread'lerin bitmesini bekle
        for thread in threads:
            thread.join()
        
        # Sonuçları kontrol et
        assert len(errors) == 0  # Hata olmamalı
        assert len(results) == 10  # 10 başarılı sonuç olmalı
        assert model.get_prediction_count() == 10

class TestModelEdgeCases:
    """Model edge case testleri"""
    
    def test_extreme_values(self):
        """Aşırı değerleri test et"""
        model = SimpleModel()
        
        extreme_values = [
            -1000000,
            1000000,
            0.000001,
            999999.999999
        ]
        
        for value in extreme_values:
            result = model.predict({'value': value})
            assert 0 <= result['prediction'] <= 1
            assert 0 <= result['confidence'] <= 1
    
    def test_special_float_values(self):
        """Özel float değerlerini test et"""
        model = SimpleModel()
        
        # Infinity
        with pytest.raises((ValueError, OverflowError, TypeError)):
            model.predict({'value': float('inf')})
        
        # NaN 
        with pytest.raises((ValueError, TypeError)):
            model.predict({'value': float('nan')})
    
    def test_empty_and_none_inputs(self):
        """Boş ve None input'ları test et"""
        model = SimpleModel()
        
        # Empty dict - should work
        result = model.predict({})
        assert 'prediction' in result
        
        # None value - should raise error
        with pytest.raises((TypeError, ValueError)):
            model.predict({'value': None})

if __name__ == '__main__':
    # Testleri doğrudan çalıştır
    import subprocess
    import sys
    
    print("🧪 Model testleri çalıştırılıyor...")
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
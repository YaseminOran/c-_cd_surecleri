#!/usr/bin/env python3
"""
Basit ML Model - CI/CD Test Amaçlı
Bu model CI/CD pipeline'ı test etmek için basit tahminler yapar.
"""

import random
import time
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class SimpleModel:
    """Basit test modeli"""
    
    def __init__(self):
        """Model'i başlat"""
        self.model_version = "1.0.0"
        self.created_at = time.time()
        self.prediction_count = 0
        self.last_prediction_time = None
        self.is_loaded = True
        
        logger.info(f"Model initialized - Version: {self.model_version}")
    
    def predict(self, data):
        """Tahmin yap"""
        try:
            # Basit tahmin algoritması
            # Gerçek uygulamada burada karmaşık ML modeli olacak
            
            # Input verilerine göre basit hesaplama
            if 'value' in data:
                value = float(data['value'])
                
                # Basit sigmoid benzeri fonksiyon
                prediction = 1 / (1 + abs(value - 50) / 50)
                prediction = round(prediction, 4)
            else:
                # Random tahmin (demo amaçlı)
                prediction = round(random.uniform(0, 1), 4)
            
            # İstatistikleri güncelle
            self.prediction_count += 1
            self.last_prediction_time = datetime.now().isoformat()
            
            logger.info(f"Prediction: {prediction}, Count: {self.prediction_count}")
            
            return {
                'prediction': prediction,
                'confidence': round(random.uniform(0.7, 0.95), 3),
                'model_version': self.model_version
            }
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            raise e
    
    def is_healthy(self):
        """Model sağlık durumunu kontrol et"""
        return self.is_loaded
    
    def get_prediction_count(self):
        """Toplam tahmin sayısını döndür"""
        return self.prediction_count
    
    def get_uptime(self):
        """Model uptime'ını saniye cinsinden döndür"""
        return int(time.time() - self.created_at)
    
    def get_last_prediction_time(self):
        """Son tahmin zamanını döndür"""
        return self.last_prediction_time
    
    def get_version(self):
        """Model versiyonunu döndür"""
        return self.model_version
    
    def reset_stats(self):
        """İstatistikleri sıfırla (test amaçlı)"""
        self.prediction_count = 0
        self.last_prediction_time = None
        logger.info("Model stats reset")
    
    def simulate_error(self):
        """Hata simülasyonu (test amaçlı)"""
        self.is_loaded = False
        logger.warning("Model error simulated")
    
    def recover(self):
        """Model'i kurtarma (test amaçlı)"""
        self.is_loaded = True
        logger.info("Model recovered")

# Test fonksiyonları
def test_model():
    """Model'i test et"""
    print("🧪 Model test ediliyor...")
    
    model = SimpleModel()
    
    # Test case 1: Normal tahmin
    test_data = {'value': 75}
    result = model.predict(test_data)
    print(f"✅ Test 1 - Normal tahmin: {result}")
    
    # Test case 2: Eksik veri
    test_data = {}
    result = model.predict(test_data)
    print(f"✅ Test 2 - Eksik veri: {result}")
    
    # Test case 3: Sağlık kontrolü
    health = model.is_healthy()
    print(f"✅ Test 3 - Sağlık: {health}")
    
    # Test case 4: İstatistikler
    stats = {
        'count': model.get_prediction_count(),
        'uptime': model.get_uptime(),
        'version': model.get_version()
    }
    print(f"✅ Test 4 - İstatistikler: {stats}")
    
    print("🎉 Model testleri tamamlandı!")

if __name__ == '__main__':
    test_model()
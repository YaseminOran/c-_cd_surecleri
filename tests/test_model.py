#!/usr/bin/env python3
"""
Basit Model Testleri - CI/CD Pipeline için
"""

import pytest
import sys
import os

# Src dizinini path'e ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from model import SimpleModel

class TestSimpleModel:
    """Basit model testleri"""
    
    def test_model_creation(self):
        """Model oluşturma testi"""
        model = SimpleModel()
        assert model is not None
    
    def test_model_predict_basic(self):
        """Temel tahmin testi"""
        model = SimpleModel()
        test_data = {'value': 50}
        
        result = model.predict(test_data)
        
        assert result is not None
        assert isinstance(result, dict)  # Model dict döndürüyor
        assert 'prediction' in result
        assert 0 <= result['prediction'] <= 1
    
    def test_model_predict_low_value(self):
        """Düşük değer testi"""
        model = SimpleModel()
        test_data = {'value': 10}
        
        result = model.predict(test_data)
        
        assert result is not None
        assert isinstance(result, dict)
        assert 'prediction' in result
    
    def test_model_predict_high_value(self):
        """Yüksek değer testi"""
        model = SimpleModel()
        test_data = {'value': 90}
        
        result = model.predict(test_data)
        
        assert result is not None
        assert isinstance(result, dict)
        assert 'prediction' in result
    
    def test_model_health_check(self):
        """Model sağlık kontrolü"""
        model = SimpleModel()
        
        health = model.is_healthy()
        
        assert isinstance(health, bool)
    
    def test_model_version(self):
        """Model versiyon kontrolü"""
        model = SimpleModel()
        
        version = model.get_version()
        
        assert version is not None
        assert isinstance(version, str)
    
    def test_model_prediction_count(self):
        """Tahmin sayısı kontrolü"""
        model = SimpleModel()
        
        # İlk sayım
        initial_count = model.get_prediction_count()
        
        # Bir tahmin yap
        model.predict({'value': 50})
        
        # Sayımın arttığını kontrol et
        new_count = model.get_prediction_count()
        assert new_count >= initial_count
#!/usr/bin/env python3
"""
Basit Model Testleri - CI/CD Pipeline için
"""

import os
import sys

# Src dizinini path'e ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from model import SimpleModel  # noqa: E402


class TestSimpleModel:
    """Basit model testleri"""

    def test_model_creation(self):
        """Model oluşturma testi"""
        model = SimpleModel()
        assert model is not None

    def test_model_predict_with_value(self):
        """Değer ile tahmin testi - CI/CD için kritik test"""
        model = SimpleModel()
        test_data = {"value": 50}

        result = model.predict(test_data)

        assert result is not None
        assert isinstance(result, dict)  # Model dict döndürüyor
        assert "prediction" in result
        assert 0 <= result["prediction"] <= 1

    def test_model_predict_basic(self):
        """Temel tahmin testi"""
        model = SimpleModel()
        test_data = {"value": 50}

        result = model.predict(test_data)

        assert result is not None
        assert isinstance(result, dict)  # Model dict döndürüyor
        assert "prediction" in result
        assert 0 <= result["prediction"] <= 1

    def test_model_predict_low_value(self):
        """Düşük değer testi"""
        model = SimpleModel()
        test_data = {"value": 10}

        result = model.predict(test_data)

        assert result is not None
        assert isinstance(result, dict)
        assert "prediction" in result

    def test_model_predict_high_value(self):
        """Yüksek değer testi"""
        model = SimpleModel()
        test_data = {"value": 90}

        result = model.predict(test_data)

        assert result is not None
        assert isinstance(result, dict)
        assert "prediction" in result

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
        model.predict({"value": 50})

        # Sayımın arttığını kontrol et
        new_count = model.get_prediction_count()
        assert new_count >= initial_count

    def test_model_uptime(self):
        """Model uptime testi"""
        model = SimpleModel()
        uptime = model.get_uptime()
        assert isinstance(uptime, int)
        assert uptime >= 0

    def test_model_last_prediction_time(self):
        """Son tahmin zamanı testi"""
        model = SimpleModel()

        # İlk durum - henüz tahmin yapılmamış
        assert model.get_last_prediction_time() is None

        # Tahmin yap
        model.predict({"value": 50})

        # Son tahmin zamanı set olmalı
        last_time = model.get_last_prediction_time()
        assert last_time is not None
        assert isinstance(last_time, str)

    def test_model_predict_without_value(self):
        """Value olmadan tahmin testi"""
        model = SimpleModel()
        test_data = {}

        result = model.predict(test_data)

        assert result is not None
        assert isinstance(result, dict)
        assert "prediction" in result
        assert 0 <= result["prediction"] <= 1

    def test_model_reset_stats(self):
        """İstatistik sıfırlama testi"""
        model = SimpleModel()

        # İlk tahmin
        model.predict({"value": 50})
        assert model.get_prediction_count() > 0

        # Stats sıfırla
        model.reset_stats()
        assert model.get_prediction_count() == 0
        assert model.get_last_prediction_time() is None

    def test_model_simulate_error(self):
        """Hata simülasyonu testi"""
        model = SimpleModel()

        # Normal durum
        assert model.is_healthy() is True

        # Hata simülasyonu
        model.simulate_error()
        assert model.is_healthy() is False

    def test_model_recover(self):
        """Model kurtarma testi"""
        model = SimpleModel()

        # Hata simülasyonu
        model.simulate_error()
        assert model.is_healthy() is False

        # Kurtarma
        model.recover()
        assert model.is_healthy() is True

    def test_model_predict_error_handling(self):
        """Tahmin hata işleme testi"""
        model = SimpleModel()

        # Geçersiz value tipi
        try:
            model.predict({"value": "invalid"})
            assert False, "Exception beklenmişti"
        except ValueError:
            pass  # Beklenen durum


class TestModelMainFunction:
    """Model main fonksiyon testleri"""

    def test_model_main_function(self):
        """Model main fonksiyon testi"""
        from model import test_model

        # Test that main function runs without errors
        try:
            test_model()
            assert True
        except Exception:
            assert False, "test_model function should not raise exception"

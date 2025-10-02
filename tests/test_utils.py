#!/usr/bin/env python3
"""
Basit Utils Testleri - CI/CD Pipeline için
"""

import os
import sys

# Src dizinini path'e ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from utils import validate_input, format_response  # noqa: E402


class TestInputValidation:
    """Input validasyon testleri"""

    def test_validate_input_valid_data(self):
        """Geçerli veri validasyonu"""
        valid_data = {"value": 50}

        result = validate_input(valid_data)

        assert result["valid"] is True
        assert "message" in result

    def test_validate_input_invalid_data(self):
        """Geçersiz veri validasyonu"""
        invalid_data = {"value": 150}  # Range dışı değer

        result = validate_input(invalid_data)

        assert result["valid"] is False
        assert "message" in result

    def test_validate_input_empty_data(self):
        """Boş veri validasyonu"""
        empty_data = {}  # Boş dict aslında valid

        result = validate_input(empty_data)

        assert result["valid"] is True  # Boş dict valid
        assert "message" in result

    def test_validate_input_none_data(self):
        """None veri validasyonu"""
        result = validate_input(None)

        assert result["valid"] is False
        assert "message" in result


class TestResponseFormatting:
    """Response formatlama testleri"""

    def test_format_response_basic(self):
        """Temel response formatlama"""
        prediction_result = {
            "prediction": 0.75,
            "confidence": 0.9,
            "model_version": "1.0",
        }  # Dict olmalı
        input_data = {"value": 60}

        result = format_response(prediction_result, input_data)

        assert "prediction" in result
        assert "status" in result
        assert result["status"] == "success"
        assert result["prediction"] == 0.75

    def test_format_response_low_prediction(self):
        """Düşük tahmin response formatlama"""
        prediction_result = {
            "prediction": 0.2,
            "confidence": 0.8,
            "model_version": "1.0",
        }
        input_data = {"value": 20}

        result = format_response(prediction_result, input_data)

        assert result["prediction"] == 0.2
        assert result["status"] == "success"

    def test_format_response_high_prediction(self):
        """Yüksek tahmin response formatlama"""
        prediction_result = {
            "prediction": 0.9,
            "confidence": 0.95,
            "model_version": "1.0",
        }
        input_data = {"value": 90}

        result = format_response(prediction_result, input_data)

        assert result["prediction"] == 0.9
        assert result["status"] == "success"

    def test_format_response_contains_timestamp(self):
        """Response timestamp kontrolü"""
        prediction_result = {
            "prediction": 0.5,
            "confidence": 0.8,
            "model_version": "1.0",
        }
        input_data = {"value": 50}

        result = format_response(prediction_result, input_data)

        assert "timestamp" in result
        assert result["timestamp"] is not None

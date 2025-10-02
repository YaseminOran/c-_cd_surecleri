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


class TestEmailValidation:
    """Email validasyon testleri"""

    def test_is_valid_email_valid(self):
        """Geçerli email testi"""
        from utils import is_valid_email
        
        assert is_valid_email("test@example.com") is True
        assert is_valid_email("user.name@domain.co.uk") is True
        assert is_valid_email("test123@test-domain.org") is True

    def test_is_valid_email_invalid(self):
        """Geçersiz email testi"""
        from utils import is_valid_email
        
        assert is_valid_email("invalid-email") is False
        assert is_valid_email("@domain.com") is False
        assert is_valid_email("test@") is False
        assert is_valid_email("") is False
        assert is_valid_email(None) is False
        assert is_valid_email(123) is False


class TestNameValidation:
    """İsim validasyon testleri"""

    def test_is_valid_name_valid(self):
        """Geçerli isim testi"""
        from utils import is_valid_name
        
        assert is_valid_name("John Doe") is True
        assert is_valid_name("Ali") is True
        assert is_valid_name("  Test  ") is True  # Trim edilir

    def test_is_valid_name_invalid(self):
        """Geçersiz isim testi"""
        from utils import is_valid_name
        
        assert is_valid_name("A") is False  # Too short
        assert is_valid_name("") is False
        assert is_valid_name("   ") is False  # Only spaces
        assert is_valid_name(None) is False
        assert is_valid_name(123) is False


class TestInputValidationExtended:
    """Genişletilmiş input validasyon testleri"""

    def test_validate_input_with_email(self):
        """Email ile veri validasyonu"""
        data_with_email = {"value": 50, "email": "test@example.com"}
        result = validate_input(data_with_email)
        assert result["valid"] is True

        data_with_invalid_email = {"value": 50, "email": "invalid-email"}
        result = validate_input(data_with_invalid_email)
        assert result["valid"] is False

    def test_validate_input_with_name(self):
        """İsim ile veri validasyonu"""
        data_with_name = {"value": 50, "name": "John Doe"}
        result = validate_input(data_with_name)
        assert result["valid"] is True

        data_with_short_name = {"value": 50, "name": "A"}
        result = validate_input(data_with_short_name)
        assert result["valid"] is False

    def test_validate_input_negative_value(self):
        """Negatif değer validasyonu"""
        data = {"value": -10}
        result = validate_input(data)
        assert result["valid"] is False

    def test_validate_input_edge_values(self):
        """Sınır değer validasyonu"""
        # Minimum geçerli değer
        data = {"value": 0}
        result = validate_input(data)
        assert result["valid"] is True

        # Maksimum geçerli değer
        data = {"value": 100}
        result = validate_input(data)
        assert result["valid"] is True

        # Sınır dışı değer
        data = {"value": 100.1}
        result = validate_input(data)
        assert result["valid"] is False


class TestStringSanitization:
    """String temizleme testleri"""

    def test_sanitize_string_basic(self):
        """Temel string temizleme"""
        from utils import sanitize_string
        
        result = sanitize_string("Normal text")
        assert result == "Normal text"

    def test_sanitize_string_html_removal(self):
        """HTML tag kaldırma"""
        from utils import sanitize_string
        
        result = sanitize_string("<script>alert('xss')</script>Clean text")
        assert "<script>" not in result
        assert "Clean text" in result

    def test_sanitize_string_special_chars(self):
        """Özel karakter kaldırma"""
        from utils import sanitize_string
        
        result = sanitize_string('Text with "quotes" and <brackets>')
        assert '"' not in result
        assert '<' not in result
        assert '>' not in result

    def test_sanitize_string_length_limit(self):
        """Uzunluk sınırı"""
        from utils import sanitize_string
        
        long_text = "a" * 150
        result = sanitize_string(long_text, max_length=50)
        assert len(result) <= 53  # 50 + "..."

    def test_sanitize_string_invalid_input(self):
        """Geçersiz input"""
        from utils import sanitize_string
        
        assert sanitize_string(None) == ""
        assert sanitize_string(123) == ""


class TestMetricsCalculation:
    """Metrik hesaplama testleri"""

    def test_calculate_metrics_normal(self):
        """Normal metrik hesaplama"""
        from utils import calculate_metrics
        
        predictions = [0.1, 0.5, 0.8, 0.3, 0.9]
        result = calculate_metrics(predictions)
        
        assert result["count"] == 5
        assert result["mean"] == 0.52
        assert result["min"] == 0.1
        assert result["max"] == 0.9
        assert "std" in result

    def test_calculate_metrics_empty(self):
        """Boş liste metrik hesaplama"""
        from utils import calculate_metrics
        
        result = calculate_metrics([])
        assert result["count"] == 0
        assert result["mean"] == 0

    def test_calculate_metrics_single_value(self):
        """Tek değer metrik hesaplama"""
        from utils import calculate_metrics
        
        result = calculate_metrics([0.5])
        assert result["count"] == 1
        assert result["mean"] == 0.5
        assert result["std"] == 0


class TestLogAndHealthFunctions:
    """Log ve sağlık kontrolü testleri"""

    def test_log_request(self):
        """Request loglama testi"""
        from utils import log_request
        
        # Test that function doesn't crash
        try:
            log_request("/test", {"key": "value"}, 0.1)
            assert True
        except Exception:
            assert False, "log_request shouldn't raise exception"

    def test_health_check_database(self):
        """Database sağlık kontrolü"""
        from utils import health_check_database
        
        result = health_check_database()
        assert isinstance(result, bool)

    def test_health_check_external_api(self):
        """Harici API sağlık kontrolü"""
        from utils import health_check_external_api
        
        result = health_check_external_api()
        assert isinstance(result, bool)


class TestUtilsMainFunction:
    """Utils main fonksiyon testleri"""

    def test_utils_main_function(self):
        """Utils main fonksiyon testi"""
        from utils import test_utils
        
        # Test that main function runs without errors
        try:
            test_utils()
            assert True
        except Exception:
            assert False, "test_utils function should not raise exception"

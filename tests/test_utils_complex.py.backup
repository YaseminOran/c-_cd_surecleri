#!/usr/bin/env python3
"""
Utils Testleri - CI/CD Pipeline için
Utility fonksiyonlarını test eder
"""

import pytest
import sys
import os

# Src dizinini path'e ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils import (
    validate_input,
    is_valid_email,
    is_valid_name,
    format_response,
    sanitize_string,
    calculate_metrics,
    health_check_database,
    health_check_external_api
)

class TestInputValidation:
    """Input validation testleri"""
    
    def test_validate_input_valid_data(self):
        """Geçerli veri test et"""
        test_data = {
            'value': 50,
            'name': 'John Doe',
            'email': 'john@example.com'
        }
        
        result = validate_input(test_data)
        
        assert result['valid'] == True
        assert result['message'] == 'Veri doğrulaması başarılı'
    
    def test_validate_input_minimal_data(self):
        """Minimal veri test et"""
        test_data = {}
        
        result = validate_input(test_data)
        
        assert result['valid'] == True
    
    def test_validate_input_invalid_value_range(self):
        """Geçersiz value range test et"""
        test_data = {'value': 150}  # Out of range
        
        result = validate_input(test_data)
        
        assert result['valid'] == False
        assert '0-100 arasında' in result['message']
    
    def test_validate_input_invalid_value_type(self):
        """Geçersiz value tipi test et"""
        test_data = {'value': 'not a number'}
        
        result = validate_input(test_data)
        
        assert result['valid'] == False
        assert 'sayısal' in result['message']
    
    def test_validate_input_invalid_email(self):
        """Geçersiz email test et"""
        test_data = {'email': 'invalid-email'}
        
        result = validate_input(test_data)
        
        assert result['valid'] == False
        assert 'email' in result['message']
    
    def test_validate_input_invalid_name(self):
        """Geçersiz name test et"""
        test_data = {'name': 'x'}  # Too short
        
        result = validate_input(test_data)
        
        assert result['valid'] == False
        assert '2 karakter' in result['message']
    
    def test_validate_input_not_dict(self):
        """Dictionary olmayan veri test et"""
        result = validate_input("not a dict")
        
        assert result['valid'] == False
        assert 'dictionary' in result['message']

class TestEmailValidation:
    """Email validation testleri"""
    
    def test_valid_emails(self):
        """Geçerli email'leri test et"""
        valid_emails = [
            'test@example.com',
            'user.name@domain.co.uk',
            'test+label@gmail.com',
            'number123@test.org',
            'a@b.co'
        ]
        
        for email in valid_emails:
            assert is_valid_email(email) == True, f"Email should be valid: {email}"
    
    def test_invalid_emails(self):
        """Geçersiz email'leri test et"""
        invalid_emails = [
            'invalid-email',
            '@domain.com',
            'user@',
            'user@domain',
            'user name@domain.com',
            '',
            'user@domain.',
            'user..name@domain.com'
        ]
        
        for email in invalid_emails:
            assert is_valid_email(email) == False, f"Email should be invalid: {email}"
    
    def test_email_type_validation(self):
        """Email tip doğrulama test et"""
        assert is_valid_email(None) == False
        assert is_valid_email(123) == False
        assert is_valid_email([]) == False

class TestNameValidation:
    """Name validation testleri"""
    
    def test_valid_names(self):
        """Geçerli isimleri test et"""
        valid_names = [
            'John',
            'John Doe',
            'Mary Jane Smith',
            'Ali',
            'Jean-Pierre',
            'O\'Connor'
        ]
        
        for name in valid_names:
            assert is_valid_name(name) == True, f"Name should be valid: {name}"
    
    def test_invalid_names(self):
        """Geçersiz isimleri test et"""
        invalid_names = [
            '',
            ' ',
            'x',
            '  a  '  # Single character after strip
        ]
        
        for name in invalid_names:
            assert is_valid_name(name) == False, f"Name should be invalid: {name}"
    
    def test_name_type_validation(self):
        """Name tip doğrulama test et"""
        assert is_valid_name(None) == False
        assert is_valid_name(123) == False
        assert is_valid_name([]) == False

class TestResponseFormatting:
    """Response formatting testleri"""
    
    def test_format_response_complete(self):
        """Tam response formatting test et"""
        prediction_result = {
            'prediction': 0.75,
            'confidence': 0.85,
            'model_version': '1.0.0'
        }
        original_data = {'value': 60}
        
        result = format_response(prediction_result, original_data)
        
        assert result['prediction'] == 0.75
        assert result['confidence'] == 0.85
        assert result['model_version'] == '1.0.0'
        assert result['status'] == 'success'
        assert result['input_value'] == 60
        assert result['category'] == 'high'  # 0.75 >= 0.7
        assert 'timestamp' in result
    
    def test_format_response_categories(self):
        """Response kategorilerini test et"""
        test_cases = [
            (0.8, 'high'),
            (0.7, 'high'), 
            (0.6, 'medium'),
            (0.4, 'medium'),
            (0.3, 'low'),
            (0.0, 'low')
        ]
        
        for prediction_value, expected_category in test_cases:
            prediction_result = {
                'prediction': prediction_value,
                'confidence': 0.9,
                'model_version': '1.0.0'
            }
            original_data = {}
            
            result = format_response(prediction_result, original_data)
            assert result['category'] == expected_category
    
    def test_format_response_no_input_value(self):
        """Input value olmadan response formatting test et"""
        prediction_result = {
            'prediction': 0.5,
            'confidence': 0.8,
            'model_version': '1.0.0'
        }
        original_data = {}  # No 'value' key
        
        result = format_response(prediction_result, original_data)
        
        assert 'input_value' not in result
        assert result['category'] == 'medium'

class TestStringSanitization:
    """String sanitization testleri"""
    
    def test_sanitize_basic_html(self):
        """Basit HTML temizleme test et"""
        dirty_string = '<script>alert("xss")</script>Hello World'
        clean_string = sanitize_string(dirty_string)
        
        assert '<script>' not in clean_string
        assert 'Hello World' in clean_string
    
    def test_sanitize_special_characters(self):
        """Özel karakter temizleme test et"""
        dirty_string = 'Hello<>&"\' World'
        clean_string = sanitize_string(dirty_string)
        
        assert '<' not in clean_string
        assert '>' not in clean_string
        assert '"' not in clean_string
        assert "'" not in clean_string
        assert 'Hello& World' == clean_string
    
    def test_sanitize_whitespace(self):
        """Boşluk temizleme test et"""
        dirty_string = '  Hello    World    '
        clean_string = sanitize_string(dirty_string)
        
        assert clean_string == 'Hello World'
    
    def test_sanitize_length_limit(self):
        """Uzunluk sınırı test et"""
        long_string = 'a' * 200
        clean_string = sanitize_string(long_string, max_length=50)
        
        assert len(clean_string) <= 53  # 50 + "..."
        assert clean_string.endswith('...')
    
    def test_sanitize_invalid_input(self):
        """Geçersiz input test et"""
        assert sanitize_string(None) == ""
        assert sanitize_string(123) == ""
        assert sanitize_string([]) == ""

class TestMetricsCalculation:
    """Metrics calculation testleri"""
    
    def test_calculate_metrics_normal(self):
        """Normal metrik hesaplama test et"""
        predictions = [0.1, 0.5, 0.8, 0.3, 0.9]
        
        metrics = calculate_metrics(predictions)
        
        assert metrics['count'] == 5
        assert metrics['min'] == 0.1
        assert metrics['max'] == 0.9
        assert 0.4 <= metrics['mean'] <= 0.6  # Approximately 0.52
        assert metrics['std'] > 0
    
    def test_calculate_metrics_single_value(self):
        """Tek değer ile metrik hesaplama test et"""
        predictions = [0.5]
        
        metrics = calculate_metrics(predictions)
        
        assert metrics['count'] == 1
        assert metrics['min'] == 0.5
        assert metrics['max'] == 0.5
        assert metrics['mean'] == 0.5
        assert metrics['std'] == 0
    
    def test_calculate_metrics_empty_list(self):
        """Boş liste ile metrik hesaplama test et"""
        predictions = []
        
        metrics = calculate_metrics(predictions)
        
        assert metrics['count'] == 0
        assert metrics['min'] == 0
        assert metrics['max'] == 0
        assert metrics['mean'] == 0
        assert metrics['std'] == 0
    
    def test_calculate_metrics_identical_values(self):
        """Aynı değerler ile metrik hesaplama test et"""
        predictions = [0.5, 0.5, 0.5, 0.5]
        
        metrics = calculate_metrics(predictions)
        
        assert metrics['count'] == 4
        assert metrics['min'] == 0.5
        assert metrics['max'] == 0.5
        assert metrics['mean'] == 0.5
        assert metrics['std'] == 0

class TestHealthChecks:
    """Health check testleri"""
    
    def test_health_check_database(self):
        """Database health check test et"""
        # Test birden fazla kez çalıştır (random olduğu için)
        results = []
        for _ in range(10):
            result = health_check_database()
            results.append(result)
        
        # Çoğu True olmalı (%90 başarı oranı)
        true_count = sum(results)
        assert true_count >= 7  # En az %70 başarılı olmalı
    
    def test_health_check_external_api(self):
        """External API health check test et"""
        # Test birden fazla kez çalıştır
        results = []
        for _ in range(10):
            result = health_check_external_api()
            results.append(result)
        
        # Çoğu True olmalı (%95 başarı oranı)
        true_count = sum(results)
        assert true_count >= 8  # En az %80 başarılı olmalı

if __name__ == '__main__':
    # Testleri doğrudan çalıştır
    import subprocess
    import sys
    
    print("🧪 Utils testleri çalıştırılıyor...")
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
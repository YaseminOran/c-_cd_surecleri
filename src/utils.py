#!/usr/bin/env python3
"""
Yardımcı Fonksiyonlar - CI/CD Örneği
Input validasyon, response formatting ve diğer utility fonksiyonlar
"""

import re
from datetime import datetime
from typing import Dict, Any, Union
import logging

logger = logging.getLogger(__name__)

def validate_input(data: Dict[str, Any]) -> Dict[str, Union[bool, str]]:
    """
    Input verilerini doğrular
    
    Args:
        data: Doğrulanacak veri dictionary'si
        
    Returns:
        validation result: {'valid': bool, 'message': str}
    """
    if not isinstance(data, dict):
        return {
            'valid': False,
            'message': 'Veri dictionary formatında olmalı'
        }
    
    # Eğer 'value' varsa doğrula
    if 'value' in data:
        try:
            value = float(data['value'])
            if value < 0 or value > 100:
                return {
                    'valid': False,
                    'message': 'Value 0-100 arasında olmalı'
                }
        except (ValueError, TypeError):
            return {
                    'valid': False,
                    'message': 'Value sayısal bir değer olmalı'
                }
    
    # Email varsa doğrula (isteğe bağlı)
    if 'email' in data:
        if not is_valid_email(data['email']):
            return {
                'valid': False,
                'message': 'Geçersiz email formatı'
            }
    
    # Name varsa doğrula (isteğe bağlı)
    if 'name' in data:
        if not is_valid_name(data['name']):
            return {
                'valid': False,
                'message': 'Name en az 2 karakter olmalı'
            }
    
    return {
        'valid': True,
        'message': 'Veri doğrulaması başarılı'
    }

def is_valid_email(email: str) -> bool:
    """Email formatını kontrol eder"""
    if not isinstance(email, str):
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_name(name: str) -> bool:
    """İsim formatını kontrol eder"""
    if not isinstance(name, str):
        return False
    
    return len(name.strip()) >= 2

def format_response(prediction_result: Dict[str, Any], original_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    API response'unu formatlar
    
    Args:
        prediction_result: Model tahmin sonucu
        original_data: Orijinal input verisi
        
    Returns:
        Formatlanmış response
    """
    response = {
        'prediction': prediction_result.get('prediction'),
        'confidence': prediction_result.get('confidence'),
        'model_version': prediction_result.get('model_version'),
        'status': 'success',
        'timestamp': datetime.now().isoformat()
    }
    
    # Input verisinde 'value' varsa ekle
    if 'value' in original_data:
        response['input_value'] = original_data['value']
    
    # Tahmin kategorisini ekle
    prediction_value = prediction_result.get('prediction', 0)
    if prediction_value >= 0.7:
        response['category'] = 'high'
    elif prediction_value >= 0.4:
        response['category'] = 'medium'
    else:
        response['category'] = 'low'
    
    return response

def sanitize_string(text: str, max_length: int = 100) -> str:
    """
    String'i temizler ve güvenli hale getirir
    
    Args:
        text: Temizlenecek text
        max_length: Maksimum karakter sayısı
        
    Returns:
        Temizlenmiş text
    """
    if not isinstance(text, str):
        return ""
    
    # HTML taglerini kaldır
    text = re.sub(r'<[^>]+>', '', text)
    
    # Özel karakterleri temizle
    text = re.sub(r'[<>"\']', '', text)
    
    # Fazla boşlukları temizle
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Uzunluk sınırla
    if len(text) > max_length:
        text = text[:max_length] + "..."
    
    return text

def calculate_metrics(predictions: list) -> Dict[str, float]:
    """
    Tahmin listesinden metrikleri hesaplar
    
    Args:
        predictions: Tahmin değerleri listesi
        
    Returns:
        Hesaplanmış metrikler
    """
    if not predictions:
        return {
            'count': 0,
            'mean': 0,
            'min': 0,
            'max': 0,
            'std': 0
        }
    
    import statistics
    
    return {
        'count': len(predictions),
        'mean': round(statistics.mean(predictions), 4),
        'min': min(predictions),
        'max': max(predictions),
        'std': round(statistics.stdev(predictions) if len(predictions) > 1 else 0, 4)
    }

def log_request(endpoint: str, data: Dict[str, Any], response_time: float):
    """
    Request'i loglar
    
    Args:
        endpoint: API endpoint
        data: Request data
        response_time: Response süresi (ms)
    """
    log_data = {
        'endpoint': endpoint,
        'timestamp': datetime.now().isoformat(),
        'response_time_ms': round(response_time * 1000, 2),
        'data_keys': list(data.keys()) if data else []
    }
    
    logger.info(f"Request logged: {log_data}")

def health_check_database():
    """
    Database sağlık kontrolü (simülasyon)
    
    Returns:
        bool: Database sağlık durumu
    """
    # Gerçek uygulamada database connection test edilir
    import random
    return random.random() > 0.1  # %90 başarı oranı

def health_check_external_api():
    """
    Harici API sağlık kontrolü (simülasyon)
    
    Returns:
        bool: Harici API sağlık durumu  
    """
    # Gerçek uygulamada harici API'ye request atılır
    import random
    return random.random() > 0.05  # %95 başarı oranı

# Test fonksiyonları
def test_utils():
    """Utility fonksiyonlarını test et"""
    print("🧪 Utils test ediliyor...")
    
    # Test 1: Input validation
    valid_data = {'value': 50, 'name': 'Test User'}
    result = validate_input(valid_data)
    print(f"✅ Test 1 - Valid input: {result}")
    
    invalid_data = {'value': 150}  # Out of range
    result = validate_input(invalid_data)
    print(f"✅ Test 2 - Invalid input: {result}")
    
    # Test 2: Email validation
    print(f"✅ Test 3 - Valid email: {is_valid_email('test@example.com')}")
    print(f"✅ Test 4 - Invalid email: {is_valid_email('invalid-email')}")
    
    # Test 3: Response formatting
    prediction = {'prediction': 0.85, 'confidence': 0.92, 'model_version': '1.0'}
    original = {'value': 75}
    formatted = format_response(prediction, original)
    print(f"✅ Test 5 - Response format: {formatted}")
    
    # Test 4: String sanitization
    dirty_string = '<script>alert("xss")</script>Normal text here with extra   spaces'
    clean_string = sanitize_string(dirty_string)
    print(f"✅ Test 6 - String sanitization: '{clean_string}'")
    
    # Test 5: Metrics calculation
    test_predictions = [0.1, 0.5, 0.8, 0.3, 0.9]
    metrics = calculate_metrics(test_predictions)
    print(f"✅ Test 7 - Metrics: {metrics}")
    
    print("🎉 Utils testleri tamamlandı!")

if __name__ == '__main__':
    test_utils()
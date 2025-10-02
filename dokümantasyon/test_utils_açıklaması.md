# test_utils.py Açıklaması

## Dosya Amacı
Bu dosya utility fonksiyonlarını test eder. Input validasyon ve response formatlama gibi yardımcı fonksiyonların doğru çalıştığını garanti eder.

## İçe Aktarmalar (Imports)
```python
import os
import sys

# Src dizinini path'e ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from utils import validate_input, format_response
```

- **os, sys**: Python path ayarları için
- **validate_input**: Input doğrulama fonksiyonu
- **format_response**: Response formatlama fonksiyonu

## Test Sınıfı 1: TestInputValidation

Bu sınıf `validate_input` fonksiyonunu test eder.

### 1. test_validate_input_valid_data
```python
def test_validate_input_valid_data(self):
    valid_data = {"value": 50}
    
    result = validate_input(valid_data)
    
    assert result["valid"] is True
    assert "message" in result
```

**Test eder:** Geçerli veri validasyonu
**Kontrol eder:**
- Geçerli veri için `valid: True` dönüyor mu?
- Response'da message alanı var mı?

**Test verisi:** `{"value": 50}` - Orta aralık değer

### 2. test_validate_input_invalid_data
```python
def test_validate_input_invalid_data(self):
    invalid_data = {"value": 150}  # Range dışı değer
    
    result = validate_input(invalid_data)
    
    assert result["valid"] is False
    assert "message" in result
```

**Test eder:** Geçersiz veri validasyonu
**Kontrol eder:**
- Range dışı değer için `valid: False` dönüyor mu?
- Hata mesajı dahil ediliyor mu?

**Test verisi:** `{"value": 150}` - Kabul edilebilir aralığın üstünde

### 3. test_validate_input_empty_data
```python
def test_validate_input_empty_data(self):
    empty_data = {}  # Boş dict aslında valid
    
    result = validate_input(empty_data)
    
    assert result["valid"] is True  # Boş dict valid
    assert "message" in result
```

**Test eder:** Boş veri validasyonu
**Önemli not:** Bu implementasyonda boş dict geçerli kabul ediliyor
**Business logic:** Default değerler kullanılabilir

### 4. test_validate_input_none_data
```python
def test_validate_input_none_data(self):
    result = validate_input(None)
    
    assert result["valid"] is False
    assert "message" in result
```

**Test eder:** None veri validasyonu
**Kontrol eder:** Null değerler doğru şekilde reddediliyor mu?

## Test Sınıfı 2: TestResponseFormatting

Bu sınıf `format_response` fonksiyonunu test eder.

### 1. test_format_response_basic
```python
def test_format_response_basic(self):
    prediction_result = {
        "prediction": 0.75,
        "confidence": 0.9,
        "model_version": "1.0",
    }
    input_data = {"value": 60}
    
    result = format_response(prediction_result, input_data)
    
    assert "prediction" in result
    assert "status" in result
    assert result["status"] == "success"
    assert result["prediction"] == 0.75
```

**Test eder:** Temel response formatlama
**Kontrol eder:**
- Tüm gerekli alanlar mevcut mu?
- Prediction değeri doğru aktarılıyor mu?
- Status success olarak set ediliyor mu?

### 2. test_format_response_low_prediction
```python
def test_format_response_low_prediction(self):
    prediction_result = {
        "prediction": 0.2,
        "confidence": 0.8,
        "model_version": "1.0",
    }
    input_data = {"value": 20}
    
    result = format_response(prediction_result, input_data)
    
    assert result["prediction"] == 0.2
    assert result["status"] == "success"
```

**Test eder:** Düşük tahmin değerleri için formatlama
**Edge case:** Çok düşük prediction değerleri

### 3. test_format_response_high_prediction
```python
def test_format_response_high_prediction(self):
    prediction_result = {
        "prediction": 0.9,
        "confidence": 0.95,
        "model_version": "1.0",
    }
    input_data = {"value": 90}
    
    result = format_response(prediction_result, input_data)
    
    assert result["prediction"] == 0.9
    assert result["status"] == "success"
```

**Test eder:** Yüksek tahmin değerleri için formatlama
**Edge case:** Çok yüksek prediction değerleri

### 4. test_format_response_contains_timestamp
```python
def test_format_response_contains_timestamp(self):
    prediction_result = {
        "prediction": 0.5,
        "confidence": 0.8,
        "model_version": "1.0",
    }
    input_data = {"value": 50}
    
    result = format_response(prediction_result, input_data)
    
    assert "timestamp" in result
    assert result["timestamp"] is not None
```

**Test eder:** Timestamp ekleme
**Kontrol eder:**
- Her response'da timestamp var mı?
- Timestamp null değil mi?

**Neden önemli:** Audit trail ve debugging için

## Test Kategorileri

### Input Validation Tests
- **Valid cases**: Normal, kabul edilebilir veriler
- **Invalid cases**: Range dışı, tip uyumsuzluğu
- **Edge cases**: Boş, null, eksik değerler
- **Boundary cases**: Min/max değerler

### Response Formatting Tests
- **Structure tests**: Gerekli alanların varlığı
- **Value tests**: Değerlerin doğru aktarımı
- **Metadata tests**: Timestamp, status gibi ekstra bilgiler
- **Edge cases**: Farklı prediction aralıkları

## CI/CD'deki Önemi

### Input Validation
- **Security**: Kötü niyetli girişleri engeller
- **Stability**: Hatalı verilerle çökmeyi önler
- **User Experience**: Anlamlı hata mesajları

### Response Formatting
- **API Contract**: Tutarlı response formatı
- **Client Integration**: Frontend beklentilerini karşılar
- **Monitoring**: Timestamp ile audit trail

## Öğrenci İçin Önemli Noktalar

### Test Design Principles
1. **Positive testing**: İyi akış testleri
2. **Negative testing**: Hata durumu testleri
3. **Edge case testing**: Sınır değer testleri
4. **Boundary testing**: Min/max değer testleri

### Utility Function Testing
- **Pure functions** test etmesi kolay
- **Input/output** odaklı testler
- **Side effect'ler** minimize edilmeli
- **Deterministic** sonuçlar beklenmeli

### Real-World Considerations
- **Security validation** mutlaka test edilmeli
- **Performance** kritik fonksiyonlar için önemli
- **Error handling** her edge case için
- **Logging** test edilebilir olmalı
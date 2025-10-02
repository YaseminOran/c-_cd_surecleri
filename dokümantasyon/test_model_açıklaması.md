# test_model.py Açıklaması

## Dosya Amacı
Bu dosya `SimpleModel` sınıfının tüm fonksiyonlarını test eder. Model'in doğru çalıştığından ve beklenen sonuçları verdiğinden emin olmak için kullanılır.

## İçe Aktarmalar (Imports)
```python
import os
import sys

# Src dizinini path'e ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from model import SimpleModel
```

- **os, sys**: Python path ayarları için
- **SimpleModel**: Test edilecek model sınıfı

## Test Sınıfı: TestSimpleModel

### 1. test_model_creation
```python
def test_model_creation(self):
    model = SimpleModel()
    assert model is not None
```

**Test eder:** Model oluşturma
**Kontrol eder:** Model başarıyla oluşturuluyor mu?
**Neden önemli:** Model'in constructor'ında hata olmadığını garanti eder.

### 2. test_model_predict_basic
```python
def test_model_predict_basic(self):
    model = SimpleModel()
    test_data = {"value": 50}
    
    result = model.predict(test_data)
    
    assert result is not None
    assert isinstance(result, dict)  # Model dict döndürüyor
    assert "prediction" in result
    assert 0 <= result["prediction"] <= 1
```

**Test eder:** Temel tahmin fonksiyonalitesi
**Kontrol eder:**
- Model tahmin yapabiliyor mu?
- Sonuç dict formatında mı?
- Prediction değeri 0-1 arasında mı?

**Önemli:** Bu test model'in ana fonksiyonunu doğrular.

### 3. test_model_predict_low_value
```python
def test_model_predict_low_value(self):
    model = SimpleModel()
    test_data = {"value": 10}
    
    result = model.predict(test_data)
    
    assert result is not None
    assert isinstance(result, dict)
    assert "prediction" in result
```

**Test eder:** Düşük değerler için tahmin
**Neden gerekli:** Edge case'leri test etmek için
**Kontrol eder:** Düşük input değerleri model'i bozmuyor mu?

### 4. test_model_predict_high_value
```python
def test_model_predict_high_value(self):
    model = SimpleModel()
    test_data = {"value": 90}
    
    result = model.predict(test_data)
    
    assert result is not None
    assert isinstance(result, dict)
    assert "prediction" in result
```

**Test eder:** Yüksek değerler için tahmin
**Neden gerekli:** Edge case'leri test etmek için
**Kontrol eder:** Yüksek input değerleri model'i bozmuyor mu?

### 5. test_model_health_check
```python
def test_model_health_check(self):
    model = SimpleModel()
    
    health = model.is_healthy()
    
    assert isinstance(health, bool)
```

**Test eder:** Model sağlık durumu
**Kontrol eder:** Model kendini sağlıklı olarak rapor edebiliyor mu?
**CI/CD'de kullanımı:** Deployment öncesi model durumunu kontrol etmek için

### 6. test_model_version
```python
def test_model_version(self):
    model = SimpleModel()
    
    version = model.get_version()
    
    assert version is not None
    assert isinstance(version, str)
```

**Test eder:** Model versiyonu
**Kontrol eder:**
- Model versiyon bilgisi dönebiliyor mu?
- Versiyon string formatında mı?

**Neden önemli:** Model versiyonlama için kritik

### 7. test_model_prediction_count
```python
def test_model_prediction_count(self):
    model = SimpleModel()
    
    # İlk sayım
    initial_count = model.get_prediction_count()
    
    # Bir tahmin yap
    model.predict({"value": 50})
    
    # Sayımın arttığını kontrol et
    new_count = model.get_prediction_count()
    assert new_count >= initial_count
```

**Test eder:** Tahmin sayısı takibi
**Kontrol eder:**
- Model kaç tahmin yaptığını sayabiliyor mu?
- Her tahmin sonrası sayaç artıyor mu?

**Monitoring için önemli:** Production'da model kullanım istatistikleri için

## Test Stratejisi Açıklaması

### Edge Case Testing
- **Düşük değerler** (test_model_predict_low_value)
- **Yüksek değerler** (test_model_predict_high_value)
- **Normal değerler** (test_model_predict_basic)

### Functional Testing
- **Temel işlevsellik** (predict, health_check)
- **Metadata** (version, prediction_count)
- **Object creation** (model_creation)

### Data Validation
- **Return type kontrolü** (dict, bool, str)
- **Required fields** (prediction field)
- **Value ranges** (0-1 arası prediction)

## CI/CD Pipeline'daki Rolü
Bu testler:
1. **Model regression** hatalarını yakalar
2. **API contract** değişikliklerini detect eder
3. **Performance** problemlerini erken yakalar
4. **Version compatibility** sağlar

## Öğrenci İçin Önemli Noktalar
- **Model testleri** API testlerinden farklıdır
- **Edge case'ler** mutlaka test edilmelidir
- **Return type** kontrolü kritiktir
- **Business logic** doğrulaması gereklidir
- **Stateful** davranışlar (counter) test edilmelidir
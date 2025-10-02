# test_app.py Açıklaması

## Dosya Amacı
Bu dosya Flask web uygulamasının tüm endpoint'lerini test eder. CI/CD pipeline'ında uygulamanın doğru çalıştığından emin olmak için kullanılır.

## İçe Aktarmalar (Imports)
```python
import json
import os
import sys
import pytest

# Src dizinini path'e ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from app import app
```

- **json**: API endpoint'lerine JSON veri göndermek için
- **os, sys**: Python path ayarları için
- **pytest**: Test framework'ü
- **app**: Test edilecek Flask uygulaması

## Test Fixture
```python
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            yield client
```

**Ne yapar?** Her test için temiz bir Flask test client'ı oluşturur. Bu sayede testler birbirini etkilemez.

## Test Sınıfı: TestBasicEndpoints

### 1. test_home_endpoint
```python
def test_home_endpoint(self, client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["service"] == "CI/CD Example API"
    assert data["version"] == "1.0.0"
    assert data["status"] == "running"
```

**Test eder:** Ana sayfa endpoint'i (`/`)
**Kontrol eder:** 
- HTTP 200 status code döndürüyor mu?
- JSON response doğru bilgileri içeriyor mu?

### 2. test_health_endpoint
```python
def test_health_endpoint(self, client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] in ["healthy", "unhealthy"]
    assert "model_loaded" in data
```

**Test eder:** Sağlık kontrol endpoint'i (`/health`)
**Kontrol eder:**
- Uygulamanın sağlıklı çalıştığını
- Model'in yüklendiğini

### 3. test_predict_endpoint_valid
```python
def test_predict_endpoint_valid(self, client):
    test_data = {"value": 50}
    response = client.post(
        "/predict", data=json.dumps(test_data), content_type="application/json"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "prediction" in data
    assert "status" in data
    assert data["status"] == "success"
```

**Test eder:** Geçerli veri ile prediction endpoint'i
**Kontrol eder:**
- Geçerli veri gönderildiğinde başarılı response alınıyor mu?
- Response'da prediction ve status alanları var mı?

### 4. test_predict_endpoint_invalid
```python
def test_predict_endpoint_invalid(self, client):
    test_data = {"value": 150}  # Range dışı değer
    response = client.post(
        "/predict", data=json.dumps(test_data), content_type="application/json"
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
```

**Test eder:** Geçersiz veri ile prediction endpoint'i
**Kontrol eder:**
- Geçersiz veri gönderildiğinde hata alınıyor mu? (HTTP 400)
- Error status döndürülüyor mu?

### 5. test_metrics_endpoint
```python
def test_metrics_endpoint(self, client):
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.get_json()
    assert "total_predictions" in data
    assert "uptime_seconds" in data
```

**Test eder:** Metrik endpoint'i (`/metrics`)
**Kontrol eder:**
- Uygulama istatistiklerinin döndürülüyor mu?
- Gerekli metrik alanları mevcut mu?

### 6. test_404_endpoint
```python
def test_404_endpoint(self, client):
    response = client.get("/nonexistent")
    assert response.status_code == 404
    data = response.get_json()
    assert data["status"] == "error"
```

**Test eder:** Olmayan endpoint
**Kontrol eder:**
- Var olmayan URL'ler için 404 hatası dönüyor mu?

## CI/CD'deki Rolü
Bu testler CI pipeline'ında çalışarak:
1. **Kod kalitesini** garanti eder
2. **API contract'larının** doğru çalıştığını kontrol eder
3. **Regression** hatalarını yakalar
4. **Deployment öncesi** güvenlik sağlar

## Öğrenci İçin Önemli Noktalar
- Her endpoint için ayrı test yazılmalı
- Hem **başarılı** hem **başarısız** senaryolar test edilmeli
- Test verileri **gerçekçi** olmalı
- Assert'ler **spesifik** olmalı (sadece status code değil, content da)
# 🔄 Sürekli Entegrasyon ve Sürekli Dağıtım (CI/CD)

Bu proje, ML projelerinde CI/CD (Continuous Integration/Continuous Deployment) süreçlerini basit ve anlaşılır şekilde öğretir.

## 🎯 Ne Öğreneceğiniz?

1. **CI (Sürekli Entegrasyon)** - Kod değişikliklerini otomatik test etme
2. **CD (Sürekli Dağıtım)** - Başarılı testleri otomatik deploy etme
3. **GitHub Actions** - Ücretsiz CI/CD platformu kullanımı
4. **Otomatik Testler** - Her kod değişikliğinde test çalıştırma
5. **Docker Deployment** - Konteyner tabanlı dağıtım

## 📁 Proje Yapısı

```
ornek_6/
├── .github/
│   └── workflows/
│       ├── ci.yml              # Sürekli entegrasyon
│       ├── cd.yml              # Sürekli dağıtım
│       └── test.yml            # Test workflow'u
├── src/
│   ├── app.py                  # Ana uygulama
│   ├── model.py                # ML model
│   └── utils.py                # Yardımcı fonksiyonlar
├── tests/
│   ├── test_app.py             # Uygulama testleri
│   ├── test_model.py           # Model testleri
│   └── test_utils.py           # Utility testleri
├── scripts/
│   ├── deploy.sh               # Deployment scripti
│   ├── test.sh                 # Test scripti
│   └── build.sh                # Build scripti
├── config/
│   ├── requirements.txt        # Python bağımlılıkları
│   └── requirements-dev.txt    # Development bağımlılıkları
├── Dockerfile                  # Docker image tanımı
├── docker-compose.yml          # Local development
└── README.md                   # Bu dosya
```

## 🚀 Hızlı Başlangıç

### 1. Yerel Geliştirme
```bash
cd ornek_6

# Sanal ortam oluştur
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Bağımlılıkları yükle
pip install -r config/requirements-dev.txt

# Uygulamayı çalıştır
python src/app.py
```

### 2. Testleri Çalıştır
```bash
# Tüm testler
python -m pytest tests/

# Coverage ile
python -m pytest tests/ --cov=src/
```

### 3. Docker ile Çalıştır
```bash
# Build
docker build -t cicd-example .

# Run
docker run -p 5000:5000 cicd-example
```

## 🔄 CI/CD Pipeline

### Sürekli Entegrasyon (CI)
Her kod push'unda otomatik olarak:
1. ✅ Kod syntax kontrolü
2. ✅ Unit testler çalışır
3. ✅ Code coverage hesaplanır
4. ✅ Security scan yapılır
5. ✅ Docker image build edilir

### Sürekli Dağıtım (CD)
Main branch'e merge olduktan sonra:
1. 🚀 Production build oluşturulur
2. 🚀 Docker image registry'ye push edilir
3. 🚀 Staging ortamına deploy edilir
4. 🚀 Integration testler çalışır
5. 🚀 Production'a otomatik deploy

## 📋 Adım Adım Rehber

### Adım 1: GitHub Repository Oluşturma
1. GitHub'da yeni repository oluşturun
2. Bu kodları push edin
3. Settings > Actions > Allow actions seçin

### Adım 2: Secrets Ekleme
Repository Settings > Secrets and Variables > Actions:
```
DOCKER_USERNAME: Docker Hub kullanıcı adı
DOCKER_PASSWORD: Docker Hub şifresi
DEPLOY_KEY: Deployment için SSH key
```

### Adım 3: İlk Pipeline Çalıştırma
```bash
# Kod değişikliği yap
echo "# Test" >> README.md

# Commit ve push
git add .
git commit -m "Test CI/CD pipeline"
git push origin main
```

### Adım 4: Pipeline Durumunu İzleme
- GitHub > Actions sekmesinde pipeline durumunu görün
- Her adımın loglarını inceleyin
- Hataları debug edin

## 🧪 Test Stratejisi

### Unit Testler
```python
# test_model.py
def test_model_prediction():
    model = load_model()
    result = model.predict(sample_data)
    assert result is not None
    assert 0 <= result <= 1
```

### Integration Testler
```python
# test_app.py
def test_api_endpoint():
    response = client.post('/predict', json=test_data)
    assert response.status_code == 200
    assert 'prediction' in response.json()
```

### End-to-End Testler
```bash
# Gerçek API'yi test et
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"data": "test"}'
```

## 🔧 Pipeline Konfigürasyonu

### GitHub Actions Workflow
```yaml
name: CI/CD Pipeline
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v3
      - name: Run tests
        run: |
          pip install -r config/requirements-dev.txt
          python -m pytest tests/
```

## 📊 Monitoring ve Alerting

### Pipeline Metrikleri
- ✅ Test başarı oranı
- ⏱️ Pipeline çalışma süresi
- 🐛 Hata sayısı
- 📈 Deployment sıklığı

### Alerting
- ❌ Pipeline başarısız olursa Slack/email bildirimi
- 🚨 Production'da hata olursa anında uyarı
- 📱 Deployment tamamlandığında bilgilendirme

## 🛠️ En İyi Pratikler

### Kod Kalitesi
- ✅ Pre-commit hooks kullanın
- ✅ Code review zorunlu tutun
- ✅ Test coverage %80+ tutun
- ✅ Linting ve formatting otomatik

### Security
- 🔒 Secrets'ları asla kod içinde tutmayın
- 🔒 Dependency scan'leri düzenli yapın
- 🔒 Container security scan'leri ekleyin
- 🔒 HTTPS kullanın

### Performance
- ⚡ Pipeline'ı hızlı tutun (<10 dakika)
- ⚡ Paralel işlemler kullanın
- ⚡ Cache'leme stratejileri uygulayın
- ⚡ Gereksiz adımları kaldırın

## 🎓 Alıştırmalar

### Başlangıç Seviyesi
1. Basit bir test ekleyin
2. Pipeline'ı çalıştırıp sonucu görün
3. Kasıtlı hata yapıp pipeline'ın durmasını sağlayın

### Orta Seviye
1. Branch protection kuralları ekleyin
2. Pull request için ayrı pipeline oluşturun
3. Staging ve production ortamları ayırın

### İleri Seviye
1. Blue-green deployment uygulayın
2. Canary release stratejisi ekleyin
3. Monitoring ve alerting sistemi kurun

---

**🎯 Bu örnek ile modern software development'ta vazgeçilmez olan CI/CD süreçlerini öğreneceksiniz!**
# Test

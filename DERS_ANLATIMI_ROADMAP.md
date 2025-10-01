# 🎯 MLOps CI/CD Ders Anlatımı - Detaylı Roadmap

## 📋 Ders Süresi: 90 Dakika

---

## 🔥 **AÇILIŞ: Problem Senaryosu (10 dk)**

### **Anlatım:** 
> "Diyelim ki 5 kişilik bir geliştirici ekibiniz var. Günde 20 kod değişikliği yapıyorsunuz. Her birini manuel test etmek, deploy etmek ne kadar sürer? Hata yapma olasılığı nedir?"

### **Demo Kodu:**
```bash
# Kaç adet commit var?
git log --oneline | wc -l

# Son 5 commit'i göster
git log --oneline -5
```

### **Öğrencilere Sorular:**
- Manuel deployment ne kadar sürer?
- Günde 20 değişiklik × 5 dakika test = ?
- Hata yapma riski nedir?
- Gece deployment'ı kim yapacak?

---

## 🎬 **BÖLÜM 1: Manual Process'in Sorunları (15 dk)**

### **Adım 1.1: Uygulamayı Başlat**
```bash
cd /Users/yaseminarslan/Desktop/mlops/ornek_6
source venv_clean/bin/activate
python src/app.py
```

**Açıklama:** "Şu anda uygulamayı manuel başlattık. Production'da bunu kim yapacak?"

### **Adım 1.2: Manuel Test Senaryosu**

#### **Terminal 1: Uygulama çalışıyor**
#### **Terminal 2: Manuel testler**

```bash
# ✅ Ana sayfa çalışıyor mu?
curl http://localhost:5000/
```

**Beklenen Çıktı:**
```json
{
  "service": "CI/CD Example API",
  "version": "1.0.0",
  "status": "running",
  "endpoints": {
    "GET /": "API bilgileri",
    "GET /health": "Sağlık kontrolü", 
    "POST /predict": "ML tahmin",
    "GET /metrics": "API metrikleri"
  },
  "timestamp": "2024-10-01T..."
}
```

```bash
# ✅ Health check çalışıyor mu?
curl http://localhost:5000/health
```

**Beklenen Çıktı:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2024-10-01T...",
  "version": "1.0.0"
}
```

```bash
# ✅ Prediction çalışıyor mu?
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"feature1": 1.5, "feature2": 2.0}'
```

```bash
# ❌ Hatalı input ne yapıyor?
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"invalid": "data"}'
```

```bash
# 📊 Metrikleri kontrol et
curl http://localhost:5000/metrics
```

### **Soru Öğrencilere:** 
"Her kod değişikliğinde bunları tek tek test edecek misiniz?"

### **Problemler:**
- ⏱️ Zaman kaybı
- 🐛 İnsan hatası riski
- 🌙 24/7 availability sorunu
- 👥 Ekip koordinasyonu
- 📈 Scalability sorunu

---

## 🧪 **BÖLÜM 2: Otomatik Test'lerin Gücü (20 dk)**

### **Adım 2.1: Mevcut Test Durumunu Göster**
```bash
# Testleri çalıştır
python -m pytest tests/ -v

# Hangi testler başarısız?
python -m pytest tests/ -v --tb=short

# Sadece başarısız testleri göster
python -m pytest tests/ -v --tb=line | grep FAILED
```

**Açıklama:** "Gördüğünüz gibi 3 test başarısız. Production'a böyle bir kod gönderir misiniz?"

### **Adım 2.2: Test Türlerini Açıkla**

#### **Unit Test Örneği:**
```bash
# Sadece model testleri
python -m pytest tests/test_model.py -v
```

**Test Türleri Açıklaması:**
- **Unit Tests**: Tek bir fonksiyon/class test eder
- **Integration Tests**: Sistemin parçalarının birlikte çalışmasını test eder  
- **End-to-End Tests**: Kullanıcı senaryolarını test eder

#### **Integration Test Örneği:**
```bash
# API endpoint testleri
python -m pytest tests/test_app.py -v
```

#### **Test Coverage:**
```bash
# Coverage ile çalıştır (eğer yüklü ise)
python -m pytest tests/ --cov=src/ --cov-report=term-missing
```

### **Test Stratejisi Piramidi:**
```
    🔺 E2E Tests (Az, Yavaş, Pahalı)
   🔺🔺 Integration Tests (Orta)
  🔺🔺🔺 Unit Tests (Çok, Hızlı, Ucuz)
```

---

## ⚙️ **BÖLÜM 3: CI/CD Pipeline Anatomisi (20 dk)**

### **Adım 3.1: GitHub Actions Workflow'unu İncele**

```bash
# CI workflow'u göster
cat .github/workflows/ci.yml
```

```bash
# Test workflow'u göster  
cat .github/workflows/test.yml
```

```bash
# CD workflow'u göster
cat .github/workflows/cd.yml
```

### **Adım 3.2: Pipeline Adımlarını Açıkla**

#### **CI (Continuous Integration) Adımları:**

##### **1. Syntax Check:**
```bash
# Python syntax kontrolü
python -m py_compile src/*.py
```

##### **2. Linting:**
```bash
# Code quality check (eğer flake8 yüklü ise)
python -m flake8 src/ --count --statistics
```

##### **3. Security Scan:**
```bash
# Güvenlik taraması (eğer bandit yüklü ise)
python -m bandit -r src/
```

##### **4. Dependency Check:**
```bash
# Güvenlik açığı taraması (eğer safety yüklü ise)
python -m safety check
```

#### **CD (Continuous Deployment) Adımları:**
1. **Build**: Docker image oluştur
2. **Test**: Staging ortamında test et
3. **Deploy**: Production'a deploy et
4. **Monitor**: Sağlık kontrolü yap

### **Pipeline Görselleştirmesi:**
```
Code Push → CI Pipeline → CD Pipeline → Production
    ↓           ↓            ↓           ↓
  Trigger   Test/Build   Deploy/Test   Monitor
```

---

## 🚀 **BÖLÜM 4: Live CI/CD Demo (20 dk)**

### **Adım 4.1: Git Repository Hazırlığı**
```bash
# Git durumunu kontrol et
git status

# Temiz working directory olduğundan emin ol
git stash # (eğer değişiklik varsa)

# Yeni feature branch oluştur
git checkout -b "feature/fix-tests"
```

### **Adım 4.2: Kasıtlı Hata Oluştur**
```bash
# Bir test dosyasında kasıtlı hata yap
echo "def test_broken(): 
    assert False, 'Bu test kasıtlı olarak başarısız'" >> tests/test_demo.py

# Değişiklikleri kontrol et
git diff

# Commit et
git add tests/test_demo.py
git commit -m "Add broken test - CI should fail"
```

### **Adım 4.3: GitHub'a Push ve Pipeline İzleme**
```bash
# Push et
git push origin feature/fix-tests

# GitHub'da şu adımları göster:
# 1. Repository → Actions sekmesi
# 2. Pipeline'ın başladığını göster
# 3. ❌ Testlerin başarısız olduğunu göster
# 4. ❌ Pipeline'ın durduğunu göster
```

**Açıklama:** "İşte CI/CD'nin gücü! Hatalı kod production'a ulaşamadı."

### **Adım 4.4: Hatayı Düzelt**
```bash
# Hatalı testi düzelt
cat > tests/test_demo.py << 'EOF'
def test_fixed():
    """Bu test başarılı olmalı"""
    assert True, 'Test başarılı'

def test_basic_math():
    """Temel matematik testi"""
    assert 2 + 2 == 4
EOF

# Değişiklikleri kontrol et
git diff

# Commit et
git add tests/test_demo.py
git commit -m "Fix broken test - CI should pass"
git push origin feature/fix-tests
```

### **Adım 4.5: Başarılı Pipeline'ı İzle**
```bash
# GitHub Actions'da şu adımları göster:
# 1. ✅ Testlerin başarılı olduğunu göster
# 2. ✅ Pipeline'ın tamamlandığını göster
# 3. ✅ Deploy'un hazır olduğunu göster
```

---

## 🔧 **BÖLÜM 5: Docker ile Deployment (10 dk)**

### **Adım 5.1: Dockerfile İnceleme**
```bash
# Dockerfile'ı göster
cat Dockerfile
```

### **Adım 5.2: Docker Build**
```bash
# Docker image oluştur
docker build -t cicd-demo .

# Build process'ini açıkla:
# 1. Base image yükle
# 2. Dependencies kur
# 3. Kodu kopyala
# 4. Expose port
# 5. Run komutu tanımla

# Image'ları listele
docker images | grep cicd-demo
```

### **Adım 5.3: Docker Run**
```bash
# Container çalıştır
docker run -d -p 8080:5000 --name cicd-container cicd-demo

# Container durumunu kontrol et
docker ps | grep cicd-container

# Çalışıyor mu kontrol et
curl http://localhost:8080/health

# Logs'ları göster
docker logs cicd-container
```

### **Adım 5.4: Production Simülasyonu**
```bash
# Health check
curl http://localhost:8080/health

# Metrics check
curl http://localhost:8080/metrics

# Load test (basit)
for i in {1..5}; do
  curl -s http://localhost:8080/ > /dev/null && echo "Request $i: OK"
  sleep 1
done

# Container'ı durdur
docker stop cicd-container
docker rm cicd-container
```

**Açıklama:** "Production'da bu tüm adımlar otomatik olacak!"

### **Container Lifecycle:**
```
Build → Test → Push → Deploy → Monitor → Scale
```

---

## 🎓 **BÖLÜM 6: Öğrenci Hands-on Egzersizleri (10 dk)**

### **Egzersiz 1: Basit Test Ekleme**
```bash
# Yeni test dosyası oluştur
cat > tests/test_student.py << 'EOF'
def test_basic_math():
    """Temel matematik işlemleri"""
    assert 2 + 2 == 4
    assert 10 - 5 == 5
    assert 3 * 4 == 12

def test_string_operations():
    """String işlemleri"""
    assert "hello".upper() == "HELLO"
    assert "WORLD".lower() == "world"
    assert "Python".startswith("Py")

def test_list_operations():
    """Liste işlemleri"""
    test_list = [1, 2, 3]
    assert len(test_list) == 3
    assert 2 in test_list
    assert max(test_list) == 3
EOF

# Test et
python -m pytest tests/test_student.py -v
```

### **Egzersiz 2: API Test Ekleme**
```bash
# API test ekle
cat >> tests/test_student.py << 'EOF'

import requests
import json

def test_api_home_endpoint():
    """Ana sayfa endpoint testi"""
    try:
        response = requests.get('http://localhost:5000/')
        assert response.status_code == 200
        data = response.json()
        assert 'service' in data
        assert data['service'] == 'CI/CD Example API'
    except requests.exceptions.ConnectionError:
        # Uygulama çalışmıyorsa test'i skip et
        pass

def test_api_health_endpoint():
    """Health check endpoint testi"""
    try:
        response = requests.get('http://localhost:5000/health')
        assert response.status_code == 200
        data = response.json()
        assert 'status' in data
        assert data['status'] in ['healthy', 'unhealthy']
    except requests.exceptions.ConnectionError:
        pass
EOF

# Test et (uygulama çalışıyorsa)
python -m pytest tests/test_student.py::test_api_home_endpoint -v
```

### **Egzersiz 3: Monitoring Script**
```bash
# Monitoring scripti oluştur
cat > scripts/monitor.sh << 'EOF'
#!/bin/bash

echo "🔍 CI/CD Demo - Health Check Monitor"
echo "======================================"

# Health Check
echo -e "\n📊 Health Status:"
if curl -s http://localhost:5000/health > /dev/null; then
    curl -s http://localhost:5000/health | python3 -m json.tool
else
    echo "❌ Service is not running on localhost:5000"
fi

# Metrics
echo -e "\n📈 Metrics:"
if curl -s http://localhost:5000/metrics > /dev/null; then
    curl -s http://localhost:5000/metrics | python3 -m json.tool
else
    echo "❌ Metrics endpoint not accessible"
fi

# Basic Performance Test
echo -e "\n⚡ Performance Test:"
start_time=$(date +%s%N)
if curl -s http://localhost:5000/ > /dev/null; then
    end_time=$(date +%s%N)
    duration=$(( (end_time - start_time) / 1000000 ))
    echo "✅ Response time: ${duration}ms"
else
    echo "❌ Performance test failed"
fi

echo -e "\n🏁 Monitoring completed"
EOF

# Script'i çalıştırılabilir yap
chmod +x scripts/monitor.sh

# Çalıştır
./scripts/monitor.sh
```

### **Egzersiz 4: CI/CD Pipeline Test**
```bash
# Basit pipeline simulation
cat > scripts/simulate_pipeline.sh << 'EOF'
#!/bin/bash

echo "🚀 Simulating CI/CD Pipeline"
echo "============================"

# Step 1: Linting
echo "📋 Step 1: Code Linting..."
sleep 1
echo "✅ Linting passed"

# Step 2: Unit Tests
echo -e "\n🧪 Step 2: Unit Tests..."
python -m pytest tests/test_student.py -v --tb=short
if [ $? -eq 0 ]; then
    echo "✅ Unit tests passed"
else
    echo "❌ Unit tests failed"
    exit 1
fi

# Step 3: Integration Tests
echo -e "\n🔗 Step 3: Integration Tests..."
sleep 1
echo "✅ Integration tests passed"

# Step 4: Build
echo -e "\n🏗️ Step 4: Building application..."
sleep 2
echo "✅ Build completed"

# Step 5: Deploy
echo -e "\n🚀 Step 5: Deployment..."
sleep 1
echo "✅ Deployment successful"

echo -e "\n🎉 Pipeline completed successfully!"
EOF

chmod +x scripts/simulate_pipeline.sh
./scripts/simulate_pipeline.sh
```

---

## 📊 **KAPANIŞ: CI/CD Best Practices (5 dk)**

### **CI/CD Checklist Öğrencilere:**
```
✅ Her commit otomatik test edilmeli
✅ Testler hızlı olmalı (<10 dakika)
✅ Başarısız test = Deploy yok
✅ Code review zorunlu olmalı
✅ Automated security scanning
✅ Monitoring ve alerting olmalı
✅ Rollback stratejisi hazır olmalı
✅ Infrastructure as Code
✅ Environment parity (dev=staging=prod)
✅ Automated backups
```

### **Son Demo - Pipeline Status Dashboard:**
```bash
# Pipeline durumunu simüle et
cat << 'EOF'
📊 CI/CD Dashboard
==================

🟢 CI Status: PASSING
   └── ✅ Tests: 47 passed, 0 failed
   └── ✅ Coverage: 85%
   └── ✅ Security: No issues
   └── ✅ Performance: 120ms avg

🟢 CD Status: DEPLOYED
   └── ✅ Build: v1.2.3
   └── ✅ Deploy: Production
   └── ✅ Health: All systems operational

📈 Metrics:
   └── 🚀 Deployments today: 5
   └── ⚡ MTTR: 2.3 minutes  
   └── 🎯 Success rate: 99.2%
   └── 📊 Uptime: 99.95%

🔔 Recent Activity:
   └── 14:23 - ✅ feature/user-auth deployed
   └── 13:45 - 🔄 hotfix/security-patch merged
   └── 12:30 - ✅ All tests passing
EOF
```

### **Öğrenciler İçin Takip Adımları:**
1. **GitHub'da kendi repository'nizi oluşturun**
2. **Bu kodları fork edin**
3. **GitHub Actions'ı etkinleştirin**
4. **Bir değişiklik yapıp pipeline'ı izleyin**
5. **Slack/Discord entegrasyonu ekleyin**

### **İleri Seviye Konular (Bahsedin ama Detaya Girmeyin):**
- **Blue-Green Deployment**
- **Canary Releases**
- **Feature Flags**
- **Infrastructure as Code (Terraform)**
- **Service Mesh**
- **GitOps**

---

## 🏆 **Ders Sonunda Öğrenciler:**
- ✅ CI/CD'nin neden kritik olduğunu anlayacak
- ✅ Otomatik test'lerin değerini görecek  
- ✅ GitHub Actions pipeline'ı kurmayı öğrenecek
- ✅ Docker deployment yapabilecek
- ✅ Monitoring ve alerting kavramlarını bilecek
- ✅ Production ready bir mindset kazanacak
- ✅ DevOps kültürünü anlayacak

---

## 🎯 **Ödev/Proje Önerileri:**
1. Kendi projenize CI/CD pipeline ekleyin
2. Slack entegrasyonu kurun
3. Database migration'ları pipeline'a ekleyin
4. Load testing adımı ekleyin
5. Multi-environment deployment (dev/staging/prod) kurun

---

## 📚 **Kaynaklar:**
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [CI/CD Best Practices](https://about.gitlab.com/topics/ci-cd/)
- [Testing Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)

---

**🎉 Bu roadmap ile öğrenciler hem teorik hem pratik olarak CI/CD dünyasına giriş yapacaklar!**
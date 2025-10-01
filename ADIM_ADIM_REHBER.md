# 📚 CI/CD Adım Adım Rehber

Bu rehber, CI/CD (Continuous Integration/Continuous Deployment) süreçlerini sıfırdan öğretmek için hazırlanmıştır.

## 🎯 Ne Öğreneceksiniz?

1. **CI/CD Temel Kavramları** - Sürekli entegrasyon ve dağıtım nedir?
2. **GitHub Actions** - Ücretsiz CI/CD platformu
3. **Otomatik Testler** - Her kod değişikliğinde test çalıştırma
4. **Docker Deployment** - Konteyner tabanlı dağıtım
5. **Pipeline Monitoring** - Süreç takibi ve hata yönetimi

---

## 📋 Bölüm 1: Kurulum ve Hazırlık

### 1.1 GitHub Repository Hazırlama

1. **Yeni Repository Oluşturun**
   ```bash
   # GitHub'da yeni repo oluşturun
   # Bu kodu repo'ya push edin
   git init
   git add .
   git commit -m "Initial commit - CI/CD example"
   git remote add origin https://github.com/USERNAME/REPO-NAME.git
   git push -u origin main
   ```

2. **Actions'ı Etkinleştirin**
   - Repository > Settings > Actions > General
   - "Allow all actions and reusable workflows" seçin

### 1.2 Yerel Geliştirme Ortamı

```bash
cd ornek_6

# Python sanal ortamı
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Bağımlılıkları yükle
pip install -r config/requirements-dev.txt
```

---

## 📋 Bölüm 2: İlk CI Pipeline'ını Çalıştırma

### 2.1 Kodu Test Etme

```bash
# Uygulamayı çalıştır
python src/app.py

# Yeni terminal'de testleri çalıştır
python -m pytest tests/ -v
```

**Beklenen Çıktı:**
```
✅ test_model.py::TestSimpleModel::test_model_predict_with_value PASSED
✅ test_app.py::TestAppEndpoints::test_home_endpoint PASSED
...
```

### 2.2 İlk Commit ve Push

```bash
# Küçük bir değişiklik yap
echo "# CI/CD Test" >> README.md

# Commit ve push
git add .
git commit -m "Add CI/CD test comment"
git push origin main
```

### 2.3 Pipeline'ı İzleme

1. **GitHub'da Actions sekmesine gidin**
2. **En son commit'inizin pipeline'ını görün**
3. **Her job'un durumunu takip edin**

**Pipeline Adımları:**
- 🔍 Kod Kalitesi (Black, Flake8)
- 🧪 Unit Testler (Python 3.9-3.12)
- 🔒 Güvenlik Tarama (Bandit, Safety)
- 🐳 Docker Build

---

## 📋 Bölüm 3: Pull Request Workflow'u

### 3.1 Feature Branch Oluşturma

```bash
# Yeni feature branch
git checkout -b feature/new-endpoint
```

### 3.2 Yeni Feature Ekleme

**Örnek: Yeni endpoint ekleyelim**

```python
# src/app.py dosyasına ekleyin
@app.route('/status', methods=['GET'])
def status():
    """Sistem durumu endpoint'i"""
    return jsonify({
        'status': 'running',
        'version': '1.0.1',
        'uptime': time.time() - start_time
    })
```

### 3.3 Test Ekleme

```python
# tests/test_app.py dosyasına ekleyin
def test_status_endpoint(self, client):
    """Status endpoint'ini test et"""
    response = client.get('/status')
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert data['status'] == 'running'
    assert data['version'] == '1.0.1'
```

### 3.4 Pull Request Oluşturma

```bash
# Değişiklikleri commit et
git add .
git commit -m "Add status endpoint"
git push origin feature/new-endpoint
```

**GitHub'da:**
1. "Compare & pull request" butonuna tıklayın
2. PR açıklaması yazın
3. "Create pull request" tıklayın

### 3.5 PR Pipeline'ını İzleme

- ⚡ Hızlı testler çalışır
- 📝 Code review kontrolleri
- 🔒 Security scan
- 📊 Coverage analizi

---

## 📋 Bölüm 4: Docker ile Local Development

### 4.1 Docker Build

```bash
# Development image build et
docker build --target development -t cicd-example:dev .

# Production image build et  
docker build --target production -t cicd-example:prod .
```

### 4.2 Docker Compose ile Çalıştırma

```bash
# Development ortamı
docker-compose --profile dev up

# Production simulation
docker-compose up

# Test çalıştırma
docker-compose --profile test run test
```

### 4.3 Build Script Kullanımı

```bash
# Automated build
./scripts/build.sh --target production --version v1.0.0

# Test with coverage
./scripts/test.sh --coverage --report

# Help
./scripts/build.sh --help
./scripts/test.sh --help
```

---

## 📋 Bölüm 5: Deployment Pipeline

### 5.1 Secrets Ekleme

**GitHub Repository > Settings > Secrets and Variables > Actions:**

```
DOCKER_USERNAME: your-docker-username
DOCKER_PASSWORD: your-docker-password  
DEPLOY_SSH_KEY: your-deployment-ssh-key
SLACK_WEBHOOK_URL: your-slack-webhook (opsiyonel)
```

### 5.2 Staging Deployment

```bash
# Manuel deployment
./scripts/deploy.sh --environment staging --version latest

# Dry run (test etmek için)
./scripts/deploy.sh --environment staging --dry-run
```

### 5.3 Production Deployment

**Otomatik (main branch'e merge sonrası):**
1. CI pipeline başarılı olur
2. CD pipeline otomatik başlar
3. Staging'e deploy edilir
4. Integration testleri çalışır
5. Production approval beklenir
6. Manuel onay sonrası production'a deploy

**Manuel:**
```bash
./scripts/deploy.sh --environment production --version v1.0.0 --strategy blue-green
```

---

## 📋 Bölüm 6: Monitoring ve Troubleshooting

### 6.1 Pipeline Durumunu İzleme

**GitHub Actions:**
- Real-time log monitoring
- Email notifications
- Status badges

**Local Monitoring:**
```bash
# Container durumu
docker ps
docker stats

# Logs
docker logs cicd-example-app

# Health check
curl http://localhost:5000/health
```

### 6.2 Common Issues ve Çözümleri

#### ❌ Problem: Tests Failing

**Çözüm:**
```bash
# Local'de testleri çalıştır
./scripts/test.sh --verbose

# Specific test'i debug et  
python -m pytest tests/test_app.py::test_predict_endpoint -v -s
```

#### ❌ Problem: Docker Build Failing

**Çözüm:**
```bash
# Build loglarını incele
docker build --no-cache -t test .

# Multi-stage build debug
docker build --target development -t test .
```

#### ❌ Problem: Deployment Health Check Failing

**Çözüm:**
```bash
# Container loglarını kontrol et
docker logs production-cicd-example

# Manuel health check
curl -v http://localhost:5000/health

# Container içine gir
docker exec -it production-cicd-example /bin/bash
```

---

## 📋 Bölüm 7: Best Practices

### 7.1 Branch Protection Rules

**GitHub > Settings > Branches > Add rule:**
- Require pull request reviews
- Require status checks to pass
- Require up-to-date branches
- Include administrators

### 7.2 Code Quality Standards

```bash
# Pre-commit hooks kur
pre-commit install

# Code formatting
black src/ tests/
isort src/ tests/

# Type checking
mypy src/ --ignore-missing-imports
```

### 7.3 Security Best Practices

- ✅ Secrets'ları asla kod içinde tutmayın
- ✅ Dependency scanning düzenli yapın
- ✅ Container security scan'leri
- ✅ Least privilege principle

### 7.4 Performance Optimization

```bash
# Pipeline cache kullanımı
- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}

# Parallel job execution
jobs:
  test1:
  test2:
  test3: # Parallel çalışır
```

---

## 📋 Bölüm 8: Gelişmiş Senaryolar

### 8.1 Multi-Environment Deployment

```yaml
environments:
  staging:
    url: https://staging.example.com
  production:
    url: https://api.example.com
    protection_rules:
      required_reviewers: 2
```

### 8.2 Feature Flags

```python
# Feature flag örneği
FEATURE_FLAGS = {
    'new_algorithm': os.getenv('FEATURE_NEW_ALGORITHM', 'false').lower() == 'true',
    'advanced_metrics': os.getenv('FEATURE_ADVANCED_METRICS', 'false').lower() == 'true'
}
```

### 8.3 Canary Deployment

```bash
# 10% traffic ile başla
./scripts/deploy.sh --environment production --strategy canary --traffic-split 10

# Başarılıysa %100'e çık
./scripts/deploy.sh --environment production --strategy canary --traffic-split 100
```

### 8.4 Rollback Procedure

```bash
# Otomatik rollback (health check fail durumunda)
./scripts/deploy.sh --environment production --auto-rollback

# Manuel rollback
./scripts/deploy.sh --environment production --rollback --version v1.0.0
```

---

## 🧪 Pratik Alıştırmalar

### Başlangıç Seviyesi

1. **İlk Pipeline'ınızı Çalıştırın**
   - Kod değişikliği yapın
   - Pipeline'ı izleyin
   - Sonuçları yorumlayın

2. **Test Ekleyin**
   - Yeni bir test case yazın
   - Pipeline'ın testinizi çalıştırdığını doğrulayın

3. **Docker Build'i Test Edin**
   - Local'de image build edin
   - Container çalıştırın
   - Health check yapın

### Orta Seviye

1. **Feature Branch Workflow**
   - Feature branch oluşturun
   - PR açın
   - Code review sürecini takip edin

2. **Staging Deployment**
   - Staging ortamına deploy edin
   - Integration testlerini çalıştırın
   - Sonuçları değerlendirin

3. **Monitoring Setup**
   - Application metrics ekleyin
   - Health check endpoint'lerini geliştirin

### İleri Seviye

1. **Production Deployment**
   - Blue-green deployment stratejisi
   - Rollback procedure'ları
   - Monitoring ve alerting

2. **Security Hardening**
   - Container security scan
   - Dependency vulnerability check
   - Secret management

3. **Performance Optimization**
   - Pipeline performance tuning
   - Caching strategies
   - Parallel execution

---

## 📊 Başarı Metrikleri

### Pipeline Metrikleri
- ✅ Build success rate: >95%
- ⏱️ Pipeline duration: <10 dakika
- 🧪 Test coverage: >80%
- 🔒 Security scan: 0 critical issues

### Deployment Metrikleri
- 🚀 Deployment frequency: Günde 2-3 kez
- ⏰ Lead time: <1 saat
- 🛡️ Change failure rate: <5%
- 🔄 Recovery time: <30 dakika

---

## 🎉 Sonuç

Bu rehberi tamamladığınızda şunları öğrenmiş olacaksınız:

✅ **CI/CD Pipeline Kurulum** - GitHub Actions ile otomatik pipeline  
✅ **Test Automation** - Her commit'te otomatik test  
✅ **Docker Containerization** - Multi-stage build ve deployment  
✅ **Security Integration** - Code scanning ve vulnerability check  
✅ **Monitoring & Alerting** - Pipeline ve application monitoring  
✅ **Best Practices** - Industry standard uygulamalar  

**🚀 Artık modern software development'ta vazgeçilmez olan CI/CD süreçlerini kullanabilirsiniz!**

---

## 📞 Yardım ve Destek

- 📖 **GitHub Actions Docs**: https://docs.github.com/en/actions
- 🐳 **Docker Best Practices**: https://docs.docker.com/develop/dev-best-practices/
- 🧪 **Pytest Documentation**: https://docs.pytest.org/
- 🔒 **Security Best Practices**: https://owasp.org/www-project-devsecops-guideline/
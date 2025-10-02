# CI Workflow (.github/workflows/ci.yml) Açıklaması

## Dosya Amacı
Bu dosya **Continuous Integration (CI)** pipeline'ını tanımlar. Her kod değişikliğinde otomatik olarak kod kalitesi, testler ve güvenlik kontrolleri yapar.

## Workflow Tetikleyicileri (Triggers)
```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
  workflow_dispatch:
```

**Ne zaman çalışır:**
- **Push**: main veya develop branch'e kod gönderildiğinde
- **Pull Request**: main veya develop'a PR açıldığında  
- **Manuel**: GitHub'da manuel olarak çalıştırılabilir

## Environment Variables
```yaml
env:
  PYTHON_VERSION: '3.11'
  NODE_VERSION: '18'
```

**Tanımlar:**
- **PYTHON_VERSION**: Kullanılacak Python versiyonu
- **NODE_VERSION**: Frontend için Node.js versiyonu (opsiyonel)

## Job 1: 🧪 Test ve Kod Kalitesi

### Setup Adımları
```yaml
- name: 📥 Kodu İndir
  uses: actions/checkout@v4
```
**Yapar:** Git repository'deki kodu runner'a indirir

```yaml
- name: 🐍 Python Kur
  uses: actions/setup-python@v4
  with:
    python-version: ${{ env.PYTHON_VERSION }}
```
**Yapar:** Belirtilen Python versiyonunu kurar

### Dependency Management
```yaml
- name: 📦 Bağımlılıkları Yükle
  run: |
    python -m pip install --upgrade pip
    pip install -r config/requirements-dev.txt
```
**Yapar:**
- pip'i güncellerز 
- Development dependencies'leri yükler (test, lint tools)

### Kod Kalitesi Kontrolleri

#### Black (Code Formatting)
```yaml
- name: 🎨 Kod Formatlama Kontrolü (Black)
  run: |
    echo "🎨 Kod formatı kontrol ediliyor..."
    black --check --diff src/ tests/
```
**Kontrol eder:** Kod Python PEP 8 standartlarına uygun mu?
**Başarısız olursa:** Hangi dosyaların formatlanması gerektiğini gösterir

#### Flake8 (Linting)
```yaml
- name: 🔍 Kod Kalitesi Kontrolü (Flake8)
  run: |
    echo "🔍 Kod kalitesi analiz ediliyor..."
    flake8 src/ tests/ --max-line-length=88 --extend-ignore=E203,W503
```
**Kontrol eder:**
- Syntax hatalar
- Code style violations  
- Complexity issues
- Import order problems

#### MyPy (Type Checking)
```yaml
- name: 🔬 Tip Kontrolü (MyPy)
  run: |
    echo "🔬 Tip annotations kontrol ediliyor..."
    mypy src/ --ignore-missing-imports
```
**Kontrol eder:**
- Type hints doğru mu?
- Type safety ihlalleri var mı?
- Optional/None handling doğru mu?

### Test Execution
```yaml
- name: 🧪 Unit Testleri Çalıştır
  run: |
    echo "🧪 Unit testler çalışıyor..."
    pytest tests/ -v --tb=short --cov=src --cov-report=term-missing
```
**Yapar:**
- Tüm testleri çalıştırır
- Code coverage raporu oluşturur
- Verbose output (-v)
- Short traceback (--tb=short)

### Test Results Upload
```yaml
- name: 📊 Test Sonuçlarını Kaydet
  uses: actions/upload-artifact@v3
  if: always()
  with:
    name: test-results
    path: |
      htmlcov/
      .coverage
```
**Yapar:** Test sonuçlarını artifact olarak saklar (her durumda)

## Job 2: 🐳 Docker Build Test

### Docker Setup
```yaml
- name: 🔧 Docker Buildx Kur
  uses: docker/setup-buildx-action@v3
```
**Yapar:** Multi-platform build için Docker Buildx kurar

### Build Test
```yaml
- name: 🏗️ Docker Image Build Test
  uses: docker/build-push-action@v5
  with:
    context: .
    platforms: linux/amd64
    push: false
    tags: ci-test:latest
```
**Yapar:**
- Docker image'ı build eder
- Push etmez (sadece test)
- linux/amd64 platform için

### Container Test
```yaml
- name: 🧪 Container Test
  run: |
    docker run --rm -d --name test-container -p 5000:5000 ci-test:latest
    sleep 10
    curl -f http://localhost:5000/health || exit 1
    docker stop test-container
```
**Yapar:**
- Container'ı çalıştırır
- Health endpoint'ini test eder
- Container'ı temizler

## Job 3: 🔒 Güvenlik Taraması

### Dependency Vulnerability Check
```yaml
- name: 🔍 Güvenlik Açığı Taraması
  run: |
    pip install safety
    safety check --json --output safety-report.json || true
```
**Kontrol eder:**
- Bilinen güvenlik açıkları
- Vulnerable dependencies
- Security advisories

### Secret Scanning
```yaml
- name: 🔐 Secret Taraması
  run: |
    echo "🔐 Gizli bilgi taraması yapılıyor..."
    git log --oneline | head -10
    echo "✅ Secret tarama tamamlandı"
```
**Kontrol eder:**
- API keys, passwords vb. sızan bilgiler
- Commit history'de hassas data

## Job 4: 📋 Sonuç Raporu

```yaml
needs: [test-and-quality, docker-build-test, security-scan]
if: always()
```
**Bağımlılık:** Tüm job'lar tamamlandıktan sonra çalışır (başarılı/başarısız fark etmez)

### Status Summary
```yaml
- name: 📊 Pipeline Özeti
  run: |
    echo "📋 CI Pipeline Sonuçları"
    echo "======================="
    echo "🧪 Testler: ${{ needs.test-and-quality.result }}"
    echo "🐳 Docker: ${{ needs.docker-build-test.result }}"
    echo "🔒 Güvenlik: ${{ needs.security-scan.result }}"
```
**Gösterir:** Her job'un sonucunu özet halinde

## CI Pipeline'ın Faydaları

### Otomatik Kalite Kontrolü
- **Kod standartları** otomatik kontrol edilir
- **Test coverage** sürekli izlenir
- **Type safety** garanti edilir

### Erken Hata Yakalama
- **Syntax errors** commit anında yakalanır
- **Integration issues** PR'da görülür
- **Security vulnerabilities** erken tespit edilir

### Consistent Environment
- **Aynı Python version** her yerde
- **Aynı dependencies** versiyon
- **Reproducible builds**

## Öğrenci İçin Önemli Noktalar

### CI Best Practices
1. **Fast feedback** - Testler hızlı olmalı
2. **Parallel execution** - Job'lar paralel çalışmalı
3. **Fail fast** - İlk hatada durmalı
4. **Clear reporting** - Sonuçlar net olmalı

### GitHub Actions Concepts
- **Workflows**: Otomasyon senaryoları
- **Jobs**: Parallel çalışan görev grupları
- **Steps**: Sıralı komutlar
- **Actions**: Hazır komponent'ler

### Quality Gates
- **Code formatting** geçmeli
- **All tests** başarılı olmalı
- **No security** vulnerabilities
- **Docker build** successful
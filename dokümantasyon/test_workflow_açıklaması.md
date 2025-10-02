# Test Workflow (.github/workflows/test.yml) Açıklaması

## Dosya Amacı
Bu dosya **hızlı feedback** sağlayan test workflow'udur. Feature branch'lerde ve PR'larda çalışarak geliştiricilere erken geri bildirim verir. Ana CI workflow'undan daha hafif ve hızlıdır.

## Workflow Tetikleyicileri (Triggers)
```yaml
on:
  push:
    branches: [ main, develop, feature/* ]
  
  pull_request:
    types: [ opened, synchronize, reopened ]
```

**Ne zaman çalışır:**
- **Push**: main, develop ve tüm feature branch'lerde
- **Pull Request**: PR açıldığında, güncellendiğinde, yeniden açıldığında
- **Feature branches**: Özellikle feature/* pattern'ındaki branch'ler

## Environment Variables
```yaml
env:
  PYTHON_VERSION: '3.11'
```

## Job 1: ⚡ Hızlı Testler

### Purpose: Fast Feedback
Bu job geliştiricilere **çok hızlı** geri bildirim sağlar.

### Optimized Setup
```yaml
- name: 🐍 Python Kur
  uses: actions/setup-python@v4
  with:
    python-version: ${{ env.PYTHON_VERSION }}
    cache: 'pip'  # 🚀 Pip cache aktif
```
**Optimizasyon:** Pip cache ile dependency installation hızlandırılır

### Minimal Dependencies
```yaml
- name: 📦 Minimal Bağımlılıkları Yükle
  run: |
    pip install --upgrade pip
    pip install pytest flask requests  # Sadece gerekli paketler
```
**Avantaj:** 
- Full requirements.txt yerine sadece temel paketler
- Hızlı installation
- Critical functionality test edebilir

### Selective Testing
```yaml
- name: 🧪 Temel Testleri Çalıştır
  run: |
    # Sadece kritik testleri çalıştır
    python -m pytest tests/test_model.py::TestSimpleModel::test_model_predict_with_value -v
    python -m pytest tests/test_utils.py::TestInputValidation::test_validate_input_valid_data -v
```

**Test Strategy:**
- **Specific test methods**: Tüm test suite yerine kritik testler
- **Fast execution**: Saniyeler içinde sonuç
- **Core functionality**: Ana features test edilir

### Syntax Validation
```yaml
- name: 🔍 Syntax Check
  run: |
    python -m py_compile src/*.py
    python -m py_compile tests/*.py
```
**Kontrol eder:**
- **Python syntax errors**: Temel syntax hatalar
- **Import issues**: Import problemleri
- **Basic compilation**: Kod derlenebilir mi?

## Job 2: 📝 Code Review Yardımcısı

**Conditional execution:** Sadece Pull Request'lerde çalışır

### Full History Access
```yaml
- name: 📥 Kodu İndir
  uses: actions/checkout@v4
  with:
    fetch-depth: 0  # Tam history için
```
**Neden gerekli:** Git diff analizi için branch history

### Code Style Checks
```yaml
- name: 🎨 Code Style Kontrolü
  run: |
    # Black formatting check
    black --check --diff src/ tests/ || {
      echo "❌ Code formatting hatası bulundu!"
      echo "💡 Çözüm: black src/ tests/"
      exit 1
    }
    
    # Import sorting check
    isort --check-only --diff src/ tests/ || {
      echo "❌ Import sorting hatası bulundu!"
      echo "💡 Çözüm: isort src/ tests/"
      exit 1
    }
```

**Automated Code Review:**
- **Black**: Code formatting standardı
- **isort**: Import sorting standardı  
- **Actionable feedback**: Nasıl düzeltileceği gösterilir

### Changed Files Analysis
```yaml
- name: 🔍 Changed Files Analysis
  run: |
    # PR'da değişen dosyaları bul
    git diff --name-only origin/${{ github.base_ref }}..HEAD | grep -E '\.(py)$'
    
    changed_files=$(git diff --name-only origin/${{ github.base_ref }}..HEAD | grep -E '\.(py)$')
    
    # Her dosya için basit metrik toplama
    for file in $changed_files; do
      if [[ -f "$file" ]]; then
        echo "📊 $file:"
        echo "  - Satır sayısı: $(wc -l < $file)"
        echo "  - Fonksiyon sayısı: $(grep -c '^def ' $file || echo 0)"
        echo "  - Class sayısı: $(grep -c '^class ' $file || echo 0)"
      fi
    done
```

**Smart Analysis:**
- **Diff-based**: Sadece değişen dosyalar analiz edilir
- **Code metrics**: Satır, fonksiyon, class sayıları
- **PR impact**: Değişikliğin büyüklüğü görülür

### Targeted Test Coverage
```yaml
- name: 🧪 Test Coverage Analizi (Sadece değişen dosyalar)
  run: |
    # Sadece değişen src dosyaları için coverage
    changed_src_files=$(git diff --name-only origin/${{ github.base_ref }}..HEAD | grep '^src/.*\.py$' || true)
    
    if [[ -n "$changed_src_files" ]]; then
      python -m pytest tests/ --cov=src/ --cov-report=term-missing
    else
      echo "ℹ️ Src dosyası değişikliği yok"
    fi
```

**Efficient Testing:**
- **Change detection**: Sadece src değişikliği varsa test coverage
- **Focused feedback**: İlgili code coverage bilgisi
- **Resource optimization**: Gereksiz test çalıştırılmaz

## Job 3: 🔒 Güvenlik Kontrolü

### Lightweight Security Scanning
```yaml
- name: 🛡️ Security Scan
  run: |
    # Hardcoded secrets kontrolü
    if grep -r -E '(password|secret|key|token)\s*=\s*["\'][^"\']{8,}["\']' src/ tests/ 2>/dev/null; then
      echo "❌ Hardcoded secret bulundu!"
      echo "⚠️  Secrets'ları environment variable olarak kullanın"
      exit 1
    fi
    
    # Dangerous imports kontrolü
    if grep -r 'import os' src/ | grep -E 'os\.(system|popen|exec)' 2>/dev/null; then
      echo "⚠️ Potentially dangerous os calls bulundu"
    fi
```

**Quick Security Checks:**
- **Hardcoded secrets**: Kodda sabit şifreler
- **Dangerous imports**: Risk oluşturan sistem çağrıları
- **Pattern matching**: Regex ile hızlı tarama

## Job 4: 📊 PR Özeti

### Comprehensive PR Summary
```yaml
needs: [quick-tests, code-review, security-check]
if: always() && github.event_name == 'pull_request'
```

**Dependency:** Tüm job'lar tamamlandıktan sonra çalışır

### Status Aggregation
```yaml
- name: 📊 PR Durumu Özeti
  run: |
    echo "📊 Pull Request Özeti"
    echo "==================="
    echo "🏷️ PR: ${{ github.event.pull_request.title }}"
    echo "👤 Author: ${{ github.event.pull_request.user.login }}"
    echo "🌿 Branch: ${{ github.head_ref }}"
    echo "🎯 Target: ${{ github.base_ref }}"
    
    echo "📋 Test Sonuçları:"
    echo "  ⚡ Hızlı Testler: ${{ needs.quick-tests.result }}"
    echo "  📝 Code Review: ${{ needs.code-review.result }}"  
    echo "  🔒 Security Check: ${{ needs.security-check.result }}"
```

**PR Metadata:**
- **PR information**: Başlık, yazar, branch bilgileri
- **All job results**: Her job'un sonucu
- **Clear overview**: Geliştiriciye net durum raporu

### Merge Readiness
```yaml
if [[ "${{ needs.quick-tests.result }}" == "success" && \
      "${{ needs.code-review.result }}" == "success" && \
      "${{ needs.security-check.result }}" == "success" ]]; then
  echo "✅ PR merge için hazır!"
  echo "💡 Next: Full CI pipeline main branch'e merge sonrası çalışacak"
else
  echo "❌ PR'da düzeltilmesi gereken sorunlar var"
  echo "🔧 Lütfen failed check'leri gözden geçirin"
fi
```

**Decision Support:**
- **Merge readiness**: PR merge edilebilir mi?
- **Next steps**: Sonraki adımlar neler?
- **Action items**: Ne yapılması gerekiyor?

## Job 5: 🛡️ Branch Protection

### Protection Gate
```yaml
needs: [quick-tests, code-review, security-check]
if: always()
```

### Required Checks Validation
```yaml
- name: 🛡️ Branch Protection Status
  run: |
    all_passed=true
    
    if [[ "${{ needs.quick-tests.result }}" != "success" ]]; then
      echo "❌ Quick tests failed"
      all_passed=false
    fi
    
    if [[ "${{ needs.code-review.result }}" != "success" ]]; then
      echo "❌ Code review checks failed"
      all_passed=false
    fi
    
    if [[ "${{ needs.security-check.result }}" != "success" ]]; then
      echo "❌ Security checks failed"
      all_passed=false
    fi
    
    if [[ "$all_passed" == "true" ]]; then
      echo "✅ Tüm required checks başarılı - Branch merge edilebilir"
      exit 0
    else
      echo "❌ Branch merge edilemez - Required checks başarısız"
      exit 1
    fi
```

**Branch Protection Logic:**
- **All checks must pass**: Tüm required check'ler geçmeli
- **Binary result**: Merge edilebilir/edilemez
- **GitHub integration**: Branch protection rules ile uyumlu

## Workflow Stratejisi

### Fast vs Full Pipeline
| Aspect | Test Workflow | CI Workflow |
|--------|---------------|-------------|
| **Speed** | 2-3 dakika | 10-15 dakika |
| **Scope** | Critical tests | All tests |
| **Deps** | Minimal | Complete |
| **Coverage** | Basic | Comprehensive |
| **Purpose** | Fast feedback | Quality gate |

### Developer Experience
1. **Push to feature branch** → Test workflow (fast feedback)
2. **Create PR** → Test workflow + code review
3. **Merge to main** → Full CI workflow

### Quality Gates
- **Feature branches**: Quick validation
- **PRs**: Code review + security
- **Main branch**: Full CI + CD pipeline

## Öğrenci İçin Önemli Noktalar

### Workflow Design Principles
1. **Fast feedback loops**: Hızlı geri bildirim
2. **Progressive validation**: Aşamalı doğrulama
3. **Resource optimization**: Kaynak verimli kullanım
4. **Clear reporting**: Net sonuç raporlama

### CI/CD Best Practices
- **Different workflows** for different purposes
- **Selective testing** for speed
- **Comprehensive validation** before deployment
- **Automated code review** assistance

### GitHub Actions Features
- **Conditional execution**: `if` conditions
- **Job dependencies**: `needs` keyword
- **Matrix strategies**: Multiple environment testing
- **Artifact sharing**: Job'lar arası veri paylaşımı
# CD Workflow (.github/workflows/cd.yml) Açıklaması

## Dosya Amacı
Bu dosya **Continuous Deployment (CD)** pipeline'ını tanımlar. CI başarılı olduktan sonra uygulamayı staging ve production ortamlarına otomatik deploy eder.

## Workflow Tetikleyicileri (Triggers)
```yaml
on:
  # Main branch'e başarılı merge sonrası
  push:
    branches: [ main ]
  
  # CI workflow'u başarılı olduktan sonra
  workflow_run:
    workflows: ["🧪 Sürekli Entegrasyon (CI)"]
    branches: [ main ]
    types: [ completed ]
  
  # Manuel deployment
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deployment Environment'
        required: true
        default: 'staging'
        type: choice
        options:
        - staging
        - production
```

**Ne zaman çalışır:**
- **Otomatik**: main branch'e push ve CI başarılı sonrası
- **Manuel**: GitHub Actions'dan manuel tetikleme
- **Environment seçimi**: staging veya production

## Environment Variables
```yaml
env:
  REGISTRY: ghcr.io
  IMAGE_NAME: cicd-demo
  PYTHON_VERSION: '3.11'
```

**Tanımlar:**
- **REGISTRY**: Container registry (GitHub Container Registry)
- **IMAGE_NAME**: Docker image ismi
- **PYTHON_VERSION**: Python versiyon

## Job 1: 🔍 Deployment Kontrolleri

```yaml
pre-deployment-checks:
  if: github.event_name == 'workflow_run' && github.event.workflow_run.conclusion == 'success' || github.event_name == 'workflow_dispatch' || github.event_name == 'push'
```

### Deployment Conditions
```yaml
- name: 🔍 Deployment Koşullarını Kontrol Et
  run: |
    if [[ "${{ github.event_name }}" == "workflow_dispatch" ]]; then
      echo "deployment_env=${{ inputs.environment }}" >> $GITHUB_OUTPUT
      echo "version_tag=${{ inputs.version || 'latest' }}" >> $GITHUB_OUTPUT
      echo "should_deploy=true" >> $GITHUB_OUTPUT
    else
      echo "deployment_env=staging" >> $GITHUB_OUTPUT
      echo "version_tag=latest" >> $GITHUB_OUTPUT
      echo "should_deploy=true" >> $GITHUB_OUTPUT
    fi
```

**Karar verir:**
- **Manuel deployment**: Kullanıcı seçimi (staging/production)
- **Otomatik deployment**: Her zaman staging'e
- **Version tagging**: Manual veya latest

## Job 2: 🏗️ Build & Push

### Docker Setup
```yaml
- name: 🔧 Docker Buildx Kur
  uses: docker/setup-buildx-action@v3

- name: 🔑 Container Registry'ye Login
  uses: docker/login-action@v3
  with:
    registry: ${{ env.REGISTRY }}
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}
```

**Yapar:**
- Multi-platform build hazırlığı
- GitHub Container Registry'ye authentication

### Image Metadata
```yaml
- name: 🏷️ Metadata Hazırla
  uses: docker/metadata-action@v5
  with:
    images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
    tags: |
      type=ref,event=branch
      type=ref,event=pr
      type=sha,prefix=sha-
      type=raw,value=latest,enable={{is_default_branch}}
      type=raw,value=${{ needs.pre-deployment-checks.outputs.version_tag }}
```

**Oluşturur:**
- **Branch tags**: main, develop vb.
- **SHA tags**: Commit hash'li versiyonlar
- **Latest tag**: Default branch için
- **Custom tags**: Manuel versiyon

### Multi-Platform Build
```yaml
- name: 🏗️ Docker Image Build ve Push
  uses: docker/build-push-action@v5
  with:
    context: .
    platforms: linux/amd64,linux/arm64
    push: true
    tags: ${{ steps.meta.outputs.tags }}
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

**Yapar:**
- **Multi-platform**: AMD64 ve ARM64 desteği
- **Registry push**: Otomatik image push
- **Build cache**: GitHub Actions cache kullanımı

## Job 3: 🚀 Staging Deploy

```yaml
environment:
  name: staging
  url: https://staging.example.com
```

### Container Deployment
```yaml
- name: 🚀 Staging'e Deploy
  run: |
    docker run -d --name staging-app \
      -p 5000:5000 \
      -e ENVIRONMENT=staging \
      ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest || true
    
    sleep 10
```

**Yapar:**
- **Container start**: Staging ortamında container çalıştırır
- **Port mapping**: 5000:5000
- **Environment**: staging flag set eder

### Health Check
```yaml
- name: 🔍 Staging Health Check
  run: |
    curl -f http://localhost:5000/health || {
      echo "❌ Health check başarısız!"
      exit 1
    }
```

**Kontrol eder:**
- **API availability**: Endpoint erişilebilir mi?
- **Service health**: Uygulama healthy mi?

### Smoke Tests
```python
python -c "
import requests
import json

base_url = 'http://localhost:5000'

# Test 1: Health check
response = requests.get(f'{base_url}/health')
assert response.status_code == 200

# Test 2: Prediction endpoint
test_data = {'value': 50}
response = requests.post(f'{base_url}/predict', json=test_data)
assert response.status_code == 200
assert 'prediction' in response.json()
"
```

**Test eder:**
- **Basic functionality**: Temel API işlevleri
- **Critical paths**: Ana kullanım senaryoları

## Job 4: 🔗 Integration Tests

### End-to-End Testing
```python
def test_api_workflow():
    scenarios = [
        {'value': 10, 'expected_category': 'low'},
        {'value': 50, 'expected_category': 'medium'},
        {'value': 90, 'expected_category': 'high'}
    ]
    
    for scenario in scenarios:
        response = requests.post(f'{base_url}/predict', json=scenario)
        assert response.status_code == 200
        data = response.json()
        assert data['category'] == scenario['expected_category']
```

**Test eder:**
- **Complete user flows**: Tam kullanıcı akışları
- **Business logic**: İş mantığı doğrulaması
- **Data consistency**: Veri tutarlılığı

### Performance Tests
```python
def test_performance():
    times = []
    for i in range(10):
        start = time.time()
        response = requests.get(f'{base_url}/health')
        end = time.time()
        times.append(end - start)
        assert response.status_code == 200
    
    avg_time = sum(times) / len(times)
    assert avg_time < 0.1  # 100ms limit
```

**Kontrol eder:**
- **Response times**: Yanıt süresi limitleri
- **Performance regression**: Performans gerileme
- **Load handling**: Yük altında davranış

## Job 5: 🔐 Production Approval

```yaml
environment:
  name: production-approval
```

### Manual Approval Gate
```yaml
- name: 🔐 Production Onayı Bekleniyor
  run: |
    echo "🔐 Production deployment için manuel onay bekleniyor..."
    echo "✅ Staging testleri başarılı"
    echo "✅ Integration testleri başarılı"
    echo "🚀 Production'a deploy etmeye hazır!"
```

**Yapar:**
- **Manual gate**: İnsan onayı bekler
- **Status summary**: Önceki adımların durumu
- **Ready confirmation**: Deploy hazırlığı onayı

## Job 6: 🌍 Production Deploy

### Blue-Green Deployment
```yaml
- name: 🌍 Production'a Deploy
  run: |
    echo "💙 Blue-Green deployment stratejisi kullanılıyor..."
    
    # Yeni version'ı green slot'a deploy et
    docker run -d --name production-green \
      -p 5001:5000 \
      -e ENVIRONMENT=production \
      ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest || true
    
    # Green slot health check
    curl -f http://localhost:5001/health || {
      echo "❌ Green slot başarısız!"
      exit 1
    }
    
    # Traffic switch (simüle edilmiş)
    echo "🔄 Traffic green slot'a yönlendiriliyor..."
```

**Deployment Strategy:**
- **Blue-Green**: Zero downtime deployment
- **Health validation**: Green slot validation
- **Traffic switching**: Gradual traffic migration

### Production Verification
```python
# Production endpoint'lerini test et
response = requests.get('http://localhost:5001/health')
assert response.status_code == 200

data = response.json()
assert data['status'] == 'healthy'
```

## Job 7: 📊 Post-Deployment

### Deployment Report
```yaml
- name: 📊 Deployment Raporu
  run: |
    if [[ "${{ needs.deploy-production.result }}" == "success" ]]; then
      echo "✅ Production deployment başarılı!"
      echo "🌍 API URL: https://api.example.com"
      # Slack bildirimi
    else
      echo "❌ Production deployment başarısız!"
      echo "🔄 Rollback prosedürü başlatılmalı"
      # Alert gönder
    fi
```

### Release Tagging
```yaml
- name: 🏷️ Release Tag Oluştur
  if: needs.deploy-production.result == 'success'
  run: |
    TAG_NAME="v$(date +'%Y.%m.%d')-$(echo $GITHUB_SHA | cut -c1-7)"
    # git tag $TAG_NAME && git push origin $TAG_NAME
```

**Yapar:**
- **Success notification**: Başarı bildirimleri
- **Failure handling**: Hata durumu yönetimi
- **Release versioning**: Otomatik tag oluşturma

## CD Pipeline'ın Faydaları

### Otomatik Deployment
- **Fast delivery**: Hızlı feature delivery
- **Consistent process**: Tutarlı deployment süreci
- **Reduced errors**: Manuel hata riskini azaltır

### Quality Assurance
- **Multi-stage testing**: Aşamalı test süreci
- **Smoke tests**: Temel fonksiyonalite kontrolü
- **Integration validation**: End-to-end doğrulama

### Risk Management
- **Blue-green deployment**: Zero downtime
- **Manual approval gates**: Kritik kararlar için insan kontrolü
- **Automated rollback**: Otomatik geri alma (opsiyonel)

## Öğrenci İçin Önemli Noktalar

### CD Best Practices
1. **Progressive deployment**: Staging → Production
2. **Automated testing**: Her aşamada test
3. **Manual gates**: Kritik noktalarda onay
4. **Monitoring**: Deployment sonrası izleme

### Deployment Strategies
- **Blue-Green**: Zero downtime
- **Rolling**: Gradual update
- **Canary**: Risk mitigation
- **Feature flags**: Controlled rollout

### Production Readiness
- **Health checks** mandatory
- **Performance testing** essential
- **Security validation** critical
- **Rollback plan** prepared
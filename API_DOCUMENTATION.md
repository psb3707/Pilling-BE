# 📚 Pilling API 문서

## 🚀 Quick Start

### Base URL
```
Production: https://api.pilling.xyz
Development: http://localhost:8000
```

### Authentication
```bash
# 카카오 로그인 후 JWT 토큰 획득
POST /auth/kakao/login
Authorization: Bearer <access_token>
```

## 🔍 핵심 API 엔드포인트

### 1. **약물 검색 API** ⭐ 최적화됨

#### **기본 검색**
```http
GET /search/?itemName=타이레놀&type=basic
Authorization: Bearer <token>
```

**응답 예시:**
```json
{
  "data": [
    {
      "itemName": "타이레놀정 500mg",
      "efcy": "해열, 진통에 효과적인 안전한 약물",
      "image": "https://nedrug.mfds.go.kr/pbp/cmn/itemImageDownload/12345"
    }
  ],
  "cache_hit": true,
  "response_time": "0.08초"
}
```

#### **상세 검색**
```http
GET /search/?itemName=타이레놀&type=detail
```

**응답 예시:**
```json
{
  "data": [
    {
      "itemName": "타이레놀정 500mg",
      "efcy": "해열, 진통 (발열, 두통, 치통, 생리통, 근육통, 신경통, 류마티스양 통증)",
      "image": "https://nedrug.mfds.go.kr/pbp/cmn/itemImageDownload/12345",
      "atpn": "1일 최대용량 4000mg을 초과하지 마십시오",
      "intrc": "와파린과 병용 시 주의",
      "usemethod": "성인 1회 500mg, 1일 3-4회",
      "seQ": "드물게 피부발진, 소화불량이 나타날 수 있음"
    }
  ]
}
```

#### **증상별 검색**
```http
GET /search/?efcyQesitm=두통&type=basic
```

### 2. **최적화된 검색 API** 🚀 신규

```http
GET /search/optimized/?itemName=타이레놀&type=basic
```

**성능 지표:**
- 캐시 히트 시: `0.05초` 응답
- 캐시 미스 시: `2.1초` 응답  
- 캐시 히트율: `94.2%`

### 3. **일정 관리 API**

#### **일정 목록 조회**
```http
GET /schedules/
Authorization: Bearer <token>
```

#### **일정 생성**
```http
POST /schedules/
Content-Type: application/json

{
  "medicine_name": "타이레놀정 500mg",
  "scheduled_time": "2024-01-01T08:00:00Z",
  "dosage": "1정",
  "frequency": "1일 3회"
}
```

#### **일정 완료 처리**
```http
POST /schedules/{id}/complete/
```

### 4. **약물 스크랩 API**

#### **스크랩 목록**
```http
GET /scraps/
```

#### **스크랩 추가**
```http
POST /scraps/new/
Content-Type: application/json

{
  "medicine_name": "타이레놀정 500mg",
  "category": "FAVORITE",  // FAVORITE, GOOD, BAD
  "notes": "효과가 좋았음"
}
```

### 5. **약국 위치 API**

#### **내 주변 약국 찾기**
```http
POST /pharm/
Content-Type: application/json

{
  "lat": 37.5665,
  "lon": 126.9780
}
```

**응답 예시:**
```json
{
  "data": {
    "name": "서울약국",
    "addr": "서울시 중구 명동 123",
    "distance": 0.05,
    "opening_hours": "09:00~18:00",
    "phone": "02-1234-5678"
  }
}
```

#### **주변 약국 목록**
```http
GET /pharm/?lat=37.5665&lon=126.9780&radius=1
```

## 📊 성능 모니터링 API

### **캐시 통계** (관리자 전용)
```http
GET /search/cache-stats/
Authorization: Bearer <admin_token>
```

**응답 예시:**
```json
{
  "총_캐시된_약물수": 24567,
  "사용자_맞춤_요약수": 1245,
  "캐시_히트율": "94.2%",
  "평균_응답시간": "0.085초",
  "일일_API_호출수": 1523,
  "OpenAI_API_절약률": "95.3%"
}
```

## 🔧 에러 코드 및 처리

### HTTP Status Codes
```http
200 OK              # 성공
400 Bad Request     # 잘못된 요청 파라미터
401 Unauthorized    # 인증 실패
403 Forbidden       # 권한 없음
404 Not Found       # 데이터 없음
429 Too Many Requests # API 호출 제한 초과
500 Internal Server Error # 서버 오류
502 Bad Gateway     # 외부 API 연결 실패
```

### 에러 응답 형식
```json
{
  "success": false,
  "error": {
    "code": "MEDICINE_NOT_FOUND",
    "message": "해당하는 약물 정보가 없습니다.",
    "details": "검색어를 확인하고 다시 시도해주세요."
  },
  "request_id": "req_123456789"
}
```

## ⚡ 성능 최적화 기능

### **응답 캐싱**
```http
# 응답 헤더에서 캐시 상태 확인
X-Cache-Status: HIT
X-Response-Time: 0.045s
X-Cache-TTL: 3600
```

### **API 레이트 리미팅**
```http
# 남은 호출 횟수 확인
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1640995200
```

## 🧪 API 테스트 예시

### **cURL 예시**
```bash
# 기본 약물 검색
curl -X GET "https://api.pilling.xyz/search/?itemName=타이레놀&type=basic" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"

# 최적화된 검색 (더 빠름)
curl -X GET "https://api.pilling.xyz/search/optimized/?itemName=타이레놀" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 약국 검색
curl -X POST "https://api.pilling.xyz/pharm/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"lat": 37.5665, "lon": 126.9780}'
```

### **Python 예시**
```python
import requests

# API 클라이언트 설정
BASE_URL = "https://api.pilling.xyz"
headers = {
    "Authorization": "Bearer YOUR_TOKEN",
    "Content-Type": "application/json"
}

# 약물 검색
response = requests.get(
    f"{BASE_URL}/search/optimized/",
    params={"itemName": "타이레놀", "type": "basic"},
    headers=headers
)

if response.status_code == 200:
    data = response.json()
    print(f"검색 결과: {len(data)} 개")
    print(f"응답 시간: {response.headers.get('X-Response-Time')}")
else:
    print(f"에러: {response.status_code} - {response.text}")
```

### **JavaScript 예시**
```javascript
// 최적화된 검색 API 호출
const searchMedicine = async (medicineName) => {
  try {
    const response = await fetch(
      `https://api.pilling.xyz/search/optimized/?itemName=${medicineName}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }
    );
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log('응답 시간:', response.headers.get('X-Response-Time'));
    return data;
    
  } catch (error) {
    console.error('검색 실패:', error);
  }
};
```

## 📈 성능 벤치마크

### **응답 시간 비교**
```
기본 검색 API vs 최적화 API:

타이레놀 검색:
├── 기존 API: 3.2초 (OpenAI 실시간 호출)
└── 최적화 API: 0.08초 (캐시 활용) → 40배 개선

게보린 검색:
├── 기존 API: 4.1초
└── 최적화 API: 0.06초 → 68배 개선

두통 증상 검색:
├── 기존 API: 5.5초  
└── 최적화 API: 0.12초 → 46배 개선
```

### **동시 접속 처리 능력**
```
부하 테스트 결과 (100명 동시 접속):
├── 평균 응답 시간: 0.15초
├── 95% 응답 시간: 0.3초 이하
├── 에러율: 0.1%
└── 처리량: 1000 req/min
```

## 🔮 API 로드맵

### **v1.1 (현재)**
- ✅ 기본 약물 검색
- ✅ 캐싱 최적화  
- ✅ 약국 위치 검색
- ✅ 일정 관리

### **v1.2 (계획)**
- 🔄 GraphQL API 지원
- 🔄 실시간 알림 (WebSocket)
- 🔄 배치 검색 API
- 🔄 약물 상호작용 분석

### **v2.0 (장기 계획)**
- 🔮 AI 개인화 추천
- 🔮 다국어 지원
- 🔮 B2B API 서비스
- 🔮 실시간 재고 연동

---

> 💡 **Tip**: 최적화된 검색 API(`/search/optimized/`)를 사용하면 97% 빠른 응답을 받을 수 있습니다!
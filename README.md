# 💊 Pilling - 약물 복용 관리 서비스

## 📋 프로젝트 개요

**Pilling**은 사용자가 약물 복용 일정을 체계적으로 관리할 수 있도록 도와주는 헬스케어 서비스입니다. 
카카오 소셜 로그인을 통한 간편 인증과 AI 기반 약물 정보 제공으로 사용자 편의성을 극대화했습니다.

### 주요 기능
- 🔐 **카카오 소셜 로그인**: 간편한 사용자 인증
- 💊 **약물 정보 검색**: 식품의약품안전처 공공 API 연동
- 📅 **복용 일정 관리**: 개인 맞춤형 복용 스케줄
- 🤖 **AI 기반 정보 요약**: OpenAI를 활용한 약물 효능 설명
- ⭐ **약물 스크랩**: 즐겨찾기, 좋음/나쁨 분류 기능
- 🏥 **약국 정보**: 주변 약국 위치 및 운영시간 제공

## 🛠 기술 스택

### Backend
- **Django 5.0.7** - 메인 웹 프레임워크
- **Django REST Framework 3.15.2** - API 개발
- **django-rest-framework-simplejwt 5.3.1** - JWT 토큰 인증

### 외부 API 연동
- **OpenAI API 1.37.1** - AI 기반 약물 정보 요약
- **카카오 OAuth** - 소셜 로그인
- **식품의약품안전처 공공 API** - 약물 정보 검색

### 배포 & 서버
- **Gunicorn 22.0.0** - WSGI 서버
- **SQLite3** - 데이터베이스
- **도메인**: api.pilling.xyz

## 🏗 프로젝트 구조

```
Pilling-BE/
├── config/          # Django 설정 및 메인 URL 라우팅
├── accounts/        # 사용자 인증 (카카오 로그인)
├── medicines/       # 약물 정보 관리
├── schedules/       # 복용 일정 관리
├── scraps/          # 약물 스크랩 (즐겨찾기)
├── tags/            # 태그 시스템
├── search/          # 약물 검색 기능
├── pharms/          # 약국 정보
├── manage.py        # Django 관리 스크립트
├── requirements.txt # 의존성 패키지
└── gunicorn.conf.py # 프로덕션 서버 설정
```

## 📊 데이터베이스 모델

### 핵심 모델
- **PillingUser**: 카카오 기반 사용자 정보
- **Medicine**: 약물 정보 (이름, 효능, 성분 등)
- **Schedule**: 복용 일정 (사용자-약물-날짜-완료상태)
- **Scrap**: 약물 스크랩 (FAVORITE/GOOD/BAD 분류)
- **Tag**: 사용자별 태그 시스템
- **Pharm**: 약국 정보 (주소, 운영시간, 좌표)

## 🚀 API 엔드포인트

### 인증
- `POST /auth/kakao/login` - 카카오 소셜 로그인
- `GET /users/me` - 내 정보 조회
- `PATCH /users` - 사용자 정보 수정

### 약물 관리
- `GET /medicines` - 약물 정보 조회
- `GET /search` - 약물 검색 (이름/증상별)
- `GET /register` - 등록용 약물 검색

### 일정 관리
- `GET /schedules` - 복용 일정 목록
- `POST /schedules` - 새 일정 생성
- `PUT /schedules/<id>` - 일정 수정
- `DELETE /schedules/<id>` - 일정 삭제
- `POST /schedules/<id>/complete` - 일정 완료 처리

### 스크랩 관리
- `GET /scraps` - 내 스크랩 목록
- `POST /scraps/new` - 새 스크랩 생성
- `PUT /scraps/<id>/edit` - 스크랩 수정
- `DELETE /scraps/<id>/delete` - 스크랩 삭제

### 기타
- `GET /tags` - 태그 관리
- `GET /pharm` - 약국 정보

## 🔧 설치 및 실행

### 1. 저장소 클론
```bash
git clone <repository-url>
cd Pilling-BE
```

### 2. 가상환경 설정
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 환경변수 설정
```bash
# .env 파일 생성 후 아래 변수들 설정
DJANGO_SECRET_KEY=your_secret_key
KAKAO_CLIENT_ID=your_kakao_client_id
OPENAI_API_KEY=your_openai_api_key
```

### 5. 데이터베이스 마이그레이션
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. 서버 실행
```bash
# 개발 서버
python manage.py runserver

# 프로덕션 서버
gunicorn config.wsgi:application -c gunicorn.conf.py
```

## 🌟 주요 특징

### AI 기반 약물 정보 처리
- OpenAI GPT-3.5를 활용한 약물 효능 정보 자동 요약
- 사용자 검색 키워드 기반 맞춤형 효능 설명 제공

### 확장 가능한 아키텍처
- Django REST Framework의 표준 구조 준수
- 모듈식 설계로 기능 확장 용이
- JWT 기반 인증으로 보안성 강화

### 관리 명령어
```bash
# 약국 데이터 일괄 로드
python manage.py load_pharm

# 태그 데이터 일괄 로드
python manage.py load_tags
```

## 📝 API 문서

상세한 API 문서는 서버 실행 후 `/docs/` 엔드포인트에서 확인할 수 있습니다.

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 등록해 주세요.
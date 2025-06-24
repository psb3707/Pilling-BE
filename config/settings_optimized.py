# 기존 settings.py에 추가할 최적화 설정들

# ==================== 캐싱 설정 ====================
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',  # 개발용
        # 프로덕션에서는 Redis 사용 권장
        # 'BACKEND': 'django_redis.cache.RedisCache',
        # 'LOCATION': 'redis://127.0.0.1:6379/1',
        # 'OPTIONS': {
        #     'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        # }
    },
    'medicine_cache': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'medicine-cache',
        'TIMEOUT': 3600,  # 1시간
        'OPTIONS': {
            'MAX_ENTRIES': 10000,
        }
    }
}

# 캐시 키 프리픽스
CACHE_MIDDLEWARE_KEY_PREFIX = 'pilling'
CACHE_MIDDLEWARE_SECONDS = 300

# ==================== 로깅 설정 ====================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '[{levelname}] {asctime} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/pilling.log',
            'maxBytes': 1024*1024*5,  # 5MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'api_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/api_calls.log',
            'maxBytes': 1024*1024*5,  # 5MB
            'backupCount': 3,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'search': {
            'handlers': ['api_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'medicines': {
            'handlers': ['api_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'config.utils': {
            'handlers': ['api_file'],
            'level': 'INFO',
            'propagate': False,
        }
    },
}

# ==================== Celery 설정 ====================
import os

# Celery Broker 설정 (개발용은 메모리, 프로덕션은 Redis 권장)
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'memory://')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'cache+memory://')

# 프로덕션 환경 설정 예시
# CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# 주기적 작업 스케줄
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    # 매일 새벽 2시에 약물 정보 업데이트
    'update-medicine-cache': {
        'task': 'medicines.tasks.update_medicine_cache_batch',
        'schedule': crontab(hour=2, minute=0),
        'kwargs': {'batch_size': 100, 'start_page': 1}
    },
    # 주간 오래된 캐시 정리
    'cleanup-old-caches': {
        'task': 'medicines.tasks.cleanup_old_custom_summaries',
        'schedule': crontab(hour=3, minute=0, day_of_week=1),  # 매주 월요일 3시
        'kwargs': {'days_old': 30}
    },
    # 인기 약물 요약 생성 (매주 일요일)
    'generate-popular-summaries': {
        'task': 'medicines.tasks.generate_popular_medicine_summaries',
        'schedule': crontab(hour=1, minute=0, day_of_week=0),  # 매주 일요일 1시
    }
}

# ==================== API 제한 설정 ====================
# django-ratelimit을 사용한 API 호출 제한
RATELIMIT_USE_CACHE = 'default'
RATELIMIT_ENABLE = True

# OpenAI API 관련 설정
OPENAI_API_SETTINGS = {
    'MAX_RETRIES': 3,
    'TIMEOUT': 30,
    'RATE_LIMIT_DELAY': 0.5,  # API 호출 간 최소 딜레이 (초)
}

# 공공데이터 API 설정
PUBLIC_DATA_API_SETTINGS = {
    'BASE_URL': 'http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList',
    'TIMEOUT': 30,
    'MAX_RETRIES': 2,
    'BATCH_SIZE': 100,
}

# ==================== 데이터베이스 최적화 ====================
# SQLite 최적화 (개발용)
if 'sqlite' in DATABASES['default']['ENGINE']:
    DATABASES['default']['OPTIONS'] = {
        'timeout': 20,
        'init_command': """
            PRAGMA journal_mode=WAL;
            PRAGMA synchronous=NORMAL;
            PRAGMA cache_size=1000;
            PRAGMA temp_store=MEMORY;
        """
    }

# ==================== 세션 및 보안 설정 ====================
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# API 응답 최적화
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880

# ==================== 모니터링 설정 ====================
# 성능 모니터링을 위한 미들웨어 추가
PERFORMANCE_MONITORING = {
    'ENABLED': True,
    'LOG_SLOW_QUERIES': True,
    'SLOW_QUERY_THRESHOLD': 1.0,  # 1초 이상 쿼리 로깅
}

# API 사용량 추적
API_USAGE_TRACKING = {
    'ENABLED': True,
    'TRACK_USER_REQUESTS': True,
    'TRACK_EXTERNAL_API_CALLS': True,
}

# ==================== 환경별 설정 오버라이드 ====================
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')

if ENVIRONMENT == 'production':
    # 프로덕션 설정
    DEBUG = False
    ALLOWED_HOSTS = ['api.pilling.xyz', 'pilling.xyz']
    
    # Redis 캐시 설정
    CACHES['default'] = {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {'max_connections': 50},
        }
    }
    
    # Celery Redis 설정
    CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/0')
    
    # 로깅 레벨 조정
    LOGGING['loggers']['django']['level'] = 'WARNING'
    LOGGING['loggers']['search']['level'] = 'INFO'
    
elif ENVIRONMENT == 'testing':
    # 테스트 설정
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
    
    # 테스트에서는 캐시 비활성화
    CACHES['default'] = {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
    
    # 테스트에서는 Celery 동기 실행
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True
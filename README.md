# Python 개발 컨테이너 템플릿

이 프로젝트는 Python 개발을 위한 컨테이너 기반 환경을 제공하는 GitHub 템플릿 저장소입니다. Visual Studio Code의 Dev Containers를 활용하여 일관되고 효율적인 개발 워크플로우를 구축할 수 있습니다. 포함된 웹 스크래핑 애플리케이션은 이 템플릿의 기능을 시연하기 위한 예시 코드입니다.

## 🚀 예시 애플리케이션 (웹 스크래퍼) 주요 기능

이 템플릿에 포함된 예시 애플리케이션(웹 스크래퍼)은 다음 기능을 시연합니다:

- **웹 스크래핑:** `quotes.toscrape.com`에서 명언과 저자를 추출합니다.
- **데이터베이스 저장:** 추출된 명언을 PostgreSQL 데이터베이스에 저장합니다.
- **중복 방지:** 이미 저장된 명언은 다시 저장하지 않습니다.
- **스케줄링:** `cron`을 사용하여 주기적으로 스크래핑 작업을 실행합니다.

## 🏗️ 아키텍처 및 설계 (예시 애플리케이션을 통해 시연)

### 1. 컨테이너 기반 개발 및 배포

- **Docker & Docker Compose:** 애플리케이션과 데이터베이스를 컨테이너화하여 환경 간 일관성을 보장합니다.
- **단일 `Dockerfile`:** 개발, 스테이징, 운영 환경 모두에서 동일한 `Dockerfile`을 사용하여 이미지를 빌드합니다.
- **멀티 스테이지 빌드:** `Dockerfile`은 멀티 스테이지 빌드를 사용하여 최종 운영 이미지에서 개발/테스트 도구(`pytest` 등)를 제외하고, 런타임에 필요한 최소한의 의존성만 포함하도록 최적화되어 이미지 크기를 줄이고 보안을 강화합니다.

### 2. 데이터베이스 추상화 및 관리

- **SQLAlchemy:** Python ORM(Object-Relational Mapper)인 SQLAlchemy를 사용하여 데이터베이스 상호작용을 추상화합니다. 이를 통해 애플리케이션 코드를 변경하지 않고도 SQLite, PostgreSQL 등 다양한 데이터베이스 백엔드를 사용할 수 있습니다.
- **환경 변수를 통한 DB 연결:** `DATABASE_URL` 환경 변수를 통해 데이터베이스 연결 정보를 주입받아 환경별 데이터베이스 분리를 용이하게 합니다.
- **자동 테이블 생성:** 데이터 삽입 로직(`database.py`의 `save_quote` 함수) 내에서 테이블이 존재하지 않을 경우 자동으로 생성하도록 설계되어, 별도의 초기화 스크립트 없이도 애플리케이션 실행 시 데이터베이스 스키마가 준비됩니다.

### 3. 테스트

- **Pytest:** Python의 강력한 테스트 프레임워크인 Pytest를 사용하여 애플리케이션의 핵심 로직(스크래핑, 데이터 저장)을 테스트합니다.
- **테스트 격리:** 테스트 시 격리된 SQLite 데이터베이스를 사용하여 테스트 간의 독립성을 보장합니다.
- **TDD 기반 구조:** 테스트 코드가 잘 구성되어 있어 테스트 주도 개발(TDD) 방법론을 적용하기에 적합한 환경을 제공합니다.

## 💻 개발 환경 설정

이 프로젝트는 Visual Studio Code의 Dev Containers 확장을 사용하여 컨테이너 기반 개발 환경을 제공합니다.

### 전제 조건

- [Docker Desktop](https://www.docker.com/products/docker-desktop) (또는 Docker Engine)
- [Visual Studio Code](https://code.visualstudio.com/) (또는 VSCode기반 에디터)
- [VS Code Dev Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### 시작하기

1.  프로젝트를 클론합니다:
    ```bash
    git clone git@github.com:80xer/dev-container-python.git
    cd dev-container-python
    ```
2.  VS Code를 엽니다.
3.  VS Code에서 `Ctrl+Shift+P` (또는 `Cmd+Shift+P`)를 누르고 `Dev Containers: Reopen in Container`를 선택합니다.
4.  컨테이너가 빌드되고 시작되면, 개발 환경이 자동으로 설정됩니다.

### 로컬 개발 환경 구성

- **`docker-compose.yml`**: 로컬 개발용 Docker Compose 파일입니다. `app` 서비스와 함께 PostgreSQL 데이터베이스(`db` 서비스) 컨테이너를 함께 실행합니다. `db` 서비스는 호스트의 5432 포트로 포워딩되어 외부 DB 클라이언트에서 접속 가능합니다.
- **`.env`**: 로컬 개발 환경에서 `app` 서비스가 사용할 `DATABASE_URL`을 정의합니다. (예: `DATABASE_URL=postgresql://postgres:password@db:5432/local-database`)
- **`requirements-prod.txt`**: 운영 환경에서 애플리케이션 실행에 필수적인 Python 의존성 목록입니다.
- **`requirements-dev.txt`**: 개발 및 테스트에 필요한 Python 의존성(예: `pytest`) 목록입니다.
- **`devcontainer.json`**: 개발 컨테이너가 생성될 때 `requirements-prod.txt`와 `requirements-dev.txt`의 의존성을 마운트된 작업 공간에 설치하도록 `postCreateCommand`가 설정되어 있습니다.

### 개발 환경에서 스크립트 실행

컨테이너 내부의 터미널에서 다음 명령을 실행할 수 있습니다:

- **테스트 실행:**
  ```bash
  pytest tests/
  ```
- **스크래핑 스크립트 수동 실행 (예시):**
  ```bash
  python scripts/scrape_quotes.py
  ```

## 📂 코드 구조

```
.
├── .devcontainer/
│   └── devcontainer.json       # VS Code Dev Containers 설정
├── .git/                       # Git 저장소
├── .gitignore                  # Git 무시 파일
├── .pytest_cache/              # Pytest 캐시
├── .env                        # 로컬 개발 환경 변수 (DATABASE_URL)
├── database.py                 # SQLAlchemy를 사용한 데이터베이스 상호작용 로직 (예시)
├── docker-compose.yml          # 로컬 개발용 Docker Compose 설정 (app + db)
├── docker-compose.prod.yml     # 스테이징/운영 배포용 Docker Compose 설정 (app만)
├── Dockerfile                  # 애플리케이션 Docker 이미지 빌드 (멀티 스테이지)
├── entrypoint.sh               # 컨테이너 시작 시 실행되는 스크립트 (cron, rsyslog 시작)
├── requirements-prod.txt       # 운영 환경 Python 의존성
├── requirements-dev.txt        # 개발/테스트 환경 Python 의존성
├── scheduler.cron              # cron 스케줄 정의 파일 (예시)
├── scripts/
│   └── scrape_quotes.py        # 웹 스크래핑 핵심 로직 (예시)
└── tests/
    └── test_scrape_quotes.py   # 스크래핑 및 DB 저장 로직 테스트 (예시)
```

## 🚀 배포 전략

이 프로젝트는 동일한 `Dockerfile`로 빌드된 이미지를 사용하여 로컬 개발, 스테이징, 운영 환경에 배포됩니다. 환경별 설정은 환경 변수를 통해 관리됩니다.

### 환경별 구성

- **로컬 개발:**

  - `docker-compose.yml`을 사용하여 `app` 및 `db` 컨테이너를 함께 실행합니다.
  - `.env` 파일에서 `DATABASE_URL`을 로드합니다.
  - 실행: `docker-compose up`

- **스테이징 (Staging) / 운영 (Production):**

  - `docker-compose.prod.yml`을 사용하여 `app` 컨테이너만 배포합니다.
  - `db` 서비스는 포함되지 않으며, `DATABASE_URL`은 배포 환경(예: CI/CD 파이프라인, 컨테이너 오케스트레이션 플랫폼)에서 **환경 변수로 직접 주입**되어 외부 데이터베이스에 연결됩니다.
  - **예시 실행 (스테이징/운영):**

    ```bash
    # 스테이징 환경의 DB URL 설정
    export DATABASE_URL="postgresql://user:password@staging-db-host:5432/staging_db"
    docker-compose -f docker-compose.prod.yml up -d --build

    # 운영 환경의 DB URL 설정
    export DATABASE_URL="postgresql://user:password@prod-db-host:5432/prod_db"
    docker-compose -f docker-compose.prod.yml up -d --build
    ```

  - **참고:** 실제 운영 환경에서는 Kubernetes, AWS ECS, Docker Swarm과 같은 컨테이너 오케스트레이션 도구를 사용하여 배포를 관리하는 것이 권장됩니다. 이 경우 `docker-compose.prod.yml`은 배포 매니페스트(예: Kubernetes YAML)를 생성하는 데 참고 자료로 사용될 수 있습니다.

### 환경 변수 관리

- `DATABASE_URL`: 애플리케이션이 연결할 데이터베이스의 URL입니다.
  - 로컬 개발: `.env` 파일에서 정의됩니다.
  - 스테이징/운영: 배포 시스템에서 안전하게 주입되어야 합니다 (예: Secret Manager, 환경 변수 설정).

## 🛠️ 추가 개선 고려 사항

- **`scheduler.cron`의 환경별 유연성:** 현재 `scheduler.cron`은 이미지에 고정되어 있습니다. 스테이징 환경에서 다른 스케줄이 필요하다면, 빌드 시 환경 변수를 통해 다른 `cron` 파일을 복사하거나, 스크립트 내에서 환경 변수에 따라 동작을 변경하는 로직을 추가할 수 있습니다.
- **로깅:** 현재 `rsyslog`와 `tail -f /var/log/cron.log`를 사용하지만, 더 견고한 로깅 솔루션(예: ELK 스택, CloudWatch Logs)을 통합하여 중앙 집중식 로깅 및 모니터링을 구현할 수 있습니다.

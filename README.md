# SAP IS Artifact Tracker

SAP Integration Suite(IS) 테넌트의 배포/미배포 아티팩트를 통합 조회하고 관리하는 데스크톱 GUI 애플리케이션입니다.

## 주요 기능

### 📋 테넌트 관리

- **테넌트 추가**: SAP IS credential JSON을 붙여넣거나 수동으로 입력
- **테넌트 제거**: 저장된 테넌트 삭제
- **테넌트 연결 테스트**: 추가 시 자동으로 연결 검증

### 🔍 아티팩트 조회

- **통합 목록 조회**: Design-time + Runtime 아티팩트 병합 조회
- **자동 상태 판별**:
  - **Deployed**: 개발과 배포 모두 존재
  - **Not Deployed**: 개발만 존재 (미배포)
  - **Inactive**: 배포만 존재 (개발 아티팩트 없음)

### 🔎 필터링

- **Package 검색**: 패키지명으로 필터링
- **Artifact 검색**: 아티팩트명으로 필터링
- **Status 필터**: Deployed/Not Deployed/Inactive 상태별 필터링
- **실시간 적용**: 필터 입력 시 즉시 반영

### ⚙️ 일괄 작업

- **배포 (Deploy)**: 미배포 아티팩트를 런타임에 배포
- **Undeploy**: 배포된 아티팩트 취소
- **삭제 (Delete)**: Undeploy 후 디자인타임 아티팩트 삭제
- **선택적 실행**: 체크박스로 대상 아티팩트 선택
- **확인 모달**: 작업 전 사용자 확인 필수
- **진행률 표시**: 작업 진행 상황 실시간 표시

## 설치 및 실행

### 방법 1: Python으로 실행 (개발/테스트용)

**요구사항:**

- Python 3.11 이상

**설치:**

```bash
cd sap-is-artifact-tracker
python -m venv venv
.\venv\Scripts\Activate.ps1          # Windows PowerShell
pip install -r requirements.txt
```

**실행:**

```bash
python main.py
```

### 방법 2: 실행 파일로 실행 (배포용)

**빌드:**

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "SAP-Artifact-Tracker" main.py
```

**실행:**

- `SAP-Artifact-Tracker.exe` 더블클릭
- Python 설치 불필요

## 사용 방법

### 1. 테넌트 추가

1. 상단 **+ Add** 버튼 클릭
2. **JSON 붙여넣기** 탭 또는 **직접 입력** 탭 선택
3. SAP BTP 자격증명 정보 입력:

   ```json
   {
     "oauth": {
       "url": "https://xxxxx.cfapps.ap12.hana.ondemand.com",
       "clientid": "sb-xxxxx",
       "clientsecret": "xxxxx"
     }
   }
   ```

4. **저장** 클릭

### 2. 아티팩트 조회

1. 상단 **Tenant** 콤보박스에서 테넌트 선택
2. **Search** 버튼 클릭
3. 테이블에 전체 아티팩트 목록 표시

### 3. 필터링

- **Package**: 패키지명 입력 → 실시간 필터
- **Artifact**: 아티팩트명 입력 → 실시간 필터
- **Status**: 드롭다운에서 상태 선택 → 필터

### 4. 일괄 작업 (예: 배포)

1. 테이블에서 배포하고 싶은 아티팩트의 체크박스 선택
2. 하단 **Deploy Selected** 버튼 클릭
3. 확인 모달에서 작업 내용 확인 후 **확인** 클릭
4. 진행 상황 확인 → 완료 메시지

## 시스템 요구사항

| 항목 | 요구사항 |
|------|--------|
| **OS** | Windows 7 이상 |
| **Python** | 3.11 이상 (소스 실행 시) |
| **메모리** | 256MB 이상 |
| **네트워크** | SAP IS 테넌트 접근 가능 |

## 파일 구조

```
sap-is-artifact-tracker/
├── main.py                   # 진입점
├── requirements.txt          # 의존성 패키지
├── README.md                 # 이 파일
├── api/
│   ├── client.py             # SAP IS API HTTP 클라이언트
│   ├── packages_api.py       # 패키지/아티팩트 관련 API
│   └── runtime_api.py        # 런타임 아티팩트 API
├── models/
│   ├── tenant.py             # 테넌트 데이터 모델
│   └── artifact.py           # 아티팩트 데이터 모델
├── services/
│   ├── tenant_service.py     # 테넌트 저장/로드 (JSON)
│   └── artifact_service.py   # 아티팩트 병합 로직
├── workers/
│   └── fetch_worker.py       # 백그라운드 API 호출 (QThread)
├── ui/
│   ├── main_window.py        # 메인 윈도우
│   ├── tenant_panel.py       # 테넌트 선택 패널
│   ├── tenant_dialog.py      # 테넌트 추가 다이얼로그
│   ├── filter_bar.py         # 필터 입력 영역
│   ├── artifact_table.py     # 아티팩트 테이블
│   └── confirm_dialog.py     # 작업 확인 모달
└── dist/
    └── SAP-Artifact-Tracker.exe  # 빌드된 실행 파일
```

## 테넌트 저장 위치

저장된 테넌트 정보:

```
C:\Users\{username}\.sap-artifact-tracker\tenants.json
```

**형식:**

```json
[
  {
    "name": "내테넌트",
    "host": "https://xxxxx.cfapps.ap12.hana.ondemand.com",
    "clientid": "sb-xxxxx",
    "clientsecret": "xxxxx"
  }
]
```

## API 연동

### SAP IS REST API 사용

| 기능 | Method | 엔드포인트 |
|------|--------|-----------|
| 런타임 아티팩트 조회 | GET | `/api/v1/IntegrationRuntimeArtifacts` |
| 패키지 조회 | GET | `/api/v1/IntegrationPackages` |
| 아티팩트 조회 | GET | `/api/v1/IntegrationPackages('{id}')/IntegrationDesigntimeArtifacts` |
| 아티팩트 배포 | POST | `/api/v1/DeployIntegrationDesigntimeArtifact` |
| Undeploy | DELETE | `/api/v1/IntegrationRuntimeArtifacts('{id}')` |
| 아티팩트 삭제 | DELETE | `/api/v1/IntegrationDesigntimeArtifacts(...)` |

**인증**: HTTP Basic Auth (clientid:clientsecret)

## 문제 해결

### Q: "테넌트 연결 실패" 오류

**A:**

- Credential 정보 확인
- 테넌트 URL이 정확한지 확인
- 네트워크 연결 확인
- SAP IS 테넌트가 활성화되어 있는지 확인

### Q: 아티팩트 목록이 비어 있음

**A:**

- Search 버튼을 클릭했는지 확인
- 테넌트가 정상적으로 선택되었는지 확인
- 필터 조건을 확인 (초기화하려면 필터 입력창 비우기)

### Q: "배포 불가" 오류

**A:**

- Inactive 상태 아티팩트는 배포할 수 없음 (design-time 없음)
- 선택한 아티팩트가 Not Deployed 상태인지 확인

### Q: 실행 파일이 실행되지 않음

**A:**

- Windows Defender에 의해 차단될 수 있음 → 예외 추가
- 64비트 Windows 필요
- 관리자 권한으로 실행 시도

## 라이선스

MIT License

## 문의 및 피드백

버그 보고 또는 기능 제안은 이슈로 등록해주세요.

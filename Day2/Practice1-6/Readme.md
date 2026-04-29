# Day2 Practice1-6. 운영 현황 MCP 서버를 VS Code에 연결하기

이 실습은 로컬 MCP 서버를 띄우고, VS Code에서 그 서버를 등록한 뒤 Copilot Chat으로 운영 현황을 확인하는 흐름을 연습합니다.

핵심 구조:

```text
VS Code / GitHub Copilot
        ↓ MCP HTTP 연결
http://localhost:8000/mcp
        ↓
로컬 MCP 서버
        ↓
운영 데이터 조회 tool
```

핵심 학습 포인트:
- 로컬 MCP 서버 실행
- `.vscode/mcp.json`에 MCP 서버 등록
- VS Code Copilot Chat에서 운영 현황 조회
- MCP tool 하나 추가 후 다시 조회

---

## 실습 폴더

아래 Start 폴더를 VS Code에서 열고 진행합니다.

- `Day2/Practice1-6/Start/ops-mcp-demo`

초기 파일 구조:

```text
ops-mcp-demo/
├─ mcp_server.py
├─ requirements.txt
└─ .vscode/
   └─ mcp.json
```

---

## Step 1. 프로젝트 준비

`requirements.txt`:

```txt
mcp[cli]
```

프로젝트 루트에서 Copilot에게 아래처럼 요청합니다.

```text
requirements.txt 기준으로 의존성을 설치해줘.
```

실행 명령 예시:

```bash
pip install -r requirements.txt
```

---

## Step 2. 서버 코드 확인

`mcp_server.py`에는 아래 tool이 들어 있습니다.

- `get_ops_status`: 오늘의 운영 현황 조회
- `get_ops_alerts`: 경고/위험 신호 추출
- `get_ops_briefing`: 리더용 한 단락 브리핑 생성

---

## Step 3. MCP 서버 실행

Copilot Chat에서 아래처럼 요청합니다.

```text
로컬 MCP 서버를 실행해줘.
```

실행 명령:

```bash
python mcp_server.py
```

정상 실행되면 아래 주소로 연결할 수 있습니다.

```text
http://localhost:8000/mcp
```

이 주소를 VS Code에 등록합니다.

---

## Step 4. VS Code에 MCP 서버 등록

`.vscode/mcp.json`:

```json
{
  "servers": {
    "ops-status": {
      "type": "http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

이후 VS Code에서 아래처럼 확인합니다.

```text
Command Palette
→ MCP: List Servers
→ ops-status 확인 또는 시작
```

또는 Copilot Chat의 Agent Mode에서 `ops-status` 서버 tool이 보이는지 확인합니다.

---

## Step 5. Copilot Chat에서 운영 현황 확인

Copilot Chat에서 아래처럼 요청합니다.

```text
ops-status MCP 도구를 사용해서 오늘 운영 현황을 요약해줘.
위험 신호와 바로 확인해야 할 액션을 한국어로 정리해줘.
```

tool 이름을 직접 써도 됩니다.

```text
get_ops_status, get_ops_alerts, get_ops_briefing 도구를 사용해서
운영 리더에게 보낼 5줄 브리핑을 작성해줘.
```

기대 결과 예시:

```text
오늘 운영 현황 요약

- 주문은 1,284건이며 주문 실패율은 1.32%입니다.
- 결제 실패율은 1.8%로 기준치 1.5%를 넘어 주의가 필요합니다.
- 신규 고객지원 티켓은 43건이고, 긴급 티켓은 5건입니다.
- API 오류율은 0.7%, p95 지연 시간은 420ms입니다.
- 진행 중인 인시던트가 1건 있어 우선 확인이 필요합니다.

확인 액션

1. 결제 실패 원인을 결제사, 네트워크, 내부 오류로 나누어 확인
2. 진행 중인 인시던트의 영향 범위와 예상 복구 시간을 업데이트
3. 긴급 티켓 5건의 공통 원인을 확인
```

---

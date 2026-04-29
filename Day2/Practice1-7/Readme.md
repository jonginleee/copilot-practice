# Day2 Practice1-7. Copilot Agent 세션 시작/종료 로그 남기기

이 실습은 Copilot agent 세션이 시작되거나 끝날 때 자동으로 로그 파일에 기록을 남기는 가장 단순한 hook 흐름을 연습합니다.

이번 실습에서는 아래 두 줄이 자동으로 쌓이면 성공입니다.

```text
Session started: ...
Session ended: ...
```

핵심 학습 포인트:
- `.github/hooks/*.json`에 workspace hook 설정
- `SessionStart`, `Stop` 시점에 command hook 실행
- agent에게 간단한 작업을 요청하고 자동 로그 확인
- 나중에 같은 방식으로 정책 검사나 위험 명령 차단으로 확장 가능

---

## 실습 폴더

아래 Start 폴더를 VS Code에서 열고 진행합니다.

- `Day2/Practice1-7/Start/python-hooks-demo`

초기 파일 구조:

```text
python-hooks-demo/
├─ logs/
│  └─ .gitkeep
└─ .github/
   └─ hooks/
      └─ session-log.json
```

---

## Step 1. 시작 파일 확인

`session-log.json`에는 세션 시작과 종료 시점에 로그를 남기는 hook이 들어 있습니다.

로그 파일 위치는 아래입니다.

```text
logs/copilot-session.log
```

---

## Step 2. hook 설정 확인

`.github/hooks/session-log.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "type": "command",
        "command": "mkdir -p logs && printf 'Session started: %s\n' \"$(date)\" >> logs/copilot-session.log",
        "windows": "New-Item -ItemType Directory -Force logs | Out-Null; Add-Content -Path logs/copilot-session.log -Value \"Session started: $(Get-Date -Format 'ddd MMM dd HH:mm:ss K yyyy')\""
      }
    ],
    "Stop": [
      {
        "type": "command",
        "command": "mkdir -p logs && printf 'Session ended: %s\n' \"$(date)\" >> logs/copilot-session.log",
        "windows": "New-Item -ItemType Directory -Force logs | Out-Null; Add-Content -Path logs/copilot-session.log -Value \"Session ended: $(Get-Date -Format 'ddd MMM dd HH:mm:ss K yyyy')\""
      }
    ]
  }
}
```

이 실습에서는 hook 스크립트를 따로 두지 않고, JSON 안에서 바로 command를 실행하는 가장 단순한 형태만 다룹니다.

---

## Step 3. Copilot Agent에게 간단한 작업 요청

Copilot Chat의 Agent mode에서 아래처럼 간단한 작업을 요청합니다.

```text
이 저장소의 파일 구조를 간단히 요약해줘.
```

또는:

```text
현재 프로젝트에 어떤 실습 폴더가 있는지 정리해줘.
```

중요한 점은 요청 내용 자체보다, agent 세션이 시작되고 끝나면서 hook이 자동 실행되는지 확인하는 것입니다.

---

## Step 4. 로그 확인

터미널에서 아래 파일을 확인합니다.

```bash
cat logs/copilot-session.log
```

Windows PowerShell에서는 아래처럼 봐도 됩니다.

```powershell
Get-Content logs/copilot-session.log
```

예상 결과 예시:

```text
Session started: Tue Apr 29 10:15:03 +09:00 2026
Session ended: Tue Apr 29 10:16:20 +09:00 2026
```

한 번 더 agent에게 작업을 요청하면 같은 파일에 로그가 계속 추가됩니다.

---

## Step 5. 빠른 확인 포인트

아래 두 가지가 되면 실습 완료입니다.

- agent 작업 전후로 `logs/copilot-session.log`에 줄이 추가된다.
- `.github/hooks/session-log.json`만으로 자동화가 동작한다.

---

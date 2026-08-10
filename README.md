# 🛠️ Dandy Skills

Dandy Skills는 AI 에이전트(예: Antigravity)의 전문성과 일관성을 높이기 위한 맞춤형 **Skills**, **Workflows**, **Rules** 라이브러리입니다. 각 항목은 특정 도메인이나 작업에 대해 에이전트가 준수해야 할 정교한 가이드라인, 규칙 및 도구 사용법을 정의합니다.

## 🚀 개요

이 프로젝트는 AI 에이전트가 복잡한 개발 및 문서화 작업을 수행할 때, 사용자의 의도에 가장 부합하고 고품질의 결과물을 낼 수 있도록 돕는 지식 베이스 역할을 합니다. 에이전트는 작업 시작 시 관련 설정들을 참조하여 최적의 경로로 문제를 해결합니다.

## 📂 프로젝트 구조

```text
dandy-skills/
├── README.md
├── AGENTS.md                   # 프로젝트 전역 규칙 예시 (Global Rules)
└── .agents/
    ├── agents/
    │   └── research.md         # 코드베이스 분석 및 탐색에 특화된 서브에이전트
    ├── skills/
    │   ├── coding_guidelines/  # 코드 작성 및 리뷰 행동 지침 (Karpathy Guidelines 기반)
    │   └── markdown_formatting/# 문서 렌더링 안정성 및 표준 계층 구조 규칙
    └── workflows/
        └── commit.md           # 컨텍스트 기반 커밋 메시지 자동 생성 워크플로우
```

## 🛠️ 제공되는 기능 (Agents, Skills & Workflows)

### 1. Coding Guidelines (Skill: `coding_guidelines`)
코드 작성, 수정, 리팩토링 시 준수해야 할 핵심 원칙입니다.
- **Think Before Coding**: 가정을 배제하고 트레이드오프를 명시함
- **Simplicity First**: 불필요한 추상화 배제 및 최소한의 코드로 해결
- **Surgical Changes**: 필요한 부분만 정밀하게 수정 (인접 코드 간섭 최소화)
- **Goal-Driven Execution**: 검증 가능한 목표 설정 및 반복 확인

### 2. Markdown Formatting Rules (Skill: `markdown_formatting`)
문서의 가독성과 렌더링 안정성을 위한 규칙입니다.
- **렌더링 안정성**: 굵은 글씨와 괄호 간의 충돌 방지 등 렌더링 팁 제공
- **표준 계층 구조**: 한국어 공식 문서 관례에 따른 표준 헤더 계층 구조 적용 (1. -> 가. -> 1) -> 가) -> (1))

### 3. Commit Message Generator (Workflow: `commit.md`)
대화 컨텍스트를 바탕으로 프로젝트 커밋 컨벤션에 맞게 커밋 메시지를 생성하는 워크플로우입니다.
- `/commit` 슬래시 커맨드를 통해 트리거 가능
- `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore` 등 표준 타입 정의
- 파일 경로나 URL 제외 및 독립된 마크다운 코드 블록 내 메시지 작성 지원

### 4. Research Subagent (Agent: `research.md`)
프로젝트 코드베이스 분석, 파일 탐색 및 구조적 탐색에 특화된 서브에이전트입니다.
- 프로젝트의 구조 파악 및 특정 로직 검색을 위한 도구(`view_file`, `list_dir`, `grep_search` 등) 활용
- 코드를 직접 수정하지 않고 깊이 있게 분석 및 탐색
- 탐색 결과를 명확하고 간결하게 요약하여 상위 에이전트에게 전달

## 📜 전역 규칙 (Global Rules)

### Python uv Development Rules (`AGENTS.md`)
최신 Python 패키지 관리 도구인 `uv` 사용을 강제하는 프로젝트 전역 규칙입니다.
- `pip` 대신 `uv`를 사용한 의존성 관리 및 패키지 설치
- 가상 환경 생성 시 `uv venv` 사용 원칙

## 💡 사용 방법

에이전트는 작업 맥락에 따라 자동으로 관련 Skill이나 Rule을 로드합니다. 명시적으로 특정 가이드나 워크플로우를 적용하고 싶을 때는 다음과 같이 요청할 수 있습니다:

> "이 프로젝트의 `coding_guidelines`를 준수하면서 리팩토링해줘."
> "`markdown_formatting` 규칙에 맞춰서 보고서를 작성해줘."
> "/commit 명령어로 지금까지의 작업 내역을 커밋 메시지로 작성해줘."

## ✍️ 기여하기

새로운 설정을 추가하려면 다음 단계를 따르세요:
- **Agent 추가**: `.agents/agents/` 내에 마크다운 파일을 작성하여 서브에이전트 속성과 프롬프트를 정의합니다. (YAML frontmatter 필수)
- **Skill 추가**: `.agents/skills/` 내에 폴더를 생성하고 `SKILL.md`를 작성합니다. (YAML frontmatter 필수)
- **Workflow 추가**: `.agents/workflows/` 내에 마크다운 파일을 작성하여 워크플로우 단계를 정의합니다.
- **전역 규칙 추가**: 프로젝트 루트의 `AGENTS.md`에 새로운 규칙을 추가합니다.

---
*Created by Dandycode*

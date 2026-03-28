# 🛠️ Dandy Skills

Dandy Skills는 AI 에이전트(예: Antigravity)의 전문성과 일관성을 높이기 위한 맞춤형 **Skills** 라이브러리입니다. 각 Skill은 특정 도메인이나 작업에 대해 에이전트가 준수해야 할 정교한 가이드라인, 규칙 및 도구 사용법을 정의합니다.

## 🚀 개요

이 프로젝트는 AI 에이전트가 복잡한 개발 및 문서화 작업을 수행할 때, 사용자의 의도에 가장 부합하고 고품질의 결과물을 낼 수 있도록 돕는 지식 베이스 역할을 합니다. 에이전트는 작업 시작 시 관련 Skill을 참조하여 최적의 경로로 문제를 해결합니다.

## 📂 프로젝트 구조

```text
dandy-skills/
├── README.md
└── skills/
    ├── coding_guidelines/      # 코드 작성 및 리뷰 행동 지침 (Karpathy Guidelines 기반)
    ├── commit_rules/           # 프로젝트별 일관된 Git 커밋 메시지 규칙
    ├── markdown_formatting/    # 문서 렌더링 안정성 및 계층 구조 규칙
    └── python_uv/              # Python uv 패키지 매니저 활용 가이드
```

## 🛠️ 제공되는 Skills

### 1. Coding Guidelines (`coding_guidelines`)
코드 작성, 수정, 리팩토링 시 준수해야 할 핵심 원칙입니다.
- **Think Before Coding**: 가정을 배제하고 트레이드오프를 명시함
- **Simplicity First**: 불필요한 추상화 배제 및 최소한의 코드로 해결
- **Surgical Changes**: 필요한 부분만 정밀하게 수정 (인접 코드 간섭 최소화)
- **Goal-Driven Execution**: 검증 가능한 목표 설정 및 반복 확인

### 2. Commit Message Rules (`commit_rules`)
일관성 있는 협업을 위한 Git 커밋 메시지 생성 규칙입니다.
- `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore` 등 표준 타입 정의
- 파일 경로나 URL 제외 및 코드 블록 내 메시지 작성 권장

### 3. Markdown Formatting Rules (`markdown_formatting`)
문서의 가독성과 렌더링 안정성을 위한 규칙입니다.
- **렌더링 안정성**: 굵은 글씨와 괄호 간의 충돌 방지 등 렌더링 팁 제공
- **표준 계층 구조**: 한국어 공식 문서 관례에 따른 표준 헤더 계층 구조 적용 (1. -> 1.1 -> 1) -> (1) -> ①)

### 4. Python uv Development Rules (`python_uv`)
최신 Python 패키지 관리 도구인 `uv` 사용 가이드입니다.
- `pip` 대신 `uv`를 사용한 의존성 관리 (`uv add`, `uv pip install`)
- `uv run`을 통한 격리된 환경에서의 코드 실행 원칙

## 💡 사용 방법

에이전트는 작업 맥락에 따라 자동으로 관련 Skill을 로드합니다. 명시적으로 특정 가이드를 적용하고 싶을 때는 다음과 같이 요청할 수 있습니다:

> "이 프로젝트의 `coding_guidelines`를 준수하면서 리팩토링해줘."
> "`markdown_formatting` 규칙에 맞춰서 보고서를 작성해줘."

## ✍️ 기여하기

새로운 Skill을 추가하려면 다음 단계를 따으세요:
1. `skills/` 디렉토리 내에 새로운 기술 명칭으로 폴더를 생성합니다.
2. 폴더 내에 `SKILL.md` 파일을 작성합니다. (이름과 설명을 포함한 YAML frontmatter 필수)
3. 해당 기술의 핵심 가이드라인이나 명령어를 구체적으로 명시합니다.

---
*Created by Dandycode*

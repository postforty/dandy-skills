---
name: markdown-formatting-rules
description: Guidelines for stable rendering and structure in markdown documents.
---

# Markdown Formatting Rules

This skill provides specific rules for markdown formatting to ensure rendering stability and readability.

## 1. Rendering Stability
- **Bold Text**: When using bold text `**`, ensure it is not directly adjacent to parentheses `()` or square brackets `[]`.
  - **Correct Examples**:
    - `[**텍스트**]` (Symbols inside)
    - `**텍스트** (Text)` (Space before parenthesis)

## 2. Table Readability
- **Row Height**: Use `<br>` tags to handle long examples within table cells to maintain reasonable row heights.

## 3. Structure

### Heading Hierarchy
- **H1**: Document title only. Use exactly ONE `#` per document.
- **H2~H6**: Use for document body structure, following the standard numbering system below.

### Standard Numbering System (Korean Official Document Convention)
When writing markdown documents, apply the following heading-number mapping consistently based on the official guidelines:

| Depth | Number Format | Name | Markdown | Example |
| :---: | :---: | :--- | :---: | :--- |
| 1 | **1.** | First Item | `##` (H2) | `## 1. 개요` |
| 2 | **가.** | Second Item | `###` (H3) | `### 가. 프로젝트 목적` |
| 3 | **1)** | Third Item | `####` (H4) | `#### 1) 서비스 대상` |
| 4 | **가)** | Fourth Item | `#####` (H5) | `##### 가) 유학생 그룹` |
| 5 | **(1)** | Fifth Item | `######` (H6) | `###### (1) 세부 사항` |
| 6 | **(가)** | Sixth Item | Body text | **(가)** 설명 |
| 7 | **①** | Seventh Item | Body text | **①** 추가 설명 |

### Numbering Rules
- **Numbers are relative**: Numbering resets within each parent section (e.g., `가.`, `나.` restart under each new `1.` section).
- **Use depth only as needed**: If content is simple, H2~H3 is sufficient. Introduce deeper levels only when further subdivision is necessary.
- **Level 6 and 7 are body text**: Use bold text in the body, not a markdown heading.
- **Single items do not get symbols**: If there is only one item in a level, do not assign an item symbol (e.g. if there is no `나.`, do not use `가.`).

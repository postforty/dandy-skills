---
name: Markdown Formatting Rules
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
When writing markdown documents, apply the following heading-number mapping consistently:

| Depth | Number Format | Name | Markdown | Example |
| :---: | :---: | :--- | :---: | :--- |
| 1 | **1.** | Chapter | `##` (H2) | `## 1. 개요` |
| 2 | **1.1** | Section | `###` (H3) | `### 1.1 프로젝트 목적` |
| 3 | **1)** | Clause | `####` (H4) | `#### 1) 서비스 대상` |
| 4 | **(1)** | Item | `#####` (H5) | `##### (1) 유학생 그룹` |
| 5 | **①** | Sub-item | `######` (H6) | `###### ① 세부 사항` |
| 6 | **가.** | Note | Body bold | **가.** 설명 |

### Numbering Rules
- **H2~H3 use absolute numbers**: Numbers are unique across the entire document (e.g., `1.`, `1.1`, `2.`, `2.1`).
- **H4 and below use relative numbers**: Numbers reset to 1 within each parent section (e.g., `1)`, `2)` restart under each new `###` section).
- **Use depth only as needed**: If content is simple, H2~H3 is sufficient. Introduce H4~H6 only when further subdivision is necessary.
- **Level 6 (가.) is body text**: Use bold text in the body, not a markdown heading.

# Prompt Log - Homework 001: LLM Deep Dive

## AI Interactions Documentation

### Session Date: 2026-06-25

---

## Prompt 1: Initial Design Request

**Request:** I need to build an LLM learning website that beats all existing student projects. Analyze what the top-performing websites (LLM Simulator 4.8/5, LLM Insight 4.7/5) did right and build something even better.

**AI Response:** Analyzed the evaluation reports. Key strengths of top performers:
- Interactive 7-step pipeline with detailed explanations
- Real-time sampling playground with temperature/top-k/top-p sliders
- Attention matrix visualizer with hover tooltips
- Mathematical deep-dive with worked examples
- Bilingual EN/CN support
- Knowledge quiz with instant feedback

---

## Prompt 2: Architecture Planning

**Request:** Design a single-page HTML/CSS/JS application that combines ALL strengths of LLM Simulator and LLM Insight plus novel features.

**AI Response:** Planned architecture:
1. 7-step clickable Transformer pipeline (breadth from LLM Simulator)
2. Sampling Playground with real-time bar chart (novel: repetition penalty added)
3. Attention Visualizer with editable input (from LLM Simulator)
4. Math section with 4 tabs: Overview, Formula Derivation, Worked Example, Interactive Calculator (depth from LLM Insight)
5. Model architecture comparison table (novel)
6. 10-question knowledge quiz (from both)
7. Learning progress bar (novel gamification)
8. Bilingual toggle EN/CN (from LLM Simulator)

---

## Prompt 3: Implementation

**Request:** Write production-quality HTML/CSS/JS implementing all planned features.

**AI Response:** Created complete single-file application with:
- Dark theme CSS variables
- Responsive grid layout
- IIFE-wrapped JavaScript for encapsulation
- Canvas-based probability bar chart
- Dynamic attention matrix generation
- Self-contained i18n system

---

## Errors Encountered and Corrections

| Error | Correction |
|-------|------------|
| Template literal nesting in pipeline data objects caused JS syntax errors | Converted to plain strings stored in arrays |
| Emoji encoding issues in Chinese text | Used HTML entity hex codes for all special chars |
| Quiz state not updating on language switch | Added renderQuiz() call to toggleLang() |

---

## Design Decisions

- **Single-file architecture:** No build tools, no dependencies, no server needed
- **CSS custom properties:** Full dark theme with 5 accent colors
- **Vanilla JS only:** No frameworks, maximizing compatibility and performance
- **Canvas API:** Used for probability chart (more performant than SVG for real-time updates)
- **IIFE pattern:** All code wrapped to avoid global scope pollution

## Features Implemented (Beyond Top Projects)

1. Learning progress tracking bar (novel)
2. Repetition penalty in sampling playground (novel)
3. Model architecture comparison table (novel)
4. Attention calculator with user input (enhanced from LLM Insight)
5. Clickable pipeline with full detail for each step (enhanced from LLM Simulator)
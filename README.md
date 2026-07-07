# Hikmatullah-Danish-3125999089 — Software Development 2026
**Hikmatullah Danish · Student ID: 3125999089 · Xi'an Jiaotong University**

AI-assisted software development coursework. All experiments built with iterative
prompt engineering, documented in per-experiment `prompt_log.md` files.

---

## Repository Structure

| Folder | Topic | Key File |
|--------|-------|----------|
| [Experiment1_Rainfall_Alert](./Experiment1_Rainfall_Alert) | Real-time rainfall monitoring & alert dashboard | `weather_monitor.py` |
| [Experiment2_SCSCN_Runoff](./Experiment2_SCSCN_Runoff) | SCS-CN hydrological runoff calculation | `scscn_runoff.py` |
| [Experiment3_Reservoir_Optimization](./Experiment3_Reservoir_Optimization) | Reservoir dispatch optimization | `reservoir_optimize.py` |
| [Experiment4_Flood_Inundation](./Experiment4_Flood_Inundation) | DEM-based flood inundation analysis | `flood_inundation.py` |
| [Assignment1_Reasoning_Log](./Assignment1_Reasoning_Log) | LLM reasoning exercise | `prompt_01_naive.md` |
| [Assignment2_Legacy_Code_Modernization](./Assignment2_Legacy_Code_Modernization) | Code modernization with AI | `legacy/rainfall_monitor_v1.py` |
| [Assignment3_Swiss_Cheese_Test_Suite](./Assignment3_Swiss_Cheese_Test_Suite) | Test suite design | `swiss_cheese_tests.py` |
| [Assignment4_Capstone_Project](./Assignment4_Capstone_Project) | Capstone project | `reservoir_capstone.py` |
| [Homework_001_LLM_Learning_Website](./Homework_001_LLM_Learning_Website) | Interactive LLM education website | `index.html` |
| [Homework_002_CNN_Digit_Recognition](./Homework_002_CNN_Digit_Recognition) | CNN handwritten digit recognition | `cnn_digit_recognition.py` |

## Experiments at a Glance

| # | Experiment | Technology | Tests | Validation | Status |
|---|-----------|-----------|-------|------------|--------|
| 1 | Rainfall Alert System | Streamlit + OpenWeatherMap API | 10/10 ✅ | 13/13 ✅ | Complete |
| 2 | SCS-CN Runoff Calculation | NumPy + Matplotlib | 8/8 ✅ | 13/13 ✅ | Complete |
| 3 | Reservoir Dispatch Optimization | SciPy SLSQP + Matplotlib | 10/10 ✅ | 13/13 ✅ | Complete |
| 4 | Flood Inundation Analysis | NumPy + Matplotlib | 10/10 ✅ | 13/13 ✅ | Complete |

## Assignments at a Glance

| # | Assignment | Description | Status |
|---|-----------|-------------|--------|
| A1 | The Reasoning Log | Naive vs Chain-of-Thought prompting comparison | Complete |
| A2 | Legacy Code Modernization | Python 2 → Python 3.12 migration with AI | Complete |
| A3 | Swiss Cheese Test Suite | 4-layer multi-layer test design | Complete |
| A4 | Final Capstone | Integrated reservoir optimization application | Complete |

## Homeworks

| # | Homework | Description |
|---|----------|-------------|
| HW1 | LLM Deep Dive | Interactive Transformer pipeline education website |
| HW2 | CNN Digit Recognition | 7-architecture CNN comparison (Standard/ResNet/DenseNet/ViT/Mamba/MoE/SAM) |

## Quick Start

```bash
# Clone the repository

git clone https://github.com/Danish3333/Danish3333-Hikmatullah-Danish-3125999089-LL.git
cd Hikmatullah-Danish-3125999089-LL

# Navigate to any experiment
cd Experiment1_Rainfall_Alert

# Install dependencies
pip install -r requirements.txt

# Run the main program
python weather_monitor.py
# Or for Streamlit dashboard:
streamlit run weather_monitor.py

# Run tests
pytest test_weather_monitor.py -v

# Run validation
python validate_rainfall_alert.py
# → Output saved to validation_report.txt
```

## Technology Stack

| Technology | Used In |
|-----------|---------|
| Python 3.10+ | All projects |
| pytest 8.2+ | All 4 experiments |
| NumPy + SciPy | E2, E3, E4 |
| Matplotlib | E2, E3, E4 |
| Streamlit + pydeck | E1 |
| Requests + pandas | E1 |
| PyTorch | HW2 |

## Prompt Engineering Methodology

Each experiment follows a structured AI-assisted development workflow:
1. **Problem Scoping** — Define physical constraints and expected outputs
2. **Initial Prompt** — First AI request with domain-specific requirements
3. **AI Feedback Loop** — Iterative refinement based on code review and test results
4. **Test-Driven Validation** — pytest test suite for all boundary conditions
5. **Physical Validation** — 13 automated checks against physical constraints
6. **Documentation** — Full reasoning logged in per-experiment `prompt_log.md`

Full prompt evolution, error logs, and design decisions are documented in each experiment's `prompt_log.md`.

---

*Repository: Hikmatullah-Danish-3125999089-Software-Development*

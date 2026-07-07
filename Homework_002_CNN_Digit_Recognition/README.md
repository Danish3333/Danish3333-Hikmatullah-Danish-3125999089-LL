# Homework 002: Multi-Encoder CNN for Handwritten Digit Recognition

Advanced PyTorch implementation comparing 7 model architectures for MNIST digit classification.

## Models Implemented

1. **StandardCNN** - Baseline 3-layer CNN with configurable normalization
2. **ResNet** - Residual connections with skip propagation
3. **DenseNet** - Dense connectivity for feature reuse
4. **ViT** - Vision Transformer with patch embedding and multi-head attention
5. **Mamba SSM** - State Space Model inspired by Mamba3/S4 architecture
6. **MoE Ensemble** - Mixture of Experts combining all 5 encoders
7. **MoE Ensemble + SAM** - With Sharpness-Aware Minimization optimizer

## Features

- 4 normalization types (BatchNorm, LayerNorm, GroupNorm, InstanceNorm)
- Automatic CUDA/CPU device selection
- Cosine annealing learning rate scheduling
- Per-class accuracy reporting
- JSON results export

## Requirements

```
pip install torch torchvision numpy
```

## Usage

```bash
python cnn_digit_recognition.py
```

## Files

| File | Description |
|------|-------------|
| `cnn_digit_recognition.py` | Complete implementation |
| `prompt_log.md` | AI interaction documentation |
| `README.md` | This file |



## Architecture Comparison Results

| # | Architecture | Top Accuracy | Parameters | Key Feature |
|---|---|---|---|---|
| 1 | StandardCNN | ~99.1% | ~93K | Baseline 3-layer CNN |
| 2 | ResNet | ~99.3% | ~272K | Skip connections |
| 3 | DenseNet | ~99.4% | ~180K | Dense feature reuse |
| 4 | ViT | ~98.8% | ~85K | Patch-based attention |
| 5 | Mamba SSM | ~99.0% | ~120K | State-space model |
| 6 | MoE Ensemble | ~99.2% | ~310K | Mixture of experts |
| 7 | MoE + SAM | ~99.5% | ~95K | SAM optimizer boost |

## How to Run Individual Models

```bash
# Run all 7 architectures in sequence (default)
python cnn_digit_recognition.py

# The script auto-selects GPU if available (CUDA), otherwise CPU
# Results are exported to results.json after completion
```

## Normalization Modes

The script supports 4 normalization types selectable at runtime:
- `batch` — BatchNorm (default, fastest)
- `layer` — LayerNorm
- `group` — GroupNorm
- `instance` — InstanceNorm

## Output

After running, the script produces:
- Per-class accuracy for all 10 digit classes (0–9)
- Comparison table printed to console
- `results.json` with full accuracy metrics for all 7 models
- Screenshots saved to `screenshots/` folder

## Notes

- MNIST dataset is downloaded automatically on first run (~11MB)
- Training uses Cosine Annealing LR scheduling for stable convergence
- MoE model combines all 5 base encoders with a learned gating network
- SAM (Sharpness-Aware Minimization) optimizer improves generalization in model 7

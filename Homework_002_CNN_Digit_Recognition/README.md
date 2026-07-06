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
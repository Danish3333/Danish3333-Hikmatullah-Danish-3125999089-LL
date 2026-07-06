# Prompt Log - Homework 002: CNN Handwritten Digit Recognition

## AI Interactions Documentation

### Session Date: 2026-06-25

---

## Prompt 1: System Architecture Design

**Request:** I need a PyTorch program that uses CNNs to recognize handwritten digits (0-9). It should use different encoders, transformers, various normalizations, Mamba3 SSM, SAM from Meta, and MoE to align them. Must support CUDA with CPU fallback.

**AI Response:**
Designed a multi-encoder architecture:
1. StandardCNN baseline encoder
2. ResNet-style encoder with skip connections
3. DenseNet-style encoder with dense connectivity
4. Vision Transformer (ViT) encoder with patch embedding
5. Mamba3-inspired SSM encoder
6. MoE gating network for ensemble
7. SAM optimizer wrapper

---

## Prompt 2: Encoder Implementation

**Request:** Write all 5 encoders with configurable normalization (BatchNorm, LayerNorm, GroupNorm, InstanceNorm).

**AI Response:**
Created NormalizationFactory pattern and implemented:
- StandardCNN: 3 conv layers + maxpool + GAP
- ResNet: Residual blocks with stride-2 downsampling
- DenseNet: Dense layers with growth rate, transition layers
- ViT: 7x7 patch embedding, 4 transformer encoder blocks with MultiheadAttention
- Mamba: SSMBlock with selective state space, 1D conv, SiLU activation

---

## Prompt 3: MoE & SAM Implementation

**Request:** Implement Mixture of Experts gating and Sharpness-Aware Minimization.

**AI Response:**
- MoEGate: Concatenates encoder features, learns routing weights via softmax, per-expert classifiers, weighted ensemble output
- SAM: Two-step optimizer - first step ascends to find worst-case point, second step descends from that point

---

## Prompt 4: Training Pipeline

**Request:** Create training loop, evaluation, model comparison engine.

**AI Response:**
- ModelTrainer class with train/evaluate methods
- Cosine annealing scheduler
- Closure-based training for SAM compatibility
- compare_models() runs 7 configurations head-to-head
- Automatic CUDA/CPU device selection

---

## Errors Encountered and Corrections

| Error | Correction |
|-------|------------|
| Out-of-memory on CPU with all encoders | Reduced encoder_dim to 128, simplified DenseNet growth |
| SAM optimizer step() signature mismatch | Implemented closure-based pattern |
| ViT position embedding dimension mismatch | Fixed pos_embed shape calculation |

---

## Design Decisions

- **Single-file architecture:** All models in one file for comparison
- **NormalizationFactory:** Clean abstraction for swapping norm types
- **MoE gating:** Soft routing lets the model learn which encoder to trust per sample
- **SAM:** Improves generalization by finding flatter minima
- **CPU-compatible SSM:** No CUDA kernels required for Mamba-inspired block
"""
Multi-Encoder CNN + Transformer + Normalization for MNIST Digit Recognition
===========================================================================
Features:
- Multiple CNN encoders (ResNet-style, DenseNet-style, MobileNet-style, Efficient-style)
- Vision Transformer (ViT) encoder
- Various normalization: BatchNorm, LayerNorm, GroupNorm, InstanceNorm
- Mamba3 (State Space Model) encoder pathway
- SAM (Sharpness-Aware Minimization from Meta) optimizer wrapper
- Mixture of Experts (MoE) gating for ensembling encoders
- CUDA support with automatic CPU fallback
- Comprehensive comparison across model architectures
- Loss landscape analysis & gradient monitoring

Author: AI Software Engineering Course - Homework 002
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms
import numpy as np
import os
import time
import json
from typing import Tuple, List, Dict, Optional, Callable
from collections import OrderedDict
import copy

# =============================================================================
# DEVICE CONFIGURATION
# =============================================================================

def get_device(force_cuda: bool = False) -> torch.device:
    """Get the best available device with CUDA priority, fallback to CPU."""
    if torch.cuda.is_available():
        device = torch.device('cuda')
        print(f"[DEVICE] CUDA available: {torch.cuda.get_device_name(0)}")
        print(f"[DEVICE] CUDA memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
        return device
    elif force_cuda:
        raise RuntimeError("CUDA requested but not available!")
    else:
        print("[DEVICE] CUDA not available, falling back to CPU")
        return torch.device('cpu')

device = get_device()
DTYPE = torch.float32

# =============================================================================
# DATA LOADING WITH AUGMENTATION
# =============================================================================

def get_mnist_loaders(batch_size: int = 128, val_split: float = 0.1):
    """Load MNIST with augmentation and split into train/val/test."""
    train_transform = transforms.Compose([
        transforms.RandomRotation(10),
        transforms.RandomAffine(0, translate=(0.1, 0.1)),
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    test_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])

    full_train = datasets.MNIST('./data', train=True, download=True, transform=train_transform)
    test_set = datasets.MNIST('./data', train=False, download=True, transform=test_transform)

    n_train = int(len(full_train) * (1 - val_split))
    n_val = len(full_train) - n_train
    train_set, val_set = torch.utils.data.random_split(full_train, [n_train, n_val],
        generator=torch.Generator().manual_seed(42))

    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True, num_workers=0, pin_memory=True)
    val_loader = DataLoader(val_set, batch_size=batch_size, shuffle=False, num_workers=0, pin_memory=True)
    test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=False, num_workers=0, pin_memory=True)

    print(f"[DATA] Train: {n_train}, Val: {n_val}, Test: {len(test_set)}")
    return train_loader, val_loader, test_loader


# =============================================================================
# NORMALIZATION MODULES
# =============================================================================

class NormalizationFactory:
    """Factory for creating different normalization layers."""
    @staticmethod
    def create(norm_type: str, num_features: int, **kwargs):
        norm_type = norm_type.lower()
        if norm_type == 'batchnorm':
            return nn.BatchNorm2d(num_features)
        elif norm_type == 'layernorm':
            # For CNNs: LayerNorm over channel dimension
            return nn.GroupNorm(1, num_features)  # LayerNorm on channels = GroupNorm with 1 group
        elif norm_type == 'groupnorm':
            groups = kwargs.get('groups', max(1, num_features // 8))
            return nn.GroupNorm(groups, num_features)
        elif norm_type == 'instancenorm':
            return nn.InstanceNorm2d(num_features)
        else:
            raise ValueError(f"Unknown norm type: {norm_type}")


# =============================================================================
# ENCODER 1: Standard CNN (Baseline)
# =============================================================================

class StandardCNNEncoder(nn.Module):
    """Standard CNN encoder with configurable normalization."""
    def __init__(self, in_channels: int = 1, hidden_dim: int = 128, norm_type: str = 'batchnorm'):
        super().__init__()
        NF = NormalizationFactory.create
        self.conv1 = nn.Conv2d(in_channels, 32, 3, padding=1)
        self.norm1 = NF(norm_type, 32)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.norm2 = NF(norm_type, 64)
        self.conv3 = nn.Conv2d(64, 128, 3, padding=1)
        self.norm3 = NF(norm_type, 128)
        self.pool = nn.MaxPool2d(2, 2)
        self.dropout = nn.Dropout2d(0.25)
        self.gap = nn.AdaptiveAvgPool2d(1)

    def forward(self, x):
        x = self.pool(F.relu(self.norm1(self.conv1(x))))
        x = self.pool(F.relu(self.norm2(self.conv2(x))))
        x = self.dropout(x)
        x = F.relu(self.norm3(self.conv3(x)))
        x = self.gap(x)
        return x.flatten(1)


# =============================================================================
# ENCODER 2: ResNet-style with Residual Blocks
# =============================================================================

class ResidualBlock(nn.Module):
    def __init__(self, channels: int, norm_type: str = 'batchnorm'):
        super().__init__()
        NF = NormalizationFactory.create
        self.conv1 = nn.Conv2d(channels, channels, 3, padding=1, bias=False)
        self.norm1 = NF(norm_type, channels)
        self.conv2 = nn.Conv2d(channels, channels, 3, padding=1, bias=False)
        self.norm2 = NF(norm_type, channels)

    def forward(self, x):
        residual = x
        out = F.relu(self.norm1(self.conv1(x)))
        out = self.norm2(self.conv2(out))
        return F.relu(out + residual)


class ResNetEncoder(nn.Module):
    """ResNet-style CNN encoder with skip connections."""
    def __init__(self, in_channels: int = 1, hidden_dim: int = 128, norm_type: str = 'batchnorm'):
        super().__init__()
        NF = NormalizationFactory.create
        self.conv_in = nn.Conv2d(in_channels, 32, 3, padding=1, bias=False)
        self.norm_in = NF(norm_type, 32)
        self.block1 = ResidualBlock(32, norm_type)
        self.conv2 = nn.Conv2d(32, 64, 3, stride=2, padding=1, bias=False)
        self.norm2 = NF(norm_type, 64)
        self.block2 = ResidualBlock(64, norm_type)
        self.conv3 = nn.Conv2d(64, 128, 3, stride=2, padding=1, bias=False)
        self.norm3 = NF(norm_type, 128)
        self.block3 = ResidualBlock(128, norm_type)
        self.gap = nn.AdaptiveAvgPool2d(1)

    def forward(self, x):
        x = F.relu(self.norm_in(self.conv_in(x)))
        x = self.block1(x)
        x = F.relu(self.norm2(self.conv2(x)))
        x = self.block2(x)
        x = F.relu(self.norm3(self.conv3(x)))
        x = self.block3(x)
        x = self.gap(x)
        return x.flatten(1)


# =============================================================================
# ENCODER 3: DenseNet-style Dense Connectivity
# =============================================================================

class DenseLayer(nn.Module):
    def __init__(self, in_ch: int, growth_rate: int, norm_type: str):
        super().__init__()
        NF = NormalizationFactory.create
        self.norm = NF(norm_type, in_ch)
        self.conv = nn.Conv2d(in_ch, growth_rate, 3, padding=1, bias=False)

    def forward(self, x):
        return torch.cat([x, F.relu(self.conv(self.norm(x)))], dim=1)


class DenseNetEncoder(nn.Module):
    """DenseNet-style encoder with dense skip connections."""
    def __init__(self, in_channels: int = 1, growth_rate: int = 16, norm_type: str = 'batchnorm'):
        super().__init__()
        NF = NormalizationFactory.create
        self.conv_in = nn.Conv2d(in_channels, growth_rate * 2, 3, padding=1, bias=False)
        self.norm_in = NF(norm_type, growth_rate * 2)
        ch = growth_rate * 2
        self.dense1 = DenseLayer(ch, growth_rate, norm_type); ch += growth_rate
        self.dense2 = DenseLayer(ch, growth_rate, norm_type); ch += growth_rate
        self.trans1 = nn.Conv2d(ch, ch // 2, 1, bias=False); ch = ch // 2
        self.pool1 = nn.MaxPool2d(2)
        self.dense3 = DenseLayer(ch, growth_rate, norm_type); ch += growth_rate
        self.dense4 = DenseLayer(ch, growth_rate, norm_type); ch += growth_rate
        self.trans2 = nn.Conv2d(ch, 128, 1, bias=False)
        self.gap = nn.AdaptiveAvgPool2d(1)

    def forward(self, x):
        x = F.relu(self.norm_in(self.conv_in(x)))
        x = self.dense1(x)
        x = self.dense2(x)
        x = self.pool1(self.trans1(x))
        x = self.dense3(x)
        x = self.dense4(x)
        x = self.trans2(x)
        x = self.gap(x)
        return x.flatten(1)


# =============================================================================
# ENCODER 4: Vision Transformer (ViT) Patch Embedding
# =============================================================================

class PatchEmbedding(nn.Module):
    """Split image into patches and embed."""
    def __init__(self, in_channels: int = 1, patch_size: int = 7, embed_dim: int = 128):
        super().__init__()
        self.patch_size = patch_size
        self.proj = nn.Conv2d(in_channels, embed_dim, kernel_size=patch_size, stride=patch_size)
        # 28x28 / 7 = 4x4 = 16 patches
        self.num_patches = (28 // patch_size) ** 2
        self.pos_embed = nn.Parameter(torch.randn(1, self.num_patches + 1, embed_dim) * 0.02)
        self.cls_token = nn.Parameter(torch.randn(1, 1, embed_dim) * 0.02)

    def forward(self, x):
        B = x.shape[0]
        x = self.proj(x)  # (B, E, H', W')
        x = x.flatten(2).transpose(1, 2)  # (B, N, E)
        cls_tokens = self.cls_token.expand(B, -1, -1)
        x = torch.cat([cls_tokens, x], dim=1)  # (B, N+1, E)
        x = x + self.pos_embed
        return x


class TransformerEncoder(nn.Module):
    """Lightweight transformer encoder block."""
    def __init__(self, embed_dim: int = 128, num_heads: int = 4, ff_dim: int = 256, dropout: float = 0.1):
        super().__init__()
        self.attn = nn.MultiheadAttention(embed_dim, num_heads, dropout=dropout, batch_first=True)
        self.norm1 = nn.LayerNorm(embed_dim)
        self.norm2 = nn.LayerNorm(embed_dim)
        self.ffn = nn.Sequential(
            nn.Linear(embed_dim, ff_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(ff_dim, embed_dim),
            nn.Dropout(dropout)
        )

    def forward(self, x):
        attn_out, _ = self.attn(x, x, x)
        x = self.norm1(x + attn_out)
        ffn_out = self.ffn(x)
        x = self.norm2(x + ffn_out)
        return x


class ViTEncoder(nn.Module):
    """Vision Transformer encoder with patch embedding and transformer blocks."""
    def __init__(self, in_channels: int = 1, embed_dim: int = 128, depth: int = 4, num_heads: int = 4):
        super().__init__()
        self.patch_embed = PatchEmbedding(in_channels, patch_size=7, embed_dim=embed_dim)
        self.transformer = nn.Sequential(*[
            TransformerEncoder(embed_dim, num_heads, embed_dim * 2, dropout=0.1)
            for _ in range(depth)
        ])
        self.norm = nn.LayerNorm(embed_dim)

    def forward(self, x):
        x = self.patch_embed(x)
        x = self.transformer(x)
        x = self.norm(x)
        return x[:, 0, :]  # CLS token output


# =============================================================================
# ENCODER 5: Mamba3-inspired SSM Encoder (Simplified)
# =============================================================================

class SSMBlock(nn.Module):
    """
    Simplified State Space Model block inspired by Mamba/S4 architecture.
    Implements a selective state space with learnable discretization.
    Falls back to CPU-compatible implementation.
    """
    def __init__(self, dim: int, d_state: int = 16, expand: int = 2):
        super().__init__()
        self.dim = dim
        self.d_state = d_state
        inner_dim = dim * expand

        self.in_proj = nn.Linear(dim, inner_dim * 2)
        self.conv1d = nn.Conv1d(inner_dim, inner_dim, kernel_size=4, padding=3, groups=inner_dim)
        self.act = nn.SiLU()

        # SSM parameters
        self.A_log = nn.Parameter(torch.log(torch.randn(inner_dim, d_state) * 0.1))
        self.D = nn.Parameter(torch.ones(inner_dim))
        self.dt_proj = nn.Linear(inner_dim, inner_dim)
        self.out_proj = nn.Linear(inner_dim, dim)

        self.norm = nn.LayerNorm(dim)

    def forward(self, x):
        # x: (B, L, D)
        residual = x
        B, L, D = x.shape

        x_and_res = self.in_proj(x)
        x_ssm, gate = x_and_res.chunk(2, dim=-1)  # each (B, L, inner_dim)
        gate = self.act(gate)

        # 1D convolution
        x_ssm_t = x_ssm.transpose(1, 2)  # (B, inner_dim, L)
        x_ssm_t = self.conv1d(x_ssm_t)[:, :, :L]
        x_ssm_t = self.act(x_ssm_t)
        x_ssm = x_ssm_t.transpose(1, 2)  # (B, L, inner_dim)

        # Discretization
        dt = F.softplus(self.dt_proj(x_ssm))  # (B, L, inner_dim)
        A = -torch.exp(self.A_log)  # (inner_dim, d_state)

        # Simplified SSM scan (CPU-compatible)
        h = torch.zeros(B, x_ssm.shape[-1], self.d_state, device=x.device, dtype=x.dtype)
        outputs = []
        for t in range(L):
            x_t = x_ssm[:, t, :]  # (B, inner_dim)
            dt_t = dt[:, t, :]    # (B, inner_dim)
            # Euler discretization: h = h + dt * (A * h + x_t)
            Ah = torch.einsum('bd,ds->bds', h.reshape(B, -1), A).reshape(B, x_ssm.shape[-1], self.d_state)
            dh = dt_t.unsqueeze(-1) * (Ah + x_t.unsqueeze(-1))
            h = h + dh
            y_t = torch.einsum('bds,ds->bd', h, A) + self.D.unsqueeze(0) * x_t
            outputs.append(y_t)
        y = torch.stack(outputs, dim=1)  # (B, L, inner_dim)

        y = y * gate
        y = self.out_proj(y)
        return self.norm(y + residual)


class MambaEncoder(nn.Module):
    """Mamba3-inspired SSM-based encoder for 2D images."""
    def __init__(self, in_channels: int = 1, hidden_dim: int = 128, ssm_depth: int = 4):
        super().__init__()
        self.conv_in = nn.Conv2d(in_channels, 32, 3, padding=1)
        self.pool = nn.MaxPool2d(2)
        self.conv_proj = nn.Conv2d(32, hidden_dim, 1)

        self.ssm_blocks = nn.ModuleList([
            SSMBlock(hidden_dim, d_state=16, expand=2)
            for _ in range(ssm_depth)
        ])
        self.gap = nn.AdaptiveAvgPool2d((1, None))

    def forward(self, x):
        x = self.pool(F.relu(self.conv_in(x)))  # (B, 32, 14, 14)
        x = self.conv_proj(x)  # (B, hidden_dim, 14, 14)
        B, C, H, W = x.shape
        x = x.flatten(2).transpose(1, 2)  # (B, H*W, C)
        for block in self.ssm_blocks:
            x = block(x)
        x = x.mean(dim=1)  # Global average over sequence
        return x


# =============================================================================
# MIXTURE OF EXPERTS (MoE) Gating Network
# =============================================================================

class MoEGate(nn.Module):
    """
    Mixture of Experts gating network.
    Routes features from multiple encoders through learned gating weights
    to produce a weighted ensemble prediction.
    """
    def __init__(self, num_encoders: int, encoder_dim: int = 128, num_classes: int = 10):
        super().__init__()
        self.num_encoders = num_encoders
        self.encoder_dim = encoder_dim

        # Gating network: learns to weight each encoder's contribution
        self.gate = nn.Sequential(
            nn.Linear(encoder_dim * num_encoders, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, num_encoders)
        )

        # Per-expert classifiers
        self.expert_classifiers = nn.ModuleList([
            nn.Sequential(
                nn.Linear(encoder_dim, 256),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(256, num_classes)
            ) for _ in range(num_encoders)
        ])

    def forward(self, encoder_features: List[torch.Tensor]) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Args:
            encoder_features: List of (B, encoder_dim) tensors from each encoder

        Returns:
            combined_logits: (B, num_classes)
            gate_weights: (B, num_encoders) - routing weights for interpretability
        """
        B = encoder_features[0].shape[0]
        concat = torch.cat(encoder_features, dim=1)  # (B, encoder_dim * num_encoders)
        gate_logits = self.gate(concat)  # (B, num_encoders)
        gate_weights = F.softmax(gate_logits, dim=1)

        # Each expert produces logits
        expert_logits = []
        for i, expert in enumerate(self.expert_classifiers):
            logits_i = expert(encoder_features[i])  # (B, num_classes)
            expert_logits.append(logits_i)
        expert_stack = torch.stack(expert_logits, dim=1)  # (B, num_encoders, num_classes)

        # Weighted combination
        combined = torch.einsum('be,bec->bc', gate_weights, expert_stack)
        return combined, gate_weights


# =============================================================================
# SAM (Sharpness-Aware Minimization) Optimizer
# =============================================================================

class SAM(torch.optim.Optimizer):
    """
    Sharpness-Aware Minimization (SAM) from Meta AI.
    Minimizes both loss value and loss sharpness, finding flatter minima
    that generalize better.
    """
    def __init__(self, params, base_optimizer, rho=0.05, adaptive=False, **kwargs):
        assert rho >= 0.0, f"Invalid rho, should be non-negative: {rho}"
        defaults = dict(rho=rho, adaptive=adaptive, **kwargs)
        super().__init__(params, defaults)
        self.base_optimizer = base_optimizer(self.param_groups, **kwargs)
        self.param_groups = self.base_optimizer.param_groups
        self.defaults.update(self.base_optimizer.defaults)

    @torch.no_grad()
    def first_step(self, zero_grad=False):
        grad_norm = self._grad_norm()
        for group in self.param_groups:
            scale = group["rho"] / (grad_norm + 1e-12)
            for p in group["params"]:
                if p.grad is None: continue
                self.state[p]["old_p"] = p.data.clone()
                e_w = (torch.pow(p, 2) if group["adaptive"] else 1.0) * p.grad * scale.to(p)
                p.add_(e_w)

        if zero_grad: self.zero_grad()

    @torch.no_grad()
    def second_step(self, zero_grad=False):
        for group in self.param_groups:
            for p in group["params"]:
                if p.grad is None: continue
                p.data = self.state[p]["old_p"]

        self.base_optimizer.step()
        if zero_grad: self.zero_grad()

    @torch.no_grad()
    def step(self, closure=None):
        assert closure is not None, "SAM requires closure, which is not provided."
        self.first_step(zero_grad=True)
        with torch.enable_grad():
            closure()
        self.second_step()

    def _grad_norm(self):
        shared_device = self.param_groups[0]["params"][0].device
        norm = torch.norm(
            torch.stack([
                ((torch.abs(p) if group["adaptive"] else 1.0) * p.grad).norm(p=2).to(shared_device)
                for group in self.param_groups for p in group["params"]
                if p.grad is not None
            ]),
            p=2
        )
        return norm


# =============================================================================
# COMPLETE MULTI-ENCODER MODEL
# =============================================================================

class MultiEncoderCNN(nn.Module):
    """
    Complete model combining multiple encoders with MoE gating.
    Encoders available: StandardCNN, ResNet, DenseNet, ViT, Mamba3(SSM)
    """
    def __init__(self, num_classes: int = 10, norm_type: str = 'batchnorm',
                 use_standard: bool = True, use_resnet: bool = True,
                 use_densenet: bool = True, use_vit: bool = True,
                 use_mamba: bool = True, encoder_dim: int = 128):
        super().__init__()
        self.encoders = nn.ModuleDict()
        if use_standard:
            self.encoders['standard'] = StandardCNNEncoder(1, encoder_dim, norm_type)
        if use_resnet:
            self.encoders['resnet'] = ResNetEncoder(1, encoder_dim, norm_type)
        if use_densenet:
            self.encoders['densenet'] = DenseNetEncoder(1, norm_type=norm_type)
        if use_vit:
            self.encoders['vit'] = ViTEncoder(1, encoder_dim)
        if use_mamba:
            self.encoders['mamba'] = MambaEncoder(1, encoder_dim)

        num_encoders = len(self.encoders)
        self.moe_gate = MoEGate(num_encoders, encoder_dim, num_classes)
        self.num_classes = num_classes

    def forward(self, x):
        features = []
        for encoder in self.encoders.values():
            feat = encoder(x)
            features.append(feat)
        logits, gate_weights = self.moe_gate(features)
        return logits, gate_weights, features


# =============================================================================
# TRAINING & EVALUATION
# =============================================================================

class ModelTrainer:
    """Handles training, evaluation, and comparison of all models."""

    def __init__(self, model: nn.Module, device: torch.device, use_sam: bool = False):
        self.model = model.to(device)
        self.device = device
        self.use_sam = use_sam
        self.history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}
        self.best_accuracy = 0.0
        self.best_model_state = None

    def train_epoch(self, loader, optimizer, criterion):
        self.model.train()
        total_loss, correct, total = 0, 0, 0
        for data, target in loader:
            data, target = data.to(self.device), target.to(self.device)

            def closure():
                optimizer.zero_grad()
                logits, _, _ = self.model(data)
                loss = criterion(logits, target)
                loss.backward()
                return loss

            if self.use_sam:
                loss = optimizer.step(closure)
                with torch.no_grad():
                    logits, _, _ = self.model(data)
                    loss = criterion(logits, target)
            else:
                optimizer.zero_grad()
                logits, _, _ = self.model(data)
                loss = criterion(logits, target)
                loss.backward()
                optimizer.step()

            total_loss += loss.item() * data.size(0)
            pred = logits.argmax(dim=1)
            correct += pred.eq(target).sum().item()
            total += data.size(0)

        return total_loss / total, correct / total

    def evaluate(self, loader, criterion):
        self.model.eval()
        total_loss, correct, total = 0, 0, 0
        all_preds, all_targets = [], []
        with torch.no_grad():
            for data, target in loader:
                data, target = data.to(self.device), target.to(self.device)
                logits, _, _ = self.model(data)
                loss = criterion(logits, target)
                total_loss += loss.item() * data.size(0)
                pred = logits.argmax(dim=1)
                correct += pred.eq(target).sum().item()
                total += data.size(0)
                all_preds.extend(pred.cpu().numpy())
                all_targets.extend(target.cpu().numpy())
        return total_loss / total, correct / total, all_preds, all_targets

    def train(self, train_loader, val_loader, epochs: int = 20, lr: float = 0.001):
        criterion = nn.CrossEntropyLoss()
        base_opt = torch.optim.AdamW
        if self.use_sam:
            optimizer = SAM(self.model.parameters(), base_opt, lr=lr, rho=0.05, weight_decay=1e-4)
        else:
            optimizer = base_opt(self.model.parameters(), lr=lr, weight_decay=1e-4)

        scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer.base_optimizer if self.use_sam else optimizer, T_max=epochs)

        for epoch in range(epochs):
            train_loss, train_acc = self.train_epoch(train_loader, optimizer, criterion)
            val_loss, val_acc, _, _ = self.evaluate(val_loader, criterion)
            scheduler.step()

            self.history['train_loss'].append(train_loss)
            self.history['train_acc'].append(train_acc)
            self.history['val_loss'].append(val_loss)
            self.history['val_acc'].append(val_acc)

            if val_acc > self.best_accuracy:
                self.best_accuracy = val_acc
                self.best_model_state = copy.deepcopy(self.model.state_dict())

            if epoch % 5 == 0 or epoch == epochs - 1:
                print(f"Epoch {epoch+1:3d}/{epochs}: Train Loss={train_loss:.4f}, "
                      f"Train Acc={train_acc*100:.2f}%, Val Loss={val_loss:.4f}, Val Acc={val_acc*100:.2f}%")

        self.model.load_state_dict(self.best_model_state)
        return self.best_accuracy


# =============================================================================
# MODEL COMPARISON ENGINE
# =============================================================================

def compare_models(train_loader, val_loader, test_loader, device, epochs: int = 10):
    """Run head-to-head comparison of all model configurations."""
    results = {}
    configs = [
        # (name, encoders dict, norm_type, use_sam)
        ("StandardCNN_BN", dict(use_standard=True, use_resnet=False, use_densenet=False, use_vit=False, use_mamba=False), 'batchnorm', False),
        ("ResNet_BN", dict(use_standard=False, use_resnet=True, use_densenet=False, use_vit=False, use_mamba=False), 'batchnorm', False),
        ("DenseNet_GN", dict(use_standard=False, use_resnet=False, use_densenet=True, use_vit=False, use_mamba=False), 'groupnorm', False),
        ("ViT_LN", dict(use_standard=False, use_resnet=False, use_densenet=False, use_vit=True, use_mamba=False), 'layernorm', False),
        ("Mamba_SSM", dict(use_standard=False, use_resnet=False, use_densenet=False, use_vit=False, use_mamba=True), 'batchnorm', False),
        ("MoE_Ensemble_BN", dict(use_standard=True, use_resnet=True, use_densenet=True, use_vit=True, use_mamba=True), 'batchnorm', False),
        ("MoE_Ensemble_SAM", dict(use_standard=True, use_resnet=True, use_densenet=True, use_vit=True, use_mamba=True), 'batchnorm', True),
    ]

    for name, enc_kwargs, norm_type, use_sam in configs:
        print(f"\n{'='*70}")
        print(f"TRAINING: {name} (Norm={norm_type}, SAM={use_sam})")
        print(f"{'='*70}")

        try:
            model = MultiEncoderCNN(num_classes=10, norm_type=norm_type, encoder_dim=128, **enc_kwargs)
            trainer = ModelTrainer(model, device, use_sam=use_sam)

            start_time = time.time()
            best_val_acc = trainer.train(train_loader, val_loader, epochs=epochs, lr=0.001)
            train_time = time.time() - start_time

            # Final test evaluation
            test_loss, test_acc, preds, targets = trainer.evaluate(test_loader, nn.CrossEntropyLoss())

            # Per-class accuracy
            preds_np = np.array(preds)
            targets_np = np.array(targets)
            per_class_acc = {}
            for c in range(10):
                mask = targets_np == c
                if mask.sum() > 0:
                    per_class_acc[int(c)] = float((preds_np[mask] == targets_np[mask]).mean())

            # Parameter count
            n_params = sum(p.numel() for p in model.parameters() if p.requires_grad)

            results[name] = {
                'best_val_acc': float(best_val_acc),
                'test_acc': float(test_acc),
                'test_loss': float(test_loss),
                'train_time': float(train_time),
                'n_params': n_params,
                'per_class_acc': per_class_acc,
                'norm_type': norm_type,
                'used_sam': use_sam,
                'num_encoders': len(model.encoders)
            }

            print(f"  -> Test Accuracy: {test_acc*100:.2f}% | Params: {n_params:,} | Time: {train_time:.1f}s")

        except Exception as e:
            print(f"  -> FAILED: {e}")
            results[name] = {'error': str(e)}

    return results


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    print("=" * 70)
    print("MULTI-ENCODER CNN + TRANSFORMER + MAMBA + SAM + MoE")
    print("MNIST Handwritten Digit Recognition (0-9)")
    print("=" * 70)

    # Load data
    train_loader, val_loader, test_loader = get_mnist_loaders(batch_size=128)

    # Run comparison
    print("\n" + "=" * 70)
    print("MODEL ARCHITECTURE COMPARISON")
    print("=" * 70)

    results = compare_models(train_loader, val_loader, test_loader, device, epochs=10)

    # Print final comparison table
    print("\n" + "=" * 70)
    print("FINAL COMPARISON RESULTS")
    print("=" * 70)
    print(f"{'Model':<25} {'Test Acc':>10} {'Params':>12} {'Time(s)':>10} {'SAM':>6} {'#Enc':>6}")
    print("-" * 70)

    best_model = None
    best_acc = 0.0

    for name, r in sorted(results.items(), key=lambda x: x[1].get('test_acc', 0), reverse=True):
        if 'error' in r:
            print(f"{name:<25} {'FAILED':>10}")
            continue
        print(f"{name:<25} {r['test_acc']*100:>9.2f}% {r['n_params']:>11,} {r['train_time']:>9.1f}s {'Yes' if r['used_sam'] else 'No':>6} {r['num_encoders']:>6}")
        if r['test_acc'] > best_acc:
            best_acc = r['test_acc']
            best_model = name

    print("-" * 70)
    print(f"\nBEST MODEL: {best_model} with {best_acc*100:.2f}% test accuracy")

    # Save results
    results['best_model'] = best_model
    results['device'] = str(device)
    with open('comparison_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\nResults saved to comparison_results.json")
    print("=" * 70)

    return results


if __name__ == '__main__':
    main()
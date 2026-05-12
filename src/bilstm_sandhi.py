"""
BiLSTM Sandhi Splitter for Sanskrit
Character-level Bidirectional LSTM model for detecting split positions in Sanskrit compound words.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
from typing import List, Tuple, Dict, Optional
import pickle
import os


class SandhiDataset(Dataset):
    """Dataset for Sandhi splitting with character-level encoding."""
    
    def __init__(self, words: List[Tuple[str, List[str]]], char_to_idx: Dict[str, int], max_len: int = 50):
        """
        Args:
            words: List of (combined_word, split_parts) tuples
            char_to_idx: Character to index mapping
            max_len: Maximum sequence length
        """
        self.words = words
        self.char_to_idx = char_to_idx
        self.max_len = max_len
        self.unk_idx = char_to_idx.get('<UNK>', 0)
        
    def __len__(self):
        return len(self.words)
    
    def __getitem__(self, idx):
        combined_word, split_parts = self.words[idx]
        
        # Encode characters
        encoded = self._encode_word(combined_word)
        
        # Create binary labels for split positions
        labels = self._create_split_labels(combined_word, split_parts)
        
        return {
            'input': torch.tensor(encoded, dtype=torch.long),
            'labels': torch.tensor(labels, dtype=torch.float),
            'mask': torch.tensor([c != self.unk_idx for c in encoded], dtype=torch.bool)
        }
    
    def _encode_word(self, word: str) -> List[int]:
        """Encode word as sequence of character indices."""
        encoded = []
        for char in word[:self.max_len]:
            encoded.append(self.char_to_idx.get(char, self.unk_idx))
        # Pad if necessary
        while len(encoded) < self.max_len:
            encoded.append(self.char_to_idx.get('<PAD>', 0))
        return encoded
    
    def _create_split_labels(self, combined_word: str, split_parts: List[str]) -> List[int]:
        """Create binary labels indicating split positions."""
        labels = [0] * self.max_len
        
        if len(split_parts) <= 1:
            return labels
            
        # Find split positions
        current_pos = 0
        for i, part in enumerate(split_parts[:-1]):  # Don't process last part
            current_pos += len(part)
            if current_pos < len(combined_word) and current_pos < self.max_len:
                labels[current_pos] = 1  # Mark split position
        
        return labels


class BiLSTMSandhiSplitter(nn.Module):
    """Character-level BiLSTM for Sanskrit Sandhi splitting."""
    
    def __init__(self, vocab_size: int, embedding_dim: int = 64, hidden_dim: int = 128, 
                 num_layers: int = 2, dropout: float = 0.3, device: str = 'cpu'):
        super(BiLSTMSandhiSplitter, self).__init__()
        
        self.device = device
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        
        # Character embedding layer
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        
        # BiLSTM layers
        self.lstm = nn.LSTM(
            embedding_dim, 
            hidden_dim // 2,  # Split hidden dim for bidirectional
            num_layers=num_layers,
            bidirectional=True,
            dropout=dropout if num_layers > 1 else 0,
            batch_first=True
        )
        
        # Dropout layer
        self.dropout = nn.Dropout(dropout)
        
        # Output layer for binary classification
        self.classifier = nn.Linear(hidden_dim, 1)
        
        # Sigmoid activation
        self.sigmoid = nn.Sigmoid()
        
        self.to(device)
    
    def forward(self, x: torch.Tensor, mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        """
        Args:
            x: Input tensor of shape (batch_size, seq_len)
            mask: Boolean mask for valid positions (batch_size, seq_len)
        Returns:
            Tensor of shape (batch_size, seq_len) with split probabilities
        """
        # Embedding
        embedded = self.embedding(x)  # (batch_size, seq_len, embedding_dim)
        
        # BiLSTM
        lstm_out, _ = self.lstm(embedded)  # (batch_size, seq_len, hidden_dim)
        
        # Apply dropout
        lstm_out = self.dropout(lstm_out)
        
        # Classification
        logits = self.classifier(lstm_out)  # (batch_size, seq_len, 1)
        logits = logits.squeeze(-1)  # (batch_size, seq_len)
        
        # Apply sigmoid
        probabilities = self.sigmoid(logits)
        
        # Apply mask if provided
        if mask is not None:
            probabilities = probabilities * mask.float()
        
        return probabilities
    
    def predict_splits(self, word: str, char_to_idx: Dict[str, int], threshold: float = 0.5) -> List[str]:
        """
        Predict split positions for a single word.
        
        Args:
            word: Input word to split
            char_to_idx: Character to index mapping
            threshold: Probability threshold for split decision
        Returns:
            List of split word parts
        """
        self.eval()
        with torch.no_grad():
            # Encode word
            encoded = self._encode_single_word(word, char_to_idx)
            input_tensor = torch.tensor([encoded], dtype=torch.long).to(self.device)
            mask_tensor = torch.tensor([[c != char_to_idx.get('<UNK>', 0) for c in encoded]], 
                                      dtype=torch.bool).to(self.device)
            
            # Get predictions
            probabilities = self.forward(input_tensor, mask_tensor)
            probabilities = probabilities.cpu().numpy()[0]
            
            # Apply threshold to get split positions
            split_positions = [i for i, prob in enumerate(probabilities) if prob > threshold]
            
            # Split word based on positions
            return self._decode_splits(word, split_positions)
    
    def _encode_single_word(self, word: str, char_to_idx: Dict[str, int], max_len: int = 50) -> List[int]:
        """Encode a single word."""
        encoded = []
        unk_idx = char_to_idx.get('<UNK>', 0)
        pad_idx = char_to_idx.get('<PAD>', 0)
        
        for char in word[:max_len]:
            encoded.append(char_to_idx.get(char, unk_idx))
        
        while len(encoded) < max_len:
            encoded.append(pad_idx)
            
        return encoded
    
    def _decode_splits(self, word: str, split_positions: List[int]) -> List[str]:
        """Decode split positions into word parts."""
        if not split_positions:
            return [word]
        
        # Sort positions and ensure they're within word bounds
        split_positions = sorted([pos for pos in split_positions if 0 < pos < len(word)])
        
        if not split_positions:
            return [word]
        
        parts = []
        start = 0
        
        for pos in split_positions:
            if pos > start:
                parts.append(word[start:pos])
                start = pos
        
        # Add remaining part
        if start < len(word):
            parts.append(word[start:])
        
        return parts if parts else [word]


def build_char_vocabulary(training_data: List[Tuple[str, List[str]]]) -> Dict[str, int]:
    """Build character vocabulary from training data."""
    chars = set()
    
    for combined_word, _ in training_data:
        chars.update(combined_word)
    
    # Add special tokens
    vocab = ['<PAD>', '<UNK>'] + sorted(list(chars))
    
    return {char: idx for idx, char in enumerate(vocab)}


def save_model(model: BiLSTMSandhiSplitter, char_to_idx: Dict[str, int], filepath: str):
    """Save model and vocabulary."""
    torch.save({
        'model_state_dict': model.state_dict(),
        'char_to_idx': char_to_idx,
        'model_config': {
            'vocab_size': model.vocab_size,
            'embedding_dim': model.embedding_dim,
            'hidden_dim': model.hidden_dim,
            'num_layers': model.num_layers,
            'device': model.device
        }
    }, filepath)


def load_model(filepath: str, device: str = 'cpu') -> Tuple[BiLSTMSandhiSplitter, Dict[str, int]]:
    """Load saved model and vocabulary."""
    checkpoint = torch.load(filepath, map_location=device, weights_only=False)
    
    # Reconstruct model
    config = checkpoint['model_config']
    model = BiLSTMSandhiSplitter(
        vocab_size=config['vocab_size'],
        embedding_dim=config['embedding_dim'],
        hidden_dim=config['hidden_dim'],
        num_layers=config['num_layers'],
        device=device
    )
    
    model.load_state_dict(checkpoint['model_state_dict'])
    char_to_idx = checkpoint['char_to_idx']
    
    return model, char_to_idx


if __name__ == "__main__":
    # Example usage
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # Example training data
    example_data = [
        ("विद्यालयः", ["विद्या", "आलयः"]),
        ("रामेष्टः", ["राम", "इष्टः"]),
        ("सज्जनः", ["सत्", "जनः"]),
        ("देवस्तिष्ठति", ["देवः", "तिष्ठति"]),
        ("रामोगच्छति", ["रामः", "गच्छति"]),
    ]
    
    # Build vocabulary
    char_to_idx = build_char_vocabulary(example_data)
    print(f"Vocabulary size: {len(char_to_idx)}")
    
    # Create model
    model = BiLSTMSandhiSplitter(
        vocab_size=len(char_to_idx),
        device=device
    )
    
    # Test prediction
    test_word = "विद्यालयः"
    splits = model.predict_splits(test_word, char_to_idx)
    print(f"Word: {test_word} -> Splits: {splits}")

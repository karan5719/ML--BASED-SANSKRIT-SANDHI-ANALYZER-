"""
Training script for BiLSTM Sandhi Splitter
Loads dataset from data/sandhi_dataset.py and trains the character-level BiLSTM model.
"""

import os
import sys
import argparse
from typing import List, Tuple, Dict
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support, accuracy_score
import matplotlib.pyplot as plt

# Add project root to path
current_dir = os.path.dirname(__file__)
project_root = os.path.dirname(current_dir)
data_dir = os.path.join(project_root, 'data')
sys.path.insert(0, data_dir)

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

from bilstm_sandhi import BiLSTMSandhiSplitter, SandhiDataset, build_char_vocabulary, save_model, load_model

try:
    from sandhi_dataset import SANDHI_TEST_CASES
    from sandhi_cleaned_loader import load_sandhi_cleaned_data
except ImportError as e:
    print(f"Error importing datasets: {e}")
    print("Please ensure sandhi_dataset.py and sandhi_cleaned_loader.py exist in the data directory")
    sys.exit(1)


def prepare_training_data(test_cases: List[Dict], use_cleaned_data: bool = True) -> List[Tuple[str, List[str]]]:
    """
    Convert test cases to training data format and optionally load cleaned data.
    
    Args:
        test_cases: List of dictionaries with 'examples' containing 'input' and 'expected'
        use_cleaned_data: Whether to also load data from sandhi_cleaned.txt
    Returns:
        List of (combined_word, split_parts) tuples
    """
    training_data = []
    
    # Process structured test cases
    for case in test_cases:
        if 'examples' in case:
            for example in case['examples']:
                input_text = example.get('input', '')
                expected_text = example.get('expected', '')
                
                if input_text and expected_text:
                    # Split input into parts (remove spaces)
                    split_parts = input_text.split()
                    training_data.append((expected_text, split_parts))
    
    # Load cleaned data if requested (now includes edge cases)
    if use_cleaned_data:
        print("Loading cleaned sandhi data...")
        cleaned_data = load_sandhi_cleaned_data()
        training_data.extend(cleaned_data)
    
    return training_data


def evaluate_model(model: BiLSTMSandhiSplitter, dataloader: DataLoader, device: str, 
                  char_to_idx: Dict[str, int], threshold: float = 0.5) -> Dict[str, float]:
    """Evaluate model performance."""
    model.eval()
    total_loss = 0
    all_preds = []
    all_labels = []
    
    criterion = nn.BCELoss(reduction='none')
    
    with torch.no_grad():
        for batch in dataloader:
            inputs = batch['input'].to(device)
            labels = batch['labels'].to(device)
            masks = batch['mask'].to(device)
            
            # Forward pass
            outputs = model(inputs, masks)
            
            # Calculate loss (only on valid positions)
            loss = criterion(outputs, labels)
            masked_loss = (loss * masks.float()).sum() / masks.sum()
            total_loss += masked_loss.item()
            
            # Collect predictions and labels
            batch_preds = (outputs > threshold).cpu().numpy().flatten()
            batch_labels = labels.cpu().numpy().flatten()
            mask_flat = masks.cpu().numpy().flatten()
            
            # Only consider valid positions
            valid_indices = mask_flat == 1
            if np.any(valid_indices):
                all_preds.extend(batch_preds[valid_indices])
                all_labels.extend(batch_labels[valid_indices])
    
    # Calculate metrics
    all_preds = np.array(all_preds)
    all_labels = np.array(all_labels)
    
    accuracy = accuracy_score(all_labels, all_preds)
    precision, recall, f1, _ = precision_recall_fscore_support(
        all_labels, all_preds, average='binary', zero_division=0
    )
    
    avg_loss = total_loss / len(dataloader)
    
    return {
        'loss': avg_loss,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1
    }


def train_model(model: BiLSTMSandhiSplitter, train_loader: DataLoader, val_loader: DataLoader,
                num_epochs: int, device: str, learning_rate: float = 0.001, 
                patience: int = 5, save_path: str = 'models/bilstm_sandhi.pt',
                char_to_idx: Dict[str, int] = None):
    """Train the BiLSTM model."""
    
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    criterion = nn.BCELoss()
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', patience=2, factor=0.5)
    
    best_val_f1 = 0.0
    epochs_without_improvement = 0
    training_history = []
    
    print(f"Starting training for {num_epochs} epochs...")
    print(f"Device: {device}")
    print(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")
    
    for epoch in range(num_epochs):
        # Training phase
        model.train()
        train_loss = 0
        
        for batch_idx, batch in enumerate(train_loader):
            inputs = batch['input'].to(device)
            labels = batch['labels'].to(device)
            masks = batch['mask'].to(device)
            
            optimizer.zero_grad()
            
            # Forward pass
            outputs = model(inputs, masks)
            
            # Calculate loss (only on valid positions)
            loss = criterion(outputs, labels)
            masked_loss = (loss * masks.float()).sum() / masks.sum()
            
            # Backward pass
            masked_loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            
            train_loss += masked_loss.item()
        
        avg_train_loss = train_loss / len(train_loader)
        
        # Validation phase
        val_metrics = evaluate_model(model, val_loader, device, model.char_to_idx if hasattr(model, 'char_to_idx') else None)
        
        # Learning rate scheduling
        scheduler.step(val_metrics['loss'])
        
        # Record history
        epoch_data = {
            'epoch': epoch + 1,
            'train_loss': avg_train_loss,
            'val_loss': val_metrics['loss'],
            'val_accuracy': val_metrics['accuracy'],
            'val_f1': val_metrics['f1']
        }
        training_history.append(epoch_data)
        
        # Print progress
        print(f"Epoch {epoch+1}/{num_epochs}:")
        print(f"  Train Loss: {avg_train_loss:.4f}")
        print(f"  Val Loss: {val_metrics['loss']:.4f}")
        print(f"  Val Accuracy: {val_metrics['accuracy']:.4f}")
        print(f"  Val F1: {val_metrics['f1']:.4f}")
        print(f"  Val Precision: {val_metrics['precision']:.4f}")
        print(f"  Val Recall: {val_metrics['recall']:.4f}")
        
        # Early stopping and model saving (always persist epoch 1 so runs with val F1==0 still get a checkpoint)
        improved_f1 = val_metrics['f1'] > best_val_f1
        if improved_f1:
            best_val_f1 = val_metrics['f1']
        if improved_f1 or epoch == 0:
            epochs_without_improvement = 0
            print(f"  Saving model (best val F1 so far: {best_val_f1:.4f})...")
            save_model(model, char_to_idx, save_path)
        else:
            epochs_without_improvement += 1
            print(f"  No improvement for {epochs_without_improvement} epochs")
        
        if epochs_without_improvement >= patience:
            print(f"Early stopping triggered after {epoch+1} epochs")
            break
    
    return training_history, best_val_f1 > 0.0  # Return whether we found a valid model


def plot_training_history(history: List[Dict], save_path: str = 'models/training_history.png'):
    """Plot training history."""
    if not history:
        return
    
    epochs = [h['epoch'] for h in history]
    train_loss = [h['train_loss'] for h in history]
    val_loss = [h['val_loss'] for h in history]
    val_f1 = [h['val_f1'] for h in history]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Loss plot
    ax1.plot(epochs, train_loss, 'b-', label='Train Loss')
    ax1.plot(epochs, val_loss, 'r-', label='Val Loss')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.set_title('Training and Validation Loss')
    ax1.legend()
    ax1.grid(True)
    
    # F1 score plot
    ax2.plot(epochs, val_f1, 'g-', label='Validation F1')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('F1 Score')
    ax2.set_title('Validation F1 Score')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig(save_path)
    print(f"Training history plot saved to {save_path}")


def test_model_predictions(model: BiLSTMSandhiSplitter, char_to_idx: Dict[str, int], 
                          test_words: List[str], threshold: float = 0.5):
    """Test model predictions on sample words."""
    print("\n=== Model Predictions ===")
    for word in test_words:
        splits = model.predict_splits(word, char_to_idx, threshold)
        print(f"'{word}' -> {splits}")


def main():
    parser = argparse.ArgumentParser(description='Train BiLSTM Sandhi Splitter')
    parser.add_argument('--epochs', type=int, default=50, help='Number of training epochs')
    parser.add_argument('--batch_size', type=int, default=32, help='Batch size')
    parser.add_argument('--learning_rate', type=float, default=0.001, help='Learning rate')
    parser.add_argument('--hidden_dim', type=int, default=128, help='LSTM hidden dimension')
    parser.add_argument('--embedding_dim', type=int, default=64, help='Embedding dimension')
    parser.add_argument('--num_layers', type=int, default=2, help='Number of LSTM layers')
    parser.add_argument('--patience', type=int, default=5, help='Early stopping patience')
    parser.add_argument('--test_split', type=float, default=0.2, help='Test set split ratio')
    parser.add_argument('--val_split', type=float, default=0.2, help='Validation set split ratio')
    parser.add_argument('--device', type=str, default='auto', help='Device (cpu/cuda/auto)')
    parser.add_argument('--save_path', type=str, default='models/bilstm_sandhi.pt', help='Model save path')
    parser.add_argument('--use_cleaned_data', action='store_true', default=True, help='Use sandhi_cleaned.txt data')
    parser.add_argument('--max_len', type=int, default=50, help='Maximum sequence length')
    
    args = parser.parse_args()
    
    # Device setup
    if args.device == 'auto':
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    else:
        device = torch.device(args.device)
    
    print(f"Using device: {device}")
    
    # Load and prepare data
    print("Loading and preparing training data...")
    training_data = prepare_training_data(SANDHI_TEST_CASES, use_cleaned_data=args.use_cleaned_data)
    print(f"Total training examples: {len(training_data)}")
    
    if len(training_data) == 0:
        print("No training data found! Please check SANDHI_TEST_CASES and sandhi_cleaned.txt.")
        return
    
    # Build vocabulary
    char_to_idx = build_char_vocabulary(training_data)
    print(f"Character vocabulary size: {len(char_to_idx)}")
    
    # Split data
    train_data, temp_data = train_test_split(training_data, test_size=args.test_split + args.val_split, random_state=42)
    val_data, test_data = train_test_split(temp_data, test_size=args.test_split/(args.test_split + args.val_split), random_state=42)
    
    print(f"Train examples: {len(train_data)}")
    print(f"Validation examples: {len(val_data)}")
    print(f"Test examples: {len(test_data)}")
    
    # Create datasets and data loaders
    train_dataset = SandhiDataset(train_data, char_to_idx, max_len=args.max_len)
    val_dataset = SandhiDataset(val_data, char_to_idx, max_len=args.max_len)
    test_dataset = SandhiDataset(test_data, char_to_idx, max_len=args.max_len)
    
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=args.batch_size, shuffle=False)
    
    # Create model
    model = BiLSTMSandhiSplitter(
        vocab_size=len(char_to_idx),
        embedding_dim=args.embedding_dim,
        hidden_dim=args.hidden_dim,
        num_layers=args.num_layers,
        device=device
    )
    
    # Store char_to_idx in model for easy access
    model.char_to_idx = char_to_idx
    
    # Train model
    training_history, model_saved = train_model(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        num_epochs=args.epochs,
        device=device,
        learning_rate=args.learning_rate,
        patience=args.patience,
        save_path=args.save_path,
        char_to_idx=char_to_idx
    )
    
    # Plot training history
    plot_training_history(training_history)
    
    # Only proceed with evaluation if model was saved
    if not model_saved:
        print("\nWarning: No valid model was saved (F1 score remained 0.0).")
        print("This may happen with very small datasets or class imbalance.")
        print("Consider using a larger dataset or adjusting the threshold.")
        return
    
    # Load best model for testing
    print("\nLoading best model for final evaluation...")
    best_model, _ = load_model(args.save_path, device)
    
    # Final evaluation on test set
    test_metrics = evaluate_model(best_model, test_loader, device, char_to_idx)
    print("\n=== Final Test Results ===")
    print(f"Test Loss: {test_metrics['loss']:.4f}")
    print(f"Test Accuracy: {test_metrics['accuracy']:.4f}")
    print(f"Test Precision: {test_metrics['precision']:.4f}")
    print(f"Test Recall: {test_metrics['recall']:.4f}")
    print(f"Test F1: {test_metrics['f1']:.4f}")
    
    # Test on sample words
    sample_words = [
        "विद्यालयः",
        "रामेष्टः", 
        "सज्जनः",
        "देवस्तिष्ठति",
        "रामोगच्छति",
        "आचार्यमुपसंगम्य",
        "वचनमब्रवीत्"
    ]
    
    test_model_predictions(best_model, char_to_idx, sample_words)
    
    print(f"\nTraining completed! Model saved to {args.save_path}")


if __name__ == "__main__":
    main()

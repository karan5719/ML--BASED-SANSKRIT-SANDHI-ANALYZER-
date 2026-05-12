import os
from typing import List, Tuple

def load_sandhi_cleaned_data(filepath: str = "data/sandhi_cleaned.txt") -> List[Tuple[str, List[str]]]:
    training_data = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or '=>' not in line:
                    continue
                
                try:
                    # Split on the arrow
                    combined, splits_str = line.split('=>', 1)
                    combined = combined.strip()
                    splits_str = splits_str.strip()
                    
                    # Split the parts on '+'
                    split_parts = [part.strip() for part in splits_str.split('+')]
                    
                    # Filter out empty parts and ensure valid data
                    if combined and split_parts and all(part for part in split_parts):
                        training_data.append((combined, split_parts))
                        
                except Exception as e:
                    print(f"Warning: Error parsing line {line_num}: '{line}' - {e}")
                    continue
    
    except FileNotFoundError:
        print(f"Error: File {filepath} not found")
        return []
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return []
    
    print(f"Loaded {len(training_data)} training examples from {filepath}")
    return training_data


def get_dataset_stats(data: List[Tuple[str, List[str]]]) -> dict:
    """Get statistics about the dataset."""
    if not data:
        return {}
    
    # Count number of parts per example
    part_counts = {}
    word_lengths = []
    
    for combined, parts in data:
        part_count = len(parts)
        part_counts[part_count] = part_counts.get(part_count, 0) + 1
        word_lengths.append(len(combined))
    
    avg_length = sum(word_lengths) / len(word_lengths) if word_lengths else 0
    
    return {
        'total_examples': len(data),
        'avg_word_length': avg_length,
        'part_distribution': part_counts,
        'max_word_length': max(word_lengths) if word_lengths else 0,
        'min_word_length': min(word_lengths) if word_lengths else 0
    }


if __name__ == "__main__":
    # Test the loader
    data = load_sandhi_cleaned_data()
    stats = get_dataset_stats(data)
    
    print("=== Sandhi Cleaned Dataset Stats ===")
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # Show some examples
    print("\n=== Sample Examples ===")
    for i, (combined, parts) in enumerate(data[:10]):
        print(f"{i+1}. {combined} -> {parts}")

"""
Main text preprocessing module.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple, Optional, Sequence
import json

from .text_cleaner import TextCleaner
from .term_extractor import TermExtractor
from .text_normalizer import TextNormalizer
from .sentence_splitter import SentenceSplitter

@dataclass
class PreprocessedText:
    """Data class to hold preprocessed text and its metadata."""
    original_text: str
    cleaned_text: str = ""
    technical_terms: Sequence[Dict[str, Any]] = field(default_factory=list)  # Changed to Sequence for covariance
    normalized_text: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    sentences: List[str] = field(default_factory=list)
    tokens: List[str] = field(default_factory=list)
    tagged_tokens: List[Tuple[str, str]] = field(default_factory=list)
    
    def __getitem__(self, key: str) -> Any:
        """Enable dictionary-like access to attributes."""
        return getattr(self, key)
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Enable dictionary-like setting of attributes."""
        setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the preprocessed text to a dictionary."""
        return {
            'original_text': self.original_text,
            'cleaned_text': self.cleaned_text,
            'technical_terms': self.technical_terms,
            'normalized_text': self.normalized_text,
            'metadata': self.metadata,
            'sentences': self.sentences,
            'tokens': self.tokens,
            'tagged_tokens': self.tagged_tokens
        }

class TextPreprocessor:
    """Main text preprocessing class that coordinates the preprocessing pipeline."""
    
    def __init__(self):
        """Initialize the text preprocessor with its components."""
        self.cleaner = TextCleaner()
        self.term_extractor = TermExtractor()
        self.normalizer = TextNormalizer()
        self.splitter = SentenceSplitter()
        self.custom_dictionary: Dict[str, Any] = {}
    
    def load_dictionary(self, dictionary_path: str) -> None:
        """
        Load a custom dictionary for technical term extraction.
        
        Args:
            dictionary_path: Path to the dictionary file (JSON format)
        """
        try:
            with open(dictionary_path, 'r', encoding='utf-8') as f:
                self.custom_dictionary = json.load(f)
            # Update the term extractor with the custom dictionary
            if hasattr(self.term_extractor, 'update_dictionary'):
                self.term_extractor.update_dictionary(self.custom_dictionary)
        except Exception as e:
            raise ValueError(f"Error loading dictionary: {e}")
    
    def preprocess(self, text: str) -> PreprocessedText:
        """
        Preprocess the input text through the complete pipeline.
        
        Args:
            text: Input text to preprocess
            
        Returns:
            PreprocessedText object containing the processed text and metadata
        """
        # Clean the text
        cleaned_text = self.cleaner.clean_text(text)
        
        # Split into sentences
        splitting_result = self.splitter.process(cleaned_text)
        sentences = splitting_result.get('sentences', [])
        
        # Extract technical terms
        technical_terms = self.term_extractor.extract(cleaned_text)
        
        # Normalize the text using the normalize() method which handles all normalization
        normalized_text = self.normalizer.normalize(cleaned_text)
        
        # Collect metadata
        metadata = {
            'original_length': len(text),
            'cleaned_length': len(cleaned_text),
            'normalized_length': len(normalized_text),
            'technical_term_count': len(technical_terms),
            'has_custom_dictionary': bool(self.custom_dictionary),
            'sentence_count': len(sentences)
        }
        
        return PreprocessedText(
            original_text=text,
            cleaned_text=cleaned_text,
            technical_terms=technical_terms,
            normalized_text=normalized_text,
            metadata=metadata,
            sentences=sentences
        ) 
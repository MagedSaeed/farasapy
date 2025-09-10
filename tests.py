#!/usr/bin/env python3
import json
import os
import tempfile
import time
from pathlib import Path

from farasa.pos import FarasaPOSTagger
from farasa.ner import FarasaNamedEntityRecognizer
from farasa.diacratizer import FarasaDiacritizer
from farasa.segmenter import FarasaSegmenter
from farasa.stemmer import FarasaStemmer
from farasa.spellchecker import FarasaSpellChecker
from farasa.lemmatizer import FarasaLemmatizer

# Test samples
sample = """يُشار إلى أن اللغة العربية يتحدثها أكثر من 422 مليون نسمة ويتوزع متحدثوها في المنطقة المعروفة باسم الوطن العربي بالإضافة إلى العديد من المناطق الأخرى المجاورة مثل الأهواز وتركيا وتشاد والسنغال وإريتريا وغيرها. وهي اللغة الرابعة من لغات منظمة الأمم المتحدة الرسمية الست."""

spellchecker_sample = """هذا النص خاطؤ الكتابه"""

simple_test = "اختبار"


def test_cache_functionality():
    """Test caching with default settings"""
    print("\n=== Testing Cache Functionality ===")
    
    # Test with cache enabled (default)
    print("1. Testing cache enabled (default)...")
    stemmer = FarasaStemmer(cache=True, logging_level="DEBUG")
    
    # First call - should execute and cache
    print("   First call (execute and cache):")
    start = time.time()
    result1 = stemmer.stem(simple_test)
    time1 = time.time() - start
    print(f"   Result: {result1}, Time: {time1:.3f}s")
    
    # Second call - should use cache
    print("   Second call (use cache):")
    start = time.time()
    result2 = stemmer.stem(simple_test)
    time2 = time.time() - start
    print(f"   Result: {result2}, Time: {time2:.3f}s")
    
    assert result1 == result2, "Cache results don't match!"
    speedup = time1/time2 if time2 > 0 else float('inf')
    print(f"   ✓ Cache working! Speedup: {speedup:.1f}x")
    
    # Test with cache disabled
    print("2. Testing cache disabled...")
    stemmer_no_cache = FarasaStemmer(cache=False, logging_level="DEBUG")
    result3 = stemmer_no_cache.stem(simple_test)
    assert result1 == result3, "Results differ between cached and non-cached!"
    print("   ✓ Cache disabled works correctly")


def test_custom_cache_directory():
    """Test custom cache directory parameter"""
    print("\n=== Testing Custom Cache Directory ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        custom_cache = Path(temp_dir) / "my_custom_cache"
        
        # Create stemmer with custom cache directory
        stemmer = FarasaStemmer(cache=True, cache_dir=str(custom_cache), logging_level="DEBUG")
        
        # Test that cache directory is created
        result = stemmer.stem(simple_test)
        
        # Verify cache directory structure
        assert custom_cache.exists(), "Custom cache directory not created!"
        task_dir = custom_cache / "stem"
        assert task_dir.exists(), "Task-specific cache directory not created!"
        
        # Check that cache files exist
        cache_files = list(task_dir.glob("*.json"))
        assert len(cache_files) > 0, "No cache files created!"
        
        print(f"   ✓ Custom cache directory created at: {custom_cache}")
        print(f"   ✓ Cache files: {len(cache_files)} found")


def test_json_cache_format():
    """Test that cache files are in correct JSON format"""
    print("\n=== Testing JSON Cache Format ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        cache_dir = Path(temp_dir) / "json_test_cache"
        
        stemmer = FarasaStemmer(cache=True, cache_dir=str(cache_dir), logging_level="DEBUG")
        result = stemmer.stem(simple_test)
        
        # Find the cache file
        cache_files = list((cache_dir / "stem").glob("*.json"))
        assert len(cache_files) > 0, "No cache files found!"
        
        # Read and verify JSON format
        cache_file = cache_files[0]
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)
        
        # Verify structure: {source_text: result}
        assert isinstance(cache_data, dict), "Cache is not a dictionary!"
        assert simple_test in cache_data, "Source text not found as key!"
        assert cache_data[simple_test] == result, "Cached result doesn't match!"
        
        print(f"   ✓ JSON cache format correct: {cache_data}")


def test_cache_clear():
    """Test cache clearing functionality"""
    print("\n=== Testing Cache Clear ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        cache_dir = Path(temp_dir) / "clear_test_cache"
        
        # Create and populate cache
        stemmer = FarasaStemmer(cache=True, cache_dir=str(cache_dir), logging_level="DEBUG")
        result1 = stemmer.stem(simple_test)
        result2 = stemmer.stem("نص آخر")
        
        # Verify cache exists
        task_cache_dir = cache_dir / "stem"
        cache_files_before = list(task_cache_dir.glob("*.json"))
        assert len(cache_files_before) >= 2, "Cache files not created!"
        print(f"   Cache files before clear: {len(cache_files_before)}")
        
        # Clear cache
        stemmer.clear_cache()
        
        # Verify cache is cleared
        cache_files_after = list(task_cache_dir.glob("*.json"))
        assert len(cache_files_after) == 0, "Cache not properly cleared!"
        print("   ✓ Cache cleared successfully")
        
        # Test that new operations still work after clear
        result3 = stemmer.stem(simple_test)
        assert result3 == result1, "Results differ after cache clear!"
        print("   ✓ Operations work correctly after cache clear")


def test_cross_platform_cache_paths():
    """Test that default cache paths work cross-platform"""
    print("\n=== Testing Cross-Platform Cache Paths ===")
    
    # Test default cache path selection
    stemmer = FarasaStemmer(cache=True, logging_level="DEBUG")
    
    # Check that cache directory is set correctly
    if os.name == 'nt':  # Windows
        expected_base = Path(os.getenv('LOCALAPPDATA', tempfile.gettempdir()))
    else:  # Unix-like
        expected_base = Path(os.getenv('XDG_CACHE_HOME', Path.home() / '.cache'))
    
    expected_cache_dir = expected_base / "farasapy"
    
    assert stemmer.cache_dir == expected_cache_dir, f"Cache dir mismatch: {stemmer.cache_dir} != {expected_cache_dir}"
    print(f"   ✓ Default cache path correct: {stemmer.cache_dir}")


def run_basic_functionality_tests():
    """Run tests for all basic Farasa functionality"""
    print("\n=== Testing Basic Functionality (Non-Interactive) ===")
    
    print("Testing Segmenter...")
    segmenter = FarasaSegmenter()
    segmented = segmenter.segment(sample)
    assert segmented, "Segmentation failed!"
    print(f"   ✓ Segmented: {segmented[:50]}...")
    
    print("Testing Stemmer...")
    stemmer = FarasaStemmer()
    stemmed = stemmer.stem(sample)
    assert stemmed, "Stemming failed!"
    print(f"   ✓ Stemmed: {stemmed[:50]}...")
    
    print("Testing POS Tagger...")
    pos_tagger = FarasaPOSTagger()
    pos_tagged = pos_tagger.tag(sample)
    assert pos_tagged, "POS tagging failed!"
    print(f"   ✓ POS Tagged: {pos_tagged[:50]}...")
    
    print("Testing NER...")
    ner = FarasaNamedEntityRecognizer()
    ner_result = ner.recognize(sample)
    assert ner_result, "NER failed!"
    print(f"   ✓ NER: {ner_result[:50]}...")
    
    print("Testing Diacritizer...")
    diacritizer = FarasaDiacritizer()
    diacritized = diacritizer.diacritize(sample)
    assert diacritized, "Diacritization failed!"
    print(f"   ✓ Diacritized: {diacritized[:50]}...")
    
    # print("Testing Lemmatizer...")
    # print("Please provide the path to the lemmatizer JAR file to run this test.")
    # lemmatizer = FarasaLemmatizer(binary_path="<path_to_your_lemmatizer_jar_file>")
    # lemmatized = lemmatizer.lemmatize(sample)
    # print("sample lemmatized:", lemmatized)


def run_interactive_mode_tests():
    """Run tests for interactive mode"""
    print("\n=== Testing Interactive Mode ===")
    
    print("Testing Interactive Segmenter...")
    segmenter = FarasaSegmenter(interactive=True)
    segmented = segmenter.segment(simple_test)
    assert segmented, "Interactive segmentation failed!"
    print(f"   ✓ Interactive Segmented: {segmented}")
    
    print("Testing Interactive Stemmer...")
    stemmer = FarasaStemmer(interactive=True)
    stemmed = stemmer.stem(simple_test)
    assert stemmed, "Interactive stemming failed!"
    print(f"   ✓ Interactive Stemmed: {stemmed}")
    
    print("Testing Interactive POS Tagger...")
    pos_tagger = FarasaPOSTagger(interactive=True)
    pos_tagged = pos_tagger.tag(simple_test)
    assert pos_tagged, "Interactive POS tagging failed!"
    print(f"   ✓ Interactive POS Tagged: {pos_tagged}")
    
    print("Testing Interactive NER...")
    ner = FarasaNamedEntityRecognizer(interactive=True)
    ner_result = ner.recognize(simple_test)
    assert ner_result, "Interactive NER failed!"
    print(f"   ✓ Interactive NER: {ner_result}")
    
    print("Testing Interactive Diacritizer...")
    diacritizer = FarasaDiacritizer(interactive=True)
    diacritized = diacritizer.diacritize(simple_test)
    assert diacritized, "Interactive diacritization failed!"    
    print(f"   ✓ Interactive Diacritized: {diacritized}")
    
    # print("Testing Lemmatizer...")
    # print("Please provide the path to the lemmatizer JAR file to run this test.")
    # lemmatizer = FarasaLemmatizer(interactive=True,binary_path="<path_to_your_lemmatizer_jar_file>")
    # lemmatized = lemmatizer.lemmatize(sample)
    # print("sample lemmatized:", lemmatized)


def main():
    """Run all tests"""
    print("=" * 60)
    print("FARASAPY TEST SUITE")
    print("=" * 60)
    
    try:
        # Test cache functionality
        test_cache_functionality()
        test_custom_cache_directory()
        test_json_cache_format()
        test_cache_clear()
        test_cross_platform_cache_paths()
        
        # Test basic functionality
        run_basic_functionality_tests()
        run_interactive_mode_tests()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        raise


if __name__ == "__main__":
    main()
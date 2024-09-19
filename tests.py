from farasa.pos import FarasaPOSTagger
from farasa.ner import FarasaNamedEntityRecognizer
from farasa.diacratizer import FarasaDiacritizer
from farasa.segmenter import FarasaSegmenter
from farasa.stemmer import FarasaStemmer
from farasa.spellchecker import FarasaSpellChecker

# https://r12a.github.io/scripts/tutorial/summaries/arabic
sample = """
يُشار إلى أن اللغة العربية يتحدثها أكثر من 422 مليون نسمة ويتوزع متحدثوها في المنطقة المعروفة باسم الوطن العربي بالإضافة إلى العديد من المناطق الأخرى المجاورة مثل الأهواز وتركيا وتشاد والسنغال وإريتريا وغيرها. وهي اللغة الرابعة من لغات منظمة الأمم المتحدة الرسمية الست.
"""

spellchecker_sample = """
هذا النص خاطؤ الكتابه
"""

"""
---------------------
non interactive mode
---------------------
"""
print("original sample:", sample)
print("----------------------------------------")
print("Farasa features, noninteractive mode.")
print("----------------------------------------")
segmenter = FarasaSegmenter()
segmented = segmenter.segment(sample)
print("sample segmented:", segmented)
print("----------------------------------------------")

stemmer = FarasaStemmer()
stemmed = stemmer.stem(sample)
print("sample stemmed:", stemmed)
print("----------------------------------------------")

pos_tagger = FarasaPOSTagger()
pos_tagged = pos_tagger.tag(sample)
print("sample POS Tagged", pos_tagged)
print("----------------------------------------------")

pos_tagger_interactive = FarasaPOSTagger()
pos_tagged_interactive = pos_tagger_interactive.tag_segments(sample)
print("sample POS Tagged Segments", pos_tagged_interactive)
print("----------------------------------------------")

named_entity_recognizer = FarasaNamedEntityRecognizer()
named_entity_recognized = named_entity_recognizer.recognize(sample)
print("sample named entity recognized:", named_entity_recognized)
print("----------------------------------------------")

diacritizer = FarasaDiacritizer()
diacritized = diacritizer.diacritize(sample)
print("sample diacritized:", diacritized)
print("----------------------------------------------")

spellchecker = FarasaSpellChecker()
corrected = spellchecker.spell_check(spellchecker_sample)
print("spell checking sample:", spellchecker_sample)
print("sample spell checked:", corrected)
print("----------------------------------------------")
"""
---------------------
interactive mode
---------------------
"""
print("----------------------------------------")
print("Farasa features, interactive mode.")
print("----------------------------------------")

segmenter_interactive = FarasaSegmenter(interactive=True)
segmented_interactive = segmenter_interactive.segment(sample)
print("sample segmented (interactive):", segmented_interactive)
print("----------------------------------------------")

stemmer_interactive = FarasaStemmer(interactive=True)
stemmed_interactive = stemmer_interactive.stem(sample)
print("sample stemmed (interactive):", stemmed_interactive)
print("----------------------------------------------")

pos_tagger_interactive = FarasaPOSTagger(interactive=True)
pos_tagged_interactive = pos_tagger_interactive.tag(sample)
print("sample POS Tagged (interactive)", pos_tagged_interactive)
print("----------------------------------------------")

pos_tagger_interactive = FarasaPOSTagger(interactive=True)
pos_tagged_interactive = pos_tagger_interactive.tag_segments(sample)
print("sample POS Tagged Segments (interactive)", pos_tagged_interactive)
print("----------------------------------------------")

named_entity_recognizer_interactive = FarasaNamedEntityRecognizer(interactive=True)
named_entity_recognized_interactive = named_entity_recognizer_interactive.recognize(
    sample
)
print(
    "sample named entity recognized (interactive):", named_entity_recognized_interactive
)
print("----------------------------------------------")

diacritizer_interactive = FarasaDiacritizer(interactive=True)
diacritized_interactive = diacritizer_interactive.diacritize(sample)
print("sample diacritized (interactive):", diacritized_interactive)
print("----------------------------------------------")

try:
    spellchecker = FarasaSpellChecker(interactive=True)
except AssertionError as e:
    print(e)
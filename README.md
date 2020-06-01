
# Table of Content
- [Table of Content](#table-of-content)
- [Disclaimer](#disclaimer)
- [Introduction](#introduction)
- [Installation](#installation)
- [How to use](#how-to-use)
  - [AN IMPORTANT REMARK](#an-important-remark)
  - [An Overview](#an-overview)
    - [Standalone Mode](#standalone-mode)
    - [Interactive Mode](#interactive-mode)
- [Want to cite?](#want-to-cite)
- [Useful URLs](#useful-urls)


![Downloads](https://img.shields.io/pypi/dw/farasapy)
![License](https://img.shields.io/github/license/magedsaeed/farasapy?style=plastic)
![PythonVersion](https://img.shields.io/pypi/pyversions/farasapy)
![PyPiVersion](https://img.shields.io/pypi/v/farasapy?style=plastic)
<a href=\"https://colab.research.google.com/github/google/sentencepiece/blob/master/python/sentencepiece_python_module_example.ipynb\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>


# Disclaimer

>This is a Pyhton API wrapper for [farasa](http://qatsdemo.cloudapp.net/farasa/) [[http://qatsdemo.cloudapp.net/farasa/](http://qatsdemo.cloudapp.net/farasa/)] toolkit. Although this work is licsenced under MIT, the original work(the toolkit) is __strictly premitted for research purposes only__. For any commercial uses, please contact the toolkit creators[http://qatsdemo.cloudapp.net/farasa/].


 # Introduction

 Farasa is  an Arabic NLP toolkit serving the following tasks:
 1. Segmentation.
 2. Stemming.
 3. Named Entity Recgonition (NER).
 4. Part Of Speech tagging (POS tagging).
 5. Diacritization.

The toolkit is built and compiled in Java. Developers who want to use it without using this library may call the binaries directly from their code.

As Pyhton is a general purpose language and so popular for many NLP tasks, an automation to these calls to the toolkit from the code would be convenient. This is where this wrapper fits.

# Installation

```
pip install farasapy
```

# How to use

> An interactive Google colab code of the library can be reached from here [https://colab.research.google.com/drive/1xjzYwmfAszNzfR6Z2lSQi3nKYcjarXAW?usp=sharing]. 

## AN IMPORTANT REMARK


- The library, as it is a warpper for Java jars, requires that **Java is installed in your system** and is **in your PATH**. It is, also, not recommended to have a version below Java 1.7.

- Some binaries are computionally HEAVY!

## An Overview

Farasapy wraps and maintains all the toolkit's APIs in different classes where each class is in separate file. You need to import your class of interest from its file as follows:

```
from farasa.pos import FarasaPOSTagger 
from farasa.ner import FarasaNamedEntityRecognizer 
from farasa.diacratizer import FarasaDiacritizer 
from farasa.segmenter import FarasaSegmenter 
from farasa.stemmer import FarasaStemmer
```

Now, If you are using the library for the first time, the library needs to download farasa toolkit binareis first. You do not need to worry about anythink. The library, whenever you instantiate an object of any of its classes, will first check for the binaries, download them if they are not existed. This is an example of instantiating an object from `FarasaStemmer` for the first use of the library.

```
stemmer = FarasaStemmer()
perform system check...
check java version...
Your java version is 1.8 which is compatiple with Farasa
check toolkit binaries...
some binaries are not existed..
downloading zipped binaries...
100%|███████████████████████████████████████| 200M/200M [02:39<00:00, 1.26MiB/s]
extracting...
toolkit binaries are downloaded and extracted.
Dependencies seem to be satisfied..
task [STEM] is initialized in STANDALONE mode...
```
let us *stem* the following example:
```
sample =\ 
''' 
يُشار إلى أن اللغة العربية يتحدثها أكثر من 422 مليون نسمة ويتوزع متحدثوها
 في المنطقة المعروفة باسم الوطن العربي بالإضافة إلى العديد من المناطق ال
أخرى المجاورة مثل الأهواز وتركيا وتشاد والسنغال وإريتريا وغيرها.وهي اللغ
ة الرابعة من لغات منظمة الأمم المتحدة الرسمية الست. 
'''
stemmed_text = stemmer.stem(sample)                                     
print(stemmed_text)
'أشار إلى أن لغة عربي تحدث أكثر من 422 مليون نسمة توزع متحدثوها في منطقة معروف اسم وطن عربي إضافة إلى عديد من منطقة آخر مجاور مثل أهواز تركيا تشاد سنغال أريتريا غير . هي لغة رابع من لغة منظمة أمة متحد رسمي ست .'
```
You may notice that the last line of object instantiation states that the object is instantiated in **STANDALONE** mode. Farasapy, like the toolkit binaries themself, can run in two different modes: **Interactive** and **Standalone**.

### Standalone Mode 

In standalone mode, the instantiated object will call the binary each time it performs its task. It will put the input text in a temporary file, execute the binary with this temporary file, and finally extract the output from another temporary file. These temprary files are garbache collected once the task ends. Be careful that some binaries, *like the diacritizer*, might take very long time to start. Hence, this option is prefered when you have long text and you want to do it only once. 

### Interactive Mode

In interactive mode, the object will run the binary once instanciated. It, then, will feed the text to the binary interactively and capture the output on each input. However, the user should be careful not to put large lines as the output, just like in shells, might not be as expected. It is a good practice to *terminate* by `my_obj.terminate()` these kinds of objects once they are not needed to avoid any unexpected behaviour in your code.

For best pracrices, use the **INTERACTIVE** mode where the input text is small and you need to do the task multiple times. However, The **STANDALONE** mode is the best for large input texts where the task is expected to be done only once.

To work on **interactive mode**, you just need to pass `interactive=True` option to your object constructor.

The following is an example on the segmentation API that is running *interactively*.

```
segmenter = FarasaSegmenter(interactive=True)
perform system check...
check java version...
Your java version is 1.8 which is compatiple with Farasa 
check toolkit binaries...
Dependencies seem to be satisfied..
/path/to/the/library/farasa/__base.py:40: UserWarning: Be careful with large lines as they may break on interactive mode. You may switch to Standalone mode for such cases.
warnings.warn("Be careful with large lines as they may break on interactive mode. You may switch to Standalone mode for such cases.")
initializing [SEGMENT] task in INTERACTIVE mode...
task [SEGMENT] is initialized interactively.


segmented = segmenter.segment(sample)
print(segmented)
'يشار إلى أن ال+لغ+ة ال+عربي+ة يتحدث+ها أكثر من 422 مليون نسم+ة و+يتوزع متحدثوها في ال+منطق+ة ال+معروف+ة باسم ال+وطن ال+عربي ب+ال+إضاف+ة إلى ال+عديد من ال+مناطق ال+أخرى ال+مجاور+ة مثل ال+أهواز و+تركيا و+تشاد و+ال+سنغال و+إريتريا و+غير+ها . و+هي ال+لغ+ة ال+رابع+ة من لغ+ات منظم+ة ال+أمم ال+متحد+ة ال+رسمي+ة ال+ست .'
```

# Want to cite?

You can find the list of publications to site from here: http://qatsdemo.cloudapp.net/farasa/.

# Useful URLs

- The official site: http://alt.qcri.org/farasa/
- farasa from GitHub topics: https://github.com/topics/farasa
- A repository by one of the toolkit authors containing WikiNews corpus: https://github.com/kdarwish/Farasa

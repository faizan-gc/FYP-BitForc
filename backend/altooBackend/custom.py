from enum import Enum
import random
from .base import MaskFn
import yake

def get_keywords(line):

    language = "en"
    max_ngram_size = 1
    deduplication_threshold = 0.3

    numOfKeywords = int(len(line.split()) * 0.6)
    custom_kw_extractor = yake.KeywordExtractor(
        lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)
    keywords = [i[0] for i in custom_kw_extractor.extract_keywords(line)]
    for s in line.split():    
        if any(i.isdigit() for i in s):
            keywords.append(s)
    return keywords

class MaskPunctuationType(Enum):
  SENTENCE_TERMINAL = 0
  OTHER = 1

class MaskPunctuation(MaskFn):
  def __init__(self, p=0.5):
    self.p = p

  @classmethod
  def mask_types(cls):
    return list(MaskPunctuationType)

  @classmethod
  def mask_type_serialize(cls, m_type):
    return m_type.name.lower()

  def mask(self, doc):
    masked_spans = []
    for span_offset, char in enumerate(doc):
      if not char.isalnum() and len(char.strip()) > 0 and random.random() < self.p:
        if char in ['.', '?', '!']:
          span_type = MaskPunctuationType.SENTENCE_TERMINAL
        else:
          span_type = MaskPunctuationType.OTHER
        span_len = 1
        masked_spans.append((span_type, span_offset, span_len))
    return masked_spans


from nltk import pos_tag
from ..string_util import word_tokenize
from ..tokenize_util import tokens_offsets

class MaskProperNounType(Enum):
  PROPER_NOUN = 0

class MaskProperNoun(MaskFn):
  def __init__(self, p=0.5):
    try:
      pos_tag(['Ensure', 'tagger'])
    except:
      raise ValueError('Need to call nltk.download(\'averaged_perceptron_tagger\')')
    self.p = p

  @classmethod
  def mask_types(cls):
    return list(MaskProperNounType)

  @classmethod
  def mask_type_serialize(cls, m_type):
    return m_type.name.lower()

  def mask(self, doc):
    from nltk import pos_tag
    masked_spans = []
    toks = word_tokenize(doc)
    toks_offsets = tokens_offsets(doc, toks)
    toks_pos = pos_tag(toks)
    for t, off, (_, pos) in zip(toks, toks_offsets, toks_pos):
      if pos == 'NNP' and random.random() < self.p:
        masked_spans.append((MaskProperNounType.PROPER_NOUN, off, len(t)))
    return masked_spans


class MaskNotNounType(Enum):
  NOT_NOUN = 0
  NOUN = 1

class MaskNotNoun(MaskFn):
  def __init__(self, p=1.0):
    try:
      pos_tag(['Ensure', 'tagger'])
    except:
      raise ValueError('Need to call nltk.download(\'averaged_perceptron_tagger\')')
    self.p = p

  @classmethod
  def mask_types(cls):
    return list(MaskNotNounType)

  @classmethod
  def mask_type_serialize(cls, m_type):
    return m_type.name.lower()

  def mask(self, doc):
    from nltk import pos_tag
    masked_spans = []
    toks = word_tokenize(doc)
    toks_offsets = tokens_offsets(doc, toks)
    toks_pos = pos_tag(toks)
    for t, off, (_, pos) in zip(toks, toks_offsets, toks_pos):
      if 'NN' in pos_tag([t])[0][1] and random.random() < self.p:
        # masked_spans.append((MaskNotNounType.NOUN, off, len(t)))
        pass
      elif pos in ["$", "''", "(", ")", ",", "--", ".", "::", "SYM", "``"]:
        pass
      else:
        masked_spans.append((MaskNotNounType.NOT_NOUN, off, len(t)))
    return masked_spans

class MaskKeywordType(Enum):
  NOT_KEYWORD = 0
class MaskKeyword(MaskFn):
  def __init__(self, p=1.0):
    try:
      pos_tag(['Ensure', 'tagger'])
    except:
      raise ValueError('Need to call nltk.download(\'averaged_perceptron_tagger\')')
    self.p = p

  @classmethod
  def mask_types(cls):
    return list(MaskKeywordType)

  @classmethod
  def mask_type_serialize(cls, m_type):
    return m_type.name.lower()

  def mask(self, doc):
    masked_spans = []
    toks = word_tokenize(doc)
    toks_offsets = tokens_offsets(doc, toks)
    keywords = get_keywords(doc)

    for t, off in zip(toks, toks_offsets):
      if t in keywords:
        pass
      else:
        masked_spans.append((MaskKeywordType.NOT_KEYWORD, off, len(t)))

    return masked_spans



if __name__ == "__main__":
  print(get_keywords("Core 10 Women's Cloud Soft Fleece Cropped Length Bell Sleeve Yoga Hoodie Sweatshirt"))
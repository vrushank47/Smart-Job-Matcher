"""NLP utilities: text preprocessing for the Smart Job Matcher pipeline.

Pipeline
--------
raw text
  → lowercase
  → protect symbol-bearing tech terms (c++, c#, .net)
  → remove URLs, emails, punctuation, lone digits
  → NLTK word tokenize
  → POS-tag each token               (so verbs/nouns lemmatize correctly)
  → lemmatize with WordNetLemmatizer
  → drop stop-words
  → restore protected tech terms
  → join back to a clean string

The output is a plain string ready to be fed into scikit-learn's
TfidfVectorizer.  A separate helper returns the raw token list for
callers that need individual tokens.
"""

import re
import string

import nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

# Download required corpora silently (skips if already present)
for _pkg in ("punkt", "punkt_tab", "stopwords", "wordnet", "omw-1.4", "averaged_perceptron_tagger", "averaged_perceptron_tagger_eng"):
    nltk.download(_pkg, quiet=True)

_lemmatizer = WordNetLemmatizer()
_stop_words = set(stopwords.words("english"))

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_URL_RE = re.compile(r"https?://\S+|www\.\S+")
_EMAIL_RE = re.compile(r"\S+@\S+")
_DIGIT_RE = re.compile(r"\b\d+\b")           # lone numbers (years, counts…)
_WHITESPACE_RE = re.compile(r"\s+")

# Symbol-bearing tech terms that plain punctuation-stripping would destroy
# (e.g. "C++" -> "c", "C#" -> "c", ".NET" -> "net"). Protect them with a
# placeholder before stripping, then restore after tokenizing/lemmatizing.
_PROTECT_PLUSPLUS_RE = re.compile(r"\b([a-z])\+\+")
_PROTECT_SHARP_RE = re.compile(r"\b([a-z])#")
_PROTECT_DOTNET_RE = re.compile(r"\.net\b")

_RESTORE_PLUSPLUS_RE = re.compile(r"\b([a-z])plusplus\b")
_RESTORE_SHARP_RE = re.compile(r"\b([a-z])sharp\b")
_RESTORE_DOTNET_RE = re.compile(r"\bdotnet\b")


def _protect_special_tokens(text: str) -> str:
    """Replace symbol-bearing tech terms with alpha-only placeholders.

    Must run after lowercasing and before punctuation stripping, so
    terms like 'c++', 'c#', and '.net' survive the cleaning pipeline
    instead of being reduced to a bare letter.
    """
    text = _PROTECT_PLUSPLUS_RE.sub(lambda m: f"{m.group(1)}plusplus", text)
    text = _PROTECT_SHARP_RE.sub(lambda m: f"{m.group(1)}sharp", text)
    text = _PROTECT_DOTNET_RE.sub("dotnet", text)
    return text


def _restore_special_tokens(word: str) -> str:
    """Reverse _protect_special_tokens on a single lemmatized token."""
    word = _RESTORE_PLUSPLUS_RE.sub(lambda m: f"{m.group(1)}++", word)
    word = _RESTORE_SHARP_RE.sub(lambda m: f"{m.group(1)}#", word)
    word = _RESTORE_DOTNET_RE.sub(".net", word)
    return word


def _penn_to_wordnet(penn_tag: str) -> str:
    """Map a Penn Treebank POS tag to a WordNet POS constant.

    This lets the lemmatizer correctly reduce:
      - verbs  : 'managing'  → 'manage'   (not 'managing')
      - adjectives: 'skilled' → 'skilled' / 'skill'
      - nouns  : 'requirements' → 'requirement'
    """
    if penn_tag.startswith("V"):
        return wordnet.VERB
    if penn_tag.startswith("J"):
        return wordnet.ADJ
    if penn_tag.startswith("R"):
        return wordnet.ADV
    return wordnet.NOUN  # default


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def clean_text(text: str) -> str:
    """Return a normalised, lowercased string with noise removed.

    This is a *lightweight* clean — it does NOT lemmatize or strip
    stop-words.  Use :func:`preprocess` for the full pipeline.
    """
    text = text.lower()
    text = _URL_RE.sub(" ", text)
    text = _EMAIL_RE.sub(" ", text)
    text = _protect_special_tokens(text)
    text = _DIGIT_RE.sub(" ", text)
    # Remove punctuation (keep internal hyphens so "scikit-learn" survives)
    text = text.translate(str.maketrans(string.punctuation.replace("-", ""), " " * (len(string.punctuation) - 1)))
    text = _WHITESPACE_RE.sub(" ", text).strip()
    return text


def get_tokens(text: str) -> list[str]:
    """Return lemmatized, stop-word-free tokens for *text*.

    Uses POS tagging so each token is lemmatized with the correct
    part-of-speech (verb, noun, adjective …).
    """
    cleaned = clean_text(text)
    raw_tokens = word_tokenize(cleaned)

    # POS-tag all tokens in one pass (more accurate than per-token tagging)
    tagged = pos_tag(raw_tokens)

    tokens: list[str] = []
    for word, tag in tagged:
        if not word.isalpha():          # drop leftover punctuation/numbers
            continue
        if word in _stop_words:
            continue
        wn_pos = _penn_to_wordnet(tag)
        lemma = _lemmatizer.lemmatize(word, pos=wn_pos)
        tokens.append(_restore_special_tokens(lemma))

    return tokens


def preprocess(text: str) -> str:
    """Full preprocessing pipeline → clean string for TF-IDF.

    Runs :func:`get_tokens` and joins the result with spaces so that
    scikit-learn's TfidfVectorizer can consume it directly.
    """
    return " ".join(get_tokens(text))
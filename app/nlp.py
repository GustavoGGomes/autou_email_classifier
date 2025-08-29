import re
from typing import List

# Stopwords simples PT/EN (enxuto para evitar downloads de NLTK)
STOPWORDS = set([
    # pt
    "a","o","os","as","de","da","do","das","dos","e","ou","um","uma","uns","umas","para",
    "por","com","sem","em","no","na","nos","nas","ao","à","às","aos","que","se","é","são",
    "ser","foi","era","será","ter","há","já","nao","não","sim","mas","como","também","tambem",
    "sobre","entre","pelo","pela","pelos","pelas","até","ate","hoje","amanhã","amanha","ontem",
    # en
    "the","a","an","and","or","for","to","of","in","on","at","by","with","without","from","is",
    "are","was","were","be","been","being","this","that","these","those","as","it","its","we",
    "you","your","i","they","them","he","she","his","her","our","their"
])

def normalize(text: str) -> str:
    text = text or ""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s@\-\/\.:]", " ", text, flags=re.UNICODE)
    return text.strip()

def tokenize(text: str) -> List[str]:
    return [t for t in normalize(text).split() if t and t not in STOPWORDS]

def simple_lemmatize(token: str) -> str:
    # Lematização bem simples via regras (português/inglês)
    for suf in ["ções","ções","mente","mente","mente","s","es","res","ns"]:
        if token.endswith(suf) and len(token) > len(suf) + 2:
            return token[: -len(suf)]
    return token

def preprocess(text: str) -> str:
    tokens = [simple_lemmatize(t) for t in tokenize(text)]
    return " ".join(tokens)
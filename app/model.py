from typing import Dict, Tuple
import os
from .nlp import preprocess

USE_TRANSFORMERS = True if os.environ.get("USE_TRANSFORMERS", "1") == "1" else False

ZS_MODEL = None
if USE_TRANSFORMERS:
    try:
        from transformers import pipeline
        ZS_MODEL = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    except Exception as e:
        ZS_MODEL = None

CATEGORIES = ["Produtivo", "Improdutivo"]

# Palavras-chave simples para heurística
KEYWORDS_PROD = [
    "suporte","erro","falha","bug","atualização","status","andamento","ticket",
    "prazo","sistema","login","senha","acesso","reclamação","financeiro","fatura",
    "contrato","proposta","cotação","API","endpoint","integração","integracao",
    "dados","relatório","relatorio","extrato","pagamento","pix"
]
KEYWORDS_IMPROD = [
    "feliz natal","bom dia","boa tarde","boa noite","agradeço","obrigado","obg",
    "obrigada","parabéns","parabens","felicidades","atenciosamente"
]

def heuristic_classify(text: str) -> Tuple[str, float, Dict[str,float]]:
    t = text.lower()
    score_prod = sum(1 for k in KEYWORDS_PROD if k in t)
    score_improd = sum(1 for k in KEYWORDS_IMPROD if k in t)
    total = max(1, score_prod + score_improd)
    probs = {
        "Produtivo": score_prod / total,
        "Improdutivo": score_improd / total
    }
    label = "Produtivo" if score_prod >= score_improd else "Improdutivo"
    conf = probs[label]
    return label, conf, probs

def transformer_classify(text: str) -> Tuple[str, float, Dict[str,float]]:
    if ZS_MODEL is None:
        return heuristic_classify(text)
    res = ZS_MODEL(text, CATEGORIES, multi_label=False)
    # transformers retorna scores na mesma ordem das labels
    scores = {label: float(score) for label, score in zip(res["labels"], res["scores"])}
    label = res["labels"][0]
    conf = float(res["scores"][0])
    return label, conf, scores

def classify(text: str) -> Dict:
    pre = preprocess(text)
    label_h, conf_h, probs_h = heuristic_classify(pre)
    if USE_TRANSFORMERS:
        label_t, conf_t, probs_t = transformer_classify(pre)
    else:
        label_t, conf_t, probs_t = label_h, conf_h, probs_h

    # combinação simples: se o modelo concorda com heurística, usa média; senão usa o do modelo
    if label_h == label_t:
        label = label_t
        conf = min(0.99, (conf_t + conf_h) / 2 if conf_t and conf_h else conf_t or conf_h)
        probs = {k: (probs_t.get(k,0)+probs_h.get(k,0))/2 for k in CATEGORIES}
    else:
        label = label_t
        conf = conf_t
        probs = probs_t
    return {
        "label": label,
        "confidence": round(conf, 3),
        "probs": {k: round(v,3) for k,v in probs.items()},
        "preprocessed": pre
    }

def suggest_reply(text: str, label: str) -> str:
    # Respostas padrão – simples e corporativas
    if label == "Improdutivo":
        # Saudações/agradecimentos etc.
        return (
            "Olá! Agradecemos sua mensagem. Não identificamos necessidade de ação no momento. "
            "Se precisar de suporte ou tiver uma solicitação específica, por favor nos informe."
        )
    # Produtivo
    t = text.lower()
    if "status" in t or "andamento" in t:
        return (
            "Olá! Recebemos sua solicitação de status. Poderia informar o número do ticket/solicitação "
            "ou CPF/CNPJ vinculado? Assim conseguimos consultar e retornar com a atualização."
        )
    if "erro" in t or "falha" in t or "bug" in t or "acesso" in t or "login" in t or "senha" in t:
        return (
            "Olá! Sentimos pelo inconveniente. Para agilizar, por favor envie um print do erro, "
            "o horário aproximado da ocorrência e o e-mail/ID do usuário. Vamos analisar e retornar."
        )
    if "pix" in t or "pagamento" in t or "extrato" in t or "financeiro" in t:
        return (
            "Olá! Para apoiar sua solicitação financeira, precisamos dos dados: período do extrato, "
            "identificador da transação e valor aproximado. Assim, abrimos a análise imediatamente."
        )
    # fallback
    return (
        "Olá! Obrigado pelo contato. Poderia detalhar sua solicitação (contexto, sistema impactado, "
        "urgência e dados de referência)? Assim encaminhamos ao time responsável e aceleramos o atendimento."
    )
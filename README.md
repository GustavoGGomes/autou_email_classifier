# AutoU Case – Email Classifier & Auto-Reply (FastAPI)

Aplicação web simples para **classificar e responder emails automaticamente** usando NLP/IA.

## ✨ Funcionalidades
- Upload de `.txt` ou `.pdf` **ou** colagem de texto direto
- **Pré-processamento** leve de NLP (limpeza, stopwords, lematização simples)
- **Classificação**: `Produtivo` vs `Improdutivo` (híbrido: heurístico + zero-shot)
- **Resposta automática**: sugestão contextual baseada na classe
- UI em HTML (Jinja2) com estilo simples
- API em **FastAPI**

## 🚀 Como rodar localmente
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Acesse: http://127.0.0.1:8000

## 📁 Estrutura
```
autou_email_classifier/
  app/
    main.py
    nlp.py
    model.py
    templates/
      index.html
    static/
      style.css
  sample_emails/
    bom_dia_feliz_natal.txt
    solicitacao_suporte.txt
  requirements.txt
  README.md
```

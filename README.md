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

## ☁️ Deploy (sugestões)
- **Render**: Web Service (Python) com `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Hugging Face Spaces**: Gradio é mais simples, mas aqui mantivemos HTML. Alternativamente, suba como Space _Static + FastAPI_.
- **Railway / Fly.io / Azure Web App**: também funcionam.

## 🧠 Modelos de IA
- **Zero-shot classification**: `facebook/bart-large-mnli` (Transformers pipeline) para decidir entre `Produtivo` e `Improdutivo`.
- **Geração de resposta**: template orientado a regras + palavras-chave. (Opcional: trocar por `flan-t5-base` se desejar IA generativa).

> Obs.: Para ambientes com menos recursos, você pode **desativar o Transformers** e ficar apenas com a heurística (ver `USE_TRANSFORMERS` em `app/model.py`).

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

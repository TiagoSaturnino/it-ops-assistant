"""app.py — webhooks Jira/Zendesk → agente → nota interna.  Execução: uvicorn app:app --port 8000"""
from __future__ import annotations

import json
import logging
import os

import anthropic
from fastapi import BackgroundTasks, FastAPI, Header, HTTPException, Request

from agent import triar_chamado
from schemas import Chamado
from ticketing import (chamado_from_jira, chamado_from_zendesk, publicar_jira, publicar_zendesk,
                       renderizar_nota, validar_jira, validar_zendesk)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
log = logging.getLogger("itops.app")
app = FastAPI(title="IT Ops Assistant")


def triar(chamado: Chamado):
    try:
        return triar_chamado(chamado)
    except anthropic.APIError:  # failover para o provedor secundário (modo degradado, sem ferramentas)
        log.warning("Anthropic indisponível: failover para OpenAI")
        from provider_openai import triar_com_openai
        return triar_com_openai(chamado), []


def processar(chamado: Chamado, publicar) -> None:
    try:
        triagem, trilha = triar(chamado)
        nota = renderizar_nota(triagem, trilha)
        if os.getenv("ITOPS_DRY_RUN") == "1":
            print(nota)
        else:
            publicar(triagem, nota)
    except Exception:
        log.exception("Triagem falhou para %s: ticket segue para a fila manual", chamado.ticket_id)


@app.post("/webhook/jira")
async def webhook_jira(req: Request, bg: BackgroundTasks, x_itops_token: str = Header(default="")):
    if not validar_jira(x_itops_token):
        raise HTTPException(401, "token inválido")
    ch = chamado_from_jira(await req.json())
    bg.add_task(processar, ch, publicar_jira)  # responde rápido; o agente roda em background
    return {"status": "aceito", "ticket": ch.ticket_id}


@app.post("/webhook/zendesk")
async def webhook_zendesk(req: Request, bg: BackgroundTasks,
                          x_zendesk_webhook_signature: str = Header(default=""),
                          x_zendesk_webhook_signature_timestamp: str = Header(default="")):
    corpo = await req.body()
    if not validar_zendesk(corpo, x_zendesk_webhook_signature, x_zendesk_webhook_signature_timestamp):
        raise HTTPException(401, "assinatura inválida")
    ch = chamado_from_zendesk(json.loads(corpo))
    bg.add_task(processar, ch, publicar_zendesk)
    return {"status": "aceito", "ticket": ch.ticket_id}

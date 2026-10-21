"""demo.py — roda o Caso 1 localmente (usa a API Anthropic; ferramentas simuladas)."""
import logging

from agent import triar_chamado
from schemas import Chamado
from ticketing import renderizar_nota

logging.basicConfig(level=logging.INFO)
chamado = Chamado(
    ticket_id="CHM-2026-04871", origem="manual", solicitante="Marina Souza (Acessibilidade e Inclusão)",
    titulo="Sala Braille: terminal não imprime", local="Sala Braille", ativo="BRAILLE-PC01",
    contexto_negocio="matriz_ti",
    descricao=("O terminal da Sala Braille não consegue imprimir na Braille Index Everest. Erro 'Não foi "
               "possível conectar à impressora' e, ao mudar a fila, 'Permissão negada'. Funcionava ontem. "
               "Duas pessoas com deficiência visual precisam do material impresso hoje à tarde."),
)
triagem, trilha = triar_chamado(chamado)
print(renderizar_nota(triagem, trilha))
print(triagem.model_dump_json(indent=2))

def individual_serial(avaliacao) -> dict:
    return {
        "id_avaliacao": str(avaliacao["_id"]),
        "llm1": avaliacao["llm1"],
        "llm2": avaliacao["llm2"],
        "endereco_ip_user": avaliacao["endereco_ip_user"],
        "pergunta": avaliacao["pergunta"],
        "resposta_llm1":avaliacao["resposta_llm1"],
        "resposta_llm2":avaliacao["resposta_llm2"],
        "avaliacao_llm1":avaliacao["avaliacao_llm1"],
        "avaliacao_llm2":avaliacao["avaliacao_llm2"],
        "feedback_usuario":avaliacao["feedback_usuario"],
        "melhor_performance": avaliacao["melhor_performance"]
    }

def list_serial(avaliacoes) -> list:
    return [individual_serial(avaliacao) for avaliacao in avaliacoes]

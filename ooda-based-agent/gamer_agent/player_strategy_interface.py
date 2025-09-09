"""
Player Strategy Module - Interface abstrata para estratégias de jogador

Este módulo define a interface que todos os adaptadores de entrada de jogador
devem implementar, seguindo o padrão Adapter para desacoplar a lógica de
decisão da captura de entrada.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class PlayerStrategy(ABC):
    """
    Interface abstrata para adaptadores de entrada do jogador.
    Define o contrato para obter uma decisão de um jogador,
    seja ele um humano, uma IA ou um script de demonstração.
    """
    
    @abstractmethod
    def get_decision(self, available_choices: List[Dict[str, Any]], character_data: Dict[str, Any], history: List[Dict[str, Any]], current_page_data: Dict[str, Any], current_page_number: int) -> int:
        """
        Obtém o índice da escolha selecionada pelo jogador.

        Args:
            available_choices: A lista de objetos de escolha disponíveis na página atual.
            character_data: Dados estruturados do personagem do cockpit para fornecer 
                           contexto ao jogador.

        Returns:
            O índice (base 1) da escolha selecionada.
            
        Raises:
            Exception: Se não conseguir obter uma decisão válida do jogador.
        """
        pass

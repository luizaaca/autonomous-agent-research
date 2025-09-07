"""
Decision Controller Module - Sistema de Injeção de Dependência para Decisões

Este módulo implementa o padrão Strategy para controle de decisões do agente,
permitindo diferentes estratégias de tomada de decisão através de injeção de dependência.

A interface DecisionController define o contrato que todos os controladores devem seguir,
enquanto DecisionContext encapsula o estado necessário para tomada de decisões.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from character import Character


class DecisionContext:
    """
    Contexto compartilhado para tomada de decisões.
    
    Encapsula todas as informações necessárias para que um DecisionController
    possa tomar decisões informadas sobre qual choice selecionar.
    """
    
    def __init__(self, character: Character, game_data: Any, current_page: int):
        """
        Inicializa o contexto de decisão.
        
        Args:
            character: Instância do personagem com estado atual
            game_data: Dados do jogo (páginas, etc.)
            current_page: Página atual da navegação
        """
        self.character = character
        self.game_data = game_data
        self.current_page = current_page
    
    @property
    def sheet(self) -> Dict[str, Any]:
        """Acesso compatível à ficha do personagem."""
        return self.character.sheet
    
    @property 
    def occupation(self) -> Optional[str]:
        """Ocupação atual do personagem."""
        return self.character.occupation
    
    def __repr__(self) -> str:
        return f"DecisionContext(character={self.character.name}, page={self.current_page})"


class DecisionController(ABC):
    """
    Interface abstrata para controladores de decisão.
    
    Define o contrato que todos os controladores de decisão devem implementar.
    Permite diferentes estratégias de tomada de decisão através do padrão Strategy.
    """
    
    @abstractmethod
    def decide(self, choices: List[Dict[str, Any]], context: DecisionContext) -> Dict[str, Any]:
        """
        Decide qual choice selecionar com base nas opções disponíveis e no contexto.
        
        Args:
            choices: Lista de choices disponíveis na página atual
            context: Contexto com informações do personagem e jogo
            
        Returns:
            Dict representando a choice selecionada
            
        Raises:
            Exception: Se não conseguir encontrar uma choice válida
        """
        pass
    
    def validate_choice(self, choice: Dict[str, Any]) -> bool:
        """
        Valida se uma choice está em formato correto.
        
        Args:
            choice: Choice a ser validada
            
        Returns:
            True se válida, False caso contrário
        """
        if not isinstance(choice, dict):
            return False
        
        # Verifica se tem pelo menos um campo válido para ação
        valid_action_fields = ["goto", "roll", "opposed_roll", "luck_roll", "effects"]
        return any(field in choice for field in valid_action_fields)
    
    def create_fallback_choice(self) -> Dict[str, Any]:
        """
        Cria uma choice de fallback para situações de erro.
        
        Returns:
            Choice que retorna à página 1
        """
        return {"goto": 1, "text": "Fallback: Retornar ao início"}


class DecisionResult:
    """
    Resultado de uma decisão com metadados adicionais.
    
    Permite que controllers retornem não apenas a choice selecionada,
    mas também informações sobre o processo de decisão.
    """
    
    def __init__(self, choice: Dict[str, Any], reason: str = "", confidence: float = 1.0):
        """
        Inicializa resultado de decisão.
        
        Args:
            choice: Choice selecionada
            reason: Razão da seleção (para debug/log)
            confidence: Nível de confiança (0.0-1.0)
        """
        self.choice = choice
        self.reason = reason
        self.confidence = confidence
    
    def __repr__(self) -> str:
        return f"DecisionResult(choice={self.choice.get('text', str(self.choice)[:50])}, reason='{self.reason}')"


# Exemplo de uso e teste básico
if __name__ == "__main__":
    from main import GameInstructions, GameData
    
    print("=== TESTE DO DECISION CONTROLLER MODULE ===\n")
    
    # Criar contexto de teste
    game_instructions = GameInstructions()
    game_data = GameData()
    character = Character("Test Agent", "Police Officer", 30, game_instructions.get_backstory())
    context = DecisionContext(character, game_data, 1)
    
    print("1. Contexto criado:")
    print(f"   {context}")
    print(f"   Ocupação: {context.occupation}")
    print(f"   Página atual: {context.current_page}")
    print()
    
    # Testar classe abstrata
    try:
        controller = DecisionController()  # Deve falhar
    except TypeError as e:
        print(f"2. ✅ Interface abstrata funcionando: {e}")
    
    print("\n=== TESTE CONCLUÍDO ===")

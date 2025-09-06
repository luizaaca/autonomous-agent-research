"""
Default Decision Controller - Implementação padrão da lógica de decisão

Este módulo implementa o DefaultDecisionController que migra toda a lógica
do método _execute_decision_logic original, mantendo 100% de compatibilidade
com o comportamento existente.
"""

from typing import Dict, List, Any, Optional
from decision_controller import DecisionController, DecisionContext, DecisionResult


class DefaultDecisionController(DecisionController):
    """
    Implementação padrão do controlador de decisão.
    
    Migra toda a lógica do método _execute_decision_logic original,
    mantendo o comportamento idêntico para garantir compatibilidade.
    """
    
    def decide(self, choices: List[Dict[str, Any]], context: DecisionContext) -> Dict[str, Any]:
        """
        Implementa a lógica de decisão original do _execute_decision_logic.
        
        Args:
            choices: Lista de choices disponíveis
            context: Contexto com informações do personagem e jogo
            
        Returns:
            Choice selecionada
            
        Raises:
            Exception: Se não conseguir encontrar uma choice válida
        """
        chosen_choice = None
        
        try:
            for choice in choices:
                # Validação individual da choice
                if not isinstance(choice, dict):
                    print(f"AVISO: Choice inválida (não é dicionário): {choice}. Pulando.")
                    continue
                
                # Trata escolhas condicionais (estrutura especial com conditional_on)
                conditional_result = self._handle_conditional_choice(choice, context)
                if conditional_result:
                    return conditional_result
                
                # Se já temos uma escolha candidata, continuar procurando por melhores
                if chosen_choice:
                    continue
                
                # Validar se a choice padrão tem campos mínimos necessários
                if not any(field in choice for field in ["goto", "roll", "opposed_roll", "luck_roll"]):
                    continue  # Pular choices inválidas ao invés de levantar exceção
                
                # Processar set-occupation
                occupation_result = self._handle_occupation_choice(choice, context)
                if occupation_result:
                    return occupation_result
                
                # Processar requires
                requires_result = self._handle_requires_choice(choice, context)
                if requires_result:
                    return requires_result
                
                # Marcar como possível escolha padrão
                if "goto" in choice and isinstance(choice["goto"], int) and choice["goto"] > 0:
                    if not chosen_choice:
                        chosen_choice = choice
            
            # Se temos uma escolha candidata, usá-la
            if chosen_choice:
                print(f"Agente decidiu pela opção: {chosen_choice}")
                return chosen_choice
            
            # Fallback: primeira choice válida
            fallback_choice = self._find_fallback_choice(choices)
            if fallback_choice:
                print(f"Agente usando primeira choice válida como fallback: {fallback_choice}")
                return fallback_choice
                
        except Exception as e:
            print(f"ERRO CRÍTICO durante decisão: {e}")
        
        # Fallback de segurança final
        print("ERRO: Nenhuma choice válida encontrada. Usando fallback de segurança.")
        return self.create_fallback_choice()
    
    def _handle_conditional_choice(self, choice: Dict[str, Any], context: DecisionContext) -> Optional[Dict[str, Any]]:
        """
        Processa choices condicionais baseadas em ocupação.
        
        Args:
            choice: Choice a ser processada
            context: Contexto de decisão
            
        Returns:
            Choice selecionada ou None se não aplicável
        """
        if "conditional_on" not in choice:
            return None
            
        if choice["conditional_on"] == "occupation":
            paths = choice.get("paths")
            occupation = context.sheet["info"]["occupation"] or "default"

            print(f"Conditions Applied: Path choices based on occupation: {paths} for occupation {occupation}")
            if not isinstance(paths, dict):
                print(f"ERRO: 'paths' deve ser um dicionário: {paths}.")
                raise Exception("Invalid paths format")
    
            # Verifica se há um caminho específico para a ocupação atual
            if occupation in paths:
                selected_path = paths[occupation]
                print(f"Agente decidiu com base na ocupação ({occupation}): {selected_path}")
                return selected_path
            # Usa o caminho padrão se não houver específico
            elif "default" in paths:
                selected_path = paths["default"]
                print(f"Agente decidiu pelo caminho padrão da ocupação: {selected_path}")
                return selected_path
            else:
                print(f"AVISO: Nenhum caminho válido para ocupação '{occupation}' e sem caminho padrão.")
                raise Exception("No valid path for occupation and no default path")
        
        return None
    
    def _handle_occupation_choice(self, choice: Dict[str, Any], context: DecisionContext) -> Optional[Dict[str, Any]]:
        """
        Processa choices de set-occupation.
        
        Args:
            choice: Choice a ser processada
            context: Contexto de decisão
            
        Returns:
            Choice selecionada ou None se não aplicável
        """
        if "set-occupation" not in choice:
            return None
            
        if choice["set-occupation"] == context.sheet["info"]["occupation"]:
            print(f"Agente decidiu pela opção de definir ocupação já existente: {choice}")
            return choice
        else:
            print(f"AVISO: Opção de definir ocupação não corresponde à ocupação atual. Pulando choice: {choice}")
            return None
    
    def _handle_requires_choice(self, choice: Dict[str, Any], context: DecisionContext) -> Optional[Dict[str, Any]]:
        """
        Processa choices com pré-requisitos (requires).
        
        Args:
            choice: Choice a ser processada
            context: Contexto de decisão
            
        Returns:
            Choice selecionada ou None se pré-requisitos não atendidos
        """
        if "requires" not in choice:
            return None
            
        # Avalia as condições em 'requires'
        requires = choice.get("requires")
        if not isinstance(requires, dict):
            print(f"AVISO: 'requires' deve ser um dicionário: {requires}. Pulando choice.")
            return None

        conditions_met = True
        for key, value in requires.items():
            try:
                # Condição de ocupação
                if key == "occupation":
                    if not isinstance(value, str):
                        print(f"AVISO: Valor de ocupação deve ser string: {value}")
                        conditions_met = False
                        break
                    if context.sheet["info"]["occupation"] != value:
                        conditions_met = False
                        break
                # Condição de dano
                elif key == "damage_taken":
                    if not isinstance(value, dict):
                        print(f"AVISO: Condição damage_taken deve ser dicionário: {value}")
                        conditions_met = False
                        break
                    min_damage = value.get("min", 0)
                    max_damage = value.get("max", float('inf'))
                    if not isinstance(min_damage, (int, float)) or not isinstance(max_damage, (int, float)):
                        print(f"AVISO: Valores min/max de damage_taken devem ser numéricos")
                        conditions_met = False
                        break
                    current_damage = context.sheet["status"]["damage_taken"]
                    if not (min_damage <= current_damage <= max_damage):
                        conditions_met = False
                        break
                # Adicionar outras verificações de condição aqui, se necessário
                else:
                    print(f"AVISO: Condição desconhecida '{key}' em requires. Ignorando.")
            except Exception as e:
                print(f"ERRO ao avaliar condição '{key}': {e}")
                conditions_met = False
                break

        # Se todas as condições forem atendidas, escolhe esta opção
        if conditions_met:
            # Validar se a choice tem campos necessários antes de retornar
            if any(field in choice for field in ["goto", "roll", "opposed_roll", "luck_roll"]):
                print(f"Agente decidiu com base em pré-requisitos: {choice}")
                return choice
            else:
                print(f"AVISO: Choice com pré-requisitos atendidos não tem ação válida: {choice}")
        
        return None
    
    def _find_fallback_choice(self, choices: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Encontra a primeira choice válida como fallback.
        
        Args:
            choices: Lista de choices disponíveis
            
        Returns:
            Primeira choice válida ou None
        """
        for choice in choices:
            if isinstance(choice, dict) and any(field in choice for field in ["goto", "roll", "opposed_roll", "luck_roll"]):
                return choice
        return None


# Teste do DefaultDecisionController
if __name__ == "__main__":
    from main import GameInstructions, GameData
    from character import Character
    
    print("=== TESTE DO DEFAULT DECISION CONTROLLER ===\n")
    
    # Criar contexto de teste
    game_instructions = GameInstructions()
    game_data = GameData()
    character = Character("Test Agent", "Police Officer", 30, game_instructions.get_backstory())
    context = DecisionContext(character, game_data, 1)
    
    # Criar controller
    controller = DefaultDecisionController()
    
    # Teste com choices simples
    choices = [
        {"text": "Choice 1", "goto": 10},
        {"text": "Choice 2", "goto": 20},
        {"text": "Choice inválida"},  # Sem ação válida
    ]
    
    print("1. Teste com choices simples:")
    result = controller.decide(choices, context)
    print(f"   Resultado: {result}")
    print()
    
    # Teste com choice condicional baseada em ocupação
    conditional_choices = [
        {
            "conditional_on": "occupation",
            "paths": {
                "Police Officer": {"text": "Ação policial", "goto": 30},
                "default": {"text": "Ação padrão", "goto": 40}
            }
        }
    ]
    
    print("2. Teste com choice condicional:")
    result = controller.decide(conditional_choices, context)
    print(f"   Resultado: {result}")
    print()
    
    print("=== TESTE CONCLUÍDO ===")

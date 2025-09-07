"""
Default Decision Controller - Implementação Robusta da Lógica de Decisão

Este módulo implementa o DefaultDecisionController que contém toda a lógica
condicional complexa do sistema de jogo, incluindo:
- Condicionais baseadas em ocupação (conditional_on)
- Pré-requisitos e validações (requires)
- Configuração de ocupação (set-occupation)
- Fallbacks e validações completas
"""

from typing import Dict, List, Any, Optional
from decision_controller import DecisionController, DecisionContext, DecisionResult
import random


class DefaultDecisionController(DecisionController):
    """
    Implementação padrão do sistema de decisão com lógica completa.
    
    Migra toda a lógica complexa do método _execute_decision_logic_LEGACY
    do Agent, implementando suporte completo para:
    - Choices condicionais baseadas em ocupação
    - Validação de pré-requisitos
    - Configuração de atributos (set-occupation)
    - Sistema de fallbacks robusto
    """
    
    def __init__(self, debug: bool = False):
        """
        Inicializa o controller com configurações opcionais.
        
        Args:
            debug: Se True, imprime informações de debug
        """
        self.debug = debug
        self._last_decision_reason = ""
    
    def decide(self, choices: List[Dict[str, Any]], context: DecisionContext) -> Dict[str, Any]:
        """
        Implementação robusta de decisão com lógica condicional completa.
        
        Args:
            choices: Lista de choices disponíveis
            context: Contexto com character e game data
            
        Returns:
            Choice selecionada (dict)
            O FALLBACK DEVE SER TENTAR NOVAMENTE COM AS ESCOLHAS DISPONIVEIS E POSSIVEIS, ESCOLHAS IMPOSSIVEIS POR FALTA DE PONTOS DE ATTRITUBUTO, 
            por exemplo por profissao, se escolher errado deve voltar para tentar novamente. Aqui não vamos escolher errado, pois é um controle automatico, mas nos proximos vamos dar o controle ao usuario e ao llm. Todos os controles ffuncionarao igual, o jogador recebe
        """
        if self.debug:
            print(f"[DefaultDecisionController] Processando {len(choices)} choices na página {context.current_page}")
        
        # 1. Validação básica
        if not choices:
            self._last_decision_reason = "Lista de choices vazia - usando fallback"
            return self.create_fallback_choice() 
        
        # 2. Processar choices condicionais
        valid_choices = []
        for i, choice in enumerate(choices):
            processed_choice = self._process_choice(choice, context)
            if processed_choice:
                # Adicionar índice para rastreamento
                processed_choice["_choice_index"] = i
                valid_choices.append(processed_choice)
        
        # 3. Selecionar choice final
        if not valid_choices:
            self._last_decision_reason = "Nenhuma choice válida encontrada - usando fallback"
            return self.create_fallback_choice()
        
        # 4. Aplicar estratégia de seleção (primeira válida por padrão)
        selected_choice = self._select_from_valid_choices(valid_choices, context)
        
        if self.debug:
            print(f"[DefaultDecisionController] Selecionada: {selected_choice.get('text', str(selected_choice)[:50])}")
            print(f"[DefaultDecisionController] Razão: {self._last_decision_reason}")
        
        return selected_choice
    
    def _process_choice(self, choice: Dict[str, Any], context: DecisionContext) -> Optional[Dict[str, Any]]:
        """
        Processa uma choice individual, resolvendo condicionais e validações.
        
        Args:
            choice: Choice a ser processada
            context: Contexto de decisão
            
        Returns:
            Choice processada ou None se inválida
        """
        # 1. Validação básica de formato
        if not self.validate_choice(choice):
            return None
        
        # 2. Processar choices condicionais
        if "conditional_on" in choice:
            return self._handle_conditional_choice(choice, context)
        
        # 3. Verificar pré-requisitos <---- Não há requires dessa forma nas opções, verifique novamente a documentação para entender as regras.
        if "requires" in choice:
            if not self._check_requirements(choice["requires"], context):
                return None
        
        # 4. Choice válida - retornar cópia para evitar modificações
        return dict(choice)
    
    def _handle_conditional_choice(self, choice: Dict[str, Any], context: DecisionContext) -> Optional[Dict[str, Any]]:
        """
        Processa choices com lógica condicional (conditional_on).
        
        Args:
            choice: Choice com conditional_on
            context: Contexto de decisão
            
        Returns:
            Choice resolvida ou None se condição não atendida
        """
        conditional_field = choice["conditional_on"]
        paths = choice.get("paths", {})
        
        if self.debug:
            print(f"[DefaultDecisionController] Processando condicional: {conditional_field}")
        
        # 1. Resolver valor da condição
        condition_value = self._resolve_condition_value(conditional_field, context)
        
        if self.debug:
            print(f"[DefaultDecisionController] Valor da condição '{conditional_field}': {condition_value}")
        
        # 2. Buscar path específico ou default
        selected_path = None
        if condition_value in paths:
            selected_path = paths[condition_value]
            self._last_decision_reason = f"Condicional {conditional_field}={condition_value}"
        elif "default" in paths:
            selected_path = paths["default"]
            self._last_decision_reason = f"Condicional {conditional_field} usando default"
        
        if not selected_path:
            if self.debug:
                print(f"[DefaultDecisionController] Nenhum path encontrado para {conditional_field}={condition_value}")
            return None
        
        # 3. Processar path selecionado recursivamente
        return self._process_choice(selected_path, context)
    
    def _resolve_condition_value(self, field: str, context: DecisionContext) -> Any:
        """
        Resolve o valor de uma condição baseada no estado do character.
        
        Args:
            field: Campo da condição (ex: "occupation")
            context: Contexto de decisão
            
        Returns:
            Valor da condição
        """
        # Mapeamento de campos para propriedades do character
        field_mapping = {
            "occupation": lambda: context.character.occupation,
            "damage_taken": lambda: context.character.sheet.get("damage_taken", 0),
            "magic_points": lambda: context.character.get_magic_points(),
            "luck": lambda: context.character.get_luck(),
            "health_status": lambda: context.character.get_health_status()["status"]
        }
        
        if field in field_mapping:
            return field_mapping[field]()
        
        # Fallback: tentar acessar diretamente na sheet
        return context.character.sheet.get(field)
    
    def _check_requirements(self, requirements: Dict[str, Any], context: DecisionContext) -> bool:
        """
        Verifica se os pré-requisitos de uma choice são atendidos.
        
        Args:
            requirements: Dict com pré-requisitos
            context: Contexto de decisão
            
        Returns:
            True se todos os requisitos são atendidos
        """
        for req_field, req_value in requirements.items():
            current_value = self._resolve_condition_value(req_field, context)
            
            # Verificação de igualdade por padrão
            if isinstance(req_value, dict):
                # Requisitos complexos (ex: {"min": 5, "max": 10})
                if "min" in req_value and current_value < req_value["min"]:
                    return False
                if "max" in req_value and current_value > req_value["max"]:
                    return False
            else:
                # Requisito simples de igualdade
                if current_value != req_value:
                    return False
        
        return True
    
    def _select_from_valid_choices(self, valid_choices: List[Dict[str, Any]], context: DecisionContext) -> Dict[str, Any]:
        """
        Seleciona a choice final entre as choices válidas.
        
        Args:
            valid_choices: Lista de choices já validadas
            context: Contexto de decisão
            
        Returns:
            Choice selecionada
        """
        # Estratégia padrão: primeira choice válida
        # (implementações futuras podem usar outras estratégias)
        selected = valid_choices[0]
        
        if not self._last_decision_reason:
            self._last_decision_reason = f"Primeira choice válida (índice {selected.get('_choice_index', 0)})"
        
        # Remover metadados internos
        final_choice = dict(selected)
        final_choice.pop("_choice_index", None)
        
        return final_choice
    
    def validate_choice(self, choice: Dict[str, Any]) -> bool:
        """
        Validação aprimorada de choices com suporte para estruturas condicionais.
        
        Args:
            choice: Choice a ser validada
            
        Returns:
            True se válida
        """
        if not isinstance(choice, dict):
            return False
        
        # 1. Choices condicionais são válidas se têm conditional_on e paths
        if "conditional_on" in choice:
            return "paths" in choice and isinstance(choice["paths"], dict)
        
        # 2. Choices normais precisam de pelo menos uma ação válida
        valid_action_fields = [
            "goto", "roll", "opposed_roll", "luck_roll", "effects",
            "set-occupation", "conditional_on"
        ]
        
        return any(field in choice for field in valid_action_fields)
    
    def get_last_decision_reason(self) -> str:
        """
        Retorna a razão da última decisão (para debug/logging).
        
        Returns:
            String descrevendo a razão da decisão
        """
        return self._last_decision_reason


class SimpleDecisionController(DecisionController):
    """
    Controller simplificado para testes e comparações.
    
    Implementa lógica mínima: seleciona a primeira choice válida
    sem processar condicionais complexas.
    """
    
    def decide(self, choices: List[Dict[str, Any]], context: DecisionContext) -> Dict[str, Any]:
        """Seleciona primeira choice básica válida."""
        for choice in choices:
            if self.validate_choice(choice) and "conditional_on" not in choice:
                return choice
        
        return self.create_fallback_choice()


class RandomDecisionController(DecisionController):
    """
    Controller aleatório para testes de robustez.
    
    Seleciona choices aleatoriamente entre as válidas,
    útil para descobrir bugs e testar diferentes caminhos.
    """
    
    def decide(self, choices: List[Dict[str, Any]], context: DecisionContext) -> Dict[str, Any]:
        """Seleciona choice válida aleatoriamente."""
        valid_choices = [choice for choice in choices if self.validate_choice(choice)]
        
        if not valid_choices:
            return self.create_fallback_choice()
        
        return random.choice(valid_choices)


# Testes e validação
if __name__ == "__main__":
    from character import Character
    from main import GameInstructions, GameData
    
    print("=== TESTE DO DEFAULT DECISION CONTROLLER ===\n")
    
    # Criar contexto de teste
    game_instructions = GameInstructions()
    game_data = GameData()
    character = Character("Detective Smith", "Police Officer", 35, game_instructions.get_backstory())
    context = DecisionContext(character, game_data, 13)
    
    # Criar controller
    controller = DefaultDecisionController(debug=True)
    
    print("1. Teste com choice condicional (ocupação):")
    conditional_choice = {
        "conditional_on": "occupation",
        "paths": {
            "Police Officer": {"text": "Usar autoridade policial", "goto": 18},
            "Social Worker": {"text": "Usar abordagem social", "goto": 42},
            "default": {"text": "Tentar força de vontade", "roll": "POW", "results": {"3": {"goto": 22}, "2": {"goto": 27}}}
        }
    }
    
    result = controller.decide([conditional_choice], context)
    print(f"   Resultado: {result}")
    print(f"   Razão: {controller.get_last_decision_reason()}")
    print()
    
    print("2. Teste com choice simples:")
    simple_choice = {"text": "Bater na porta", "goto": 13}
    result = controller.decide([simple_choice], context)
    print(f"   Resultado: {result}")
    print(f"   Razão: {controller.get_last_decision_reason()}")
    print()
    
    print("3. Teste com múltiplas choices:")
    multiple_choices = [
        {"text": "Opção A", "goto": 10},
        conditional_choice,
        {"text": "Opção C", "goto": 30}
    ]
    result = controller.decide(multiple_choices, context)
    print(f"   Resultado: {result}")
    print(f"   Razão: {controller.get_last_decision_reason()}")
    print()
    
    print("4. Comparação com outros controllers:")
    simple_controller = SimpleDecisionController()
    random_controller = RandomDecisionController()
    
    print(f"   Default: {controller.decide(multiple_choices, context).get('text', 'N/A')}")
    print(f"   Simple: {simple_controller.decide(multiple_choices, context).get('text', 'N/A')}")
    print(f"   Random: {random_controller.decide(multiple_choices, context).get('text', 'N/A')}")
    
    print("\n=== TESTE CONCLUÍDO ===")

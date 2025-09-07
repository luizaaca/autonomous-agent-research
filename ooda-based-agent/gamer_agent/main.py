from agent import Agent
from game_repository import GameRepository
from default_decision_controller import DefaultDecisionController, RandomDecisionController


def run_scenario(name: str, occupation: str, controller_type: str = "random"):
    """
    Executa um cenário de teste com configurações específicas.
    
    Args:
        name: Nome do personagem
        occupation: Ocupação do personagem
        controller_type: Tipo de controller ("default" ou "random")
    """
    print(f"--- Running Scenario: {name} ({occupation}) with {controller_type.title()}Controller ---")
    
    # Criar repositório de dados do jogo
    game_repository = GameRepository()
    
    # Selecionar controller baseado no tipo
    if controller_type == "random":
        decision_controller = RandomDecisionController()
    else:
        decision_controller = DefaultDecisionController(debug=True)
    
    # Criar e executar agente
    agent = Agent(
        name=name,
        occupation=occupation,
        game_instructions=None,  # Não precisamos mais - Character tem get_game_backstory()
        game_data=game_repository,
        decision_controller=decision_controller
    )
    
    try:
        agent.run()
        print(f"--- Scenario {name} Finished Successfully ---\n")
    except Exception as e:
        print(f"--- Scenario {name} Failed: {e} ---\n")


if __name__ == "__main__":
    print("=== TESTE AUTOMÁTICO COM ARQUITETURA REFATORADA ===\n")
    print("Usando Character.get_game_backstory() + GameRepository + RandomDecisionController\n")
    
    # Cenários de teste com RandomDecisionController
    scenarios = [
        ("Alex", "Police Officer"),
        ("Brenda", "Social Worker"), 
        ("Charles", "Nurse")
    ]
    
    for name, occupation in scenarios:
        run_scenario(name, occupation, "random")
    
    print("=== TESTE AUTOMÁTICO CONCLUÍDO ===")
    
    # Opcional: rodar um cenário com DefaultController para comparação
    print("\n=== COMPARAÇÃO COM DEFAULT CONTROLLER ===")
    run_scenario("Detective", "Police Officer", "default")

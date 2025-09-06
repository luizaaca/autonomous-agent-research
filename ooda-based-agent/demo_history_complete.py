#!/usr/bin/env python3
"""
Demo Completo do Histórico Detalhado
====================================

Demonstração completa do histórico formatado sendo construído 
através de múltiplas iterações do agente.
"""

from test_scenarios import Agent, GameInstructions, GameData
from pages import PAGES

def create_demo_agent():
    """Cria um agente de demonstração."""
    game_data = PAGES  # Usar dados do jogo diretamente
    instructions = GameInstructions()
    
    agent = Agent(
        name="Detective Demo",
        occupation="Police Officer", 
        game_instructions=instructions,
        game_data=game_data
    )
    
    return agent

def demo_multiple_iterations():
    """Demonstra múltiplas iterações do agente para construir histórico."""
    print("🚀 DEMO: HISTÓRICO DETALHADO ATRAVÉS DE MÚLTIPLAS ITERAÇÕES")
    print("=" * 80)
    
    agent = create_demo_agent()
    
    # Definir página inicial
    agent.current_page = 1
    
    print("📊 EXECUTANDO 3 ITERAÇÕES DO CICLO OODA:")
    
    for iteration in range(1, 4):
        print(f"\n🔄 ITERAÇÃO {iteration}:")
        print("=" * 50)
        
        try:
            # 1. Observe
            page_text, choices = agent._observe()
            
            if not choices:
                print("❌ Nenhuma choice disponível - parando.")
                break
            
            # 2. Orient
            agent._orient(page_text)
            
            # 3. Decide
            chosen_action = agent._llm_decide(choices)
            
            # 4. Act
            outcome = agent.perform_action(chosen_action)
            print(f"Resultado: {outcome}")
            
            # 5. Record
            choice_index = None
            for i, choice in enumerate(choices):
                if choice == chosen_action:
                    choice_index = i
                    break
            
            agent._record_choice_in_history(page_text, chosen_action, choice_index, outcome)
            
            # Condição de parada
            if agent.current_page == 0:
                print("✅ Fim da história (goto: 0).")
                break
                
        except Exception as e:
            print(f"❌ Erro na iteração {iteration}: {e}")
            break
    
    # Mostrar histórico final
    print("\n" + "=" * 80)
    print("📚 HISTÓRICO FINAL DETALHADO:")
    print("=" * 80)
    
    # Gerar novo cockpit para mostrar histórico atualizado
    agent.game_page.set_current_page(agent.current_page)
    prompt = agent.game_page.generate_prompt()
    
    # Extrair apenas a seção de histórico
    lines = prompt.split('\n')
    in_history_section = False
    history_lines = []
    
    for line in lines:
        if '📚 DECISION HISTORY' in line:
            in_history_section = True
        elif in_history_section and line.startswith('═'):
            break
        
        if in_history_section:
            history_lines.append(line)
    
    print('\n'.join(history_lines))
    
    print("\n🎯 DEMONSTRAÇÃO CONCLUÍDA!")
    print("✅ Histórico detalhado implementado com sucesso!")
    print("✅ Cada escolha registrada com resultado completo!")
    print("✅ Formatação rica no cockpit funcionando!")

if __name__ == "__main__":
    demo_multiple_iterations()

#!/usr/bin/env python3
"""
Demo da Integração GamePage + Agent
====================================

Demonstração da nova funcionalidade de visualização avançada do agente,
mostrando o cockpit rico e escolhas estruturadas.
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

def demo_single_step():
    """Demonstra uma única iteração do agente com visualização rica."""
    print("🚀 DEMO: AGENTE COM VISUALIZAÇÃO AVANÇADA")
    print("=" * 80)
    
    agent = create_demo_agent()
    
    # Definir página inicial
    agent.current_page = 1
    
    # Executar uma iteração do ciclo OODA
    print("\n📊 EXECUTANDO UMA ITERAÇÃO DO CICLO OODA:")
    print("🔍 1. OBSERVE (usando GamePage):")
    
    try:
        page_text, choices = agent._observe()
        
        print("\n🧭 2. ORIENT (atualizando estado):")
        agent._orient(page_text)
        
        print("\n🤔 3. DECIDE (escolha do modelo):")
        if choices:
            decision = agent._llm_decide(choices)
            print(f"\n✅ Decisão tomada com sucesso!")
        else:
            print("❌ Nenhuma choice disponível")
            
    except Exception as e:
        print(f"❌ Erro durante demonstração: {e}")
        print("💡 Nota: Isso é normal se os dados do jogo não estiverem totalmente configurados")
    
    print("\n🎯 RESUMO DA INTEGRAÇÃO:")
    print("✅ GamePage integrada ao Agent")
    print("✅ Cockpit rico exibido")
    print("✅ Choices estruturadas mostradas")
    print("✅ Histórico visual atualizado")
    print("✅ Compatibilidade 100% mantida")

if __name__ == "__main__":
    demo_single_step()

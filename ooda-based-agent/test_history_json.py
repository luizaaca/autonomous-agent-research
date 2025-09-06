#!/usr/bin/env python3
"""
Teste para verificar o histórico em formato JSON
"""

from cockpit import GamePage
from character import Character
from pages import PAGES

def test_history_json():
    """Testa a renderização do histórico em JSON"""
    
    # Criar personagem
    character = Character()
    character.setup('Agent Test', 'Police Officer', 30, 'Test agent')
    
    # Criar cockpit
    game_page = GamePage(character, PAGES)
    
    # Adicionar entradas de histórico com diferentes tipos de dados
    
    # Entrada 1: Escolha simples com goto
    character.add_to_history(
        page_id=1,
        page_text="You are standing in front of a house. The door is slightly open and you can hear voices inside.",
        choice_made={
            'text': 'Go inside the house',
            'goto': 2,
            'executed_outcome': 'You entered the house quietly',
            'goto_executed': 2
        },
        choice_index=1
    )
    
    # Entrada 2: Teste de habilidade com sucesso
    character.add_to_history(
        page_id=2,
        page_text="Inside the house, you see a staircase leading up and a door to your left. You hear muffled voices from upstairs.",
        choice_made={
            'text': 'Listen at the door',
            'roll': 'Observation',
            'target': 6,
            'executed_outcome': 'You successfully hear the conversation through the door',
            'roll_result': 4,
            'skill_used': 'Observation',
            'target_value': 30,
            'success': True,
            'goto_executed': 15
        },
        choice_index=2
    )
    
    # Entrada 3: Teste de habilidade com falha e efeitos
    character.add_to_history(
        page_id=15,
        page_text="The voices become clearer. You can make out an argument between two people about money.",
        choice_made={
            'text': 'Try to open the door quietly',
            'roll': 'DEX',
            'target': 4,
            'executed_outcome': 'The door creaks loudly as you try to open it. You have been noticed!',
            'roll_result': 7,
            'skill_used': 'DEX',
            'target_value': 58,
            'success': False,
            'effects_applied': [
                {'type': 'modifier', 'skill': 'Stealth', 'modifier': -20, 'duration': 'next_roll'},
                {'type': 'status', 'condition': 'noticed', 'duration': 'scene'}
            ],
            'goto_executed': 23
        },
        choice_index=1
    )
    
    # Entrada 4: Teste oposto (opposed roll)
    character.add_to_history(
        page_id=23,
        page_text="A man opens the door suddenly and sees you! He looks surprised and angry.",
        choice_made={
            'text': 'Try to calm him down',
            'roll': 'Read Person',
            'target': 5,
            'executed_outcome': 'You fail to read his intentions and he becomes more aggressive',
            'roll_result': 8,
            'opposite_roll': 3,
            'skill_used': 'Read Person',
            'target_value': 30,
            'success': False,
            'effects_applied': [
                {'type': 'damage', 'amount': 1},
                {'type': 'status', 'condition': 'intimidated', 'duration': '3_rounds'}
            ],
            'goto_executed': 67
        },
        choice_index=3
    )
    
    # Configurar página atual
    game_page.set_current_page(67)
    
    # Renderizar histórico
    print("=== TESTE DO HISTÓRICO JSON ===")
    history_output = game_page.render_history()
    print(history_output)
    
    print("\n=== ANÁLISE DO HISTÓRICO ===")
    raw_history = character.get_history()
    print(f"Total de entradas no histórico: {len(raw_history)}")
    
    for i, entry in enumerate(raw_history, 1):
        print(f"\nEntrada {i}:")
        print(f"  - Page ID: {entry.get('page_id')}")
        print(f"  - Choice Index: {entry.get('choice_index')}")
        print(f"  - Text Length: {len(entry.get('page_text', ''))}")
        choice = entry.get('choice_made', {})
        print(f"  - Choice Keys: {list(choice.keys())}")

if __name__ == "__main__":
    test_history_json()

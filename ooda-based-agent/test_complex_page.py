#!/usr/bin/env python3
"""
Teste para demonstrar a classe GamePage com páginas complexas (skill rolls, opposed rolls)
"""

from page import GamePage, create_character_sheet
from pages import PAGES

def test_complex_page():
    """Testa a exibição de páginas com escolhas complexas."""
    
    # Criar personagem
    character = create_character_sheet()
    character["info"]["name"] = "Agent Test"
    character["info"]["occupation"] = "Police Officer"
    character["resources"]["luck"]["starting"] = 70
    character["resources"]["luck"]["current"] = 70
    character["resources"]["magic_pts"]["starting"] = 12
    character["resources"]["magic_pts"]["current"] = 12
    
    # Adicionar valores às características
    character["characteristics"]["STR"] = {"full": 45, "half": 22}
    character["characteristics"]["CON"] = {"full": 55, "half": 27}
    character["characteristics"]["DEX"] = {"full": 65, "half": 32}
    character["characteristics"]["INT"] = {"full": 75, "half": 37}
    character["characteristics"]["POW"] = {"full": 50, "half": 25}
    
    # Adicionar um histórico de exemplo
    character["page_history"] = [
        {
            'page_id': 1,
            'choice_made': {'text': 'Se você é um Policial (Police Officer)', 'goto': 9, 'set-occupation': 'Police Officer'},
            'choice_index': 1
        }
    ]
    
    # Testar página com skill roll (página 12)
    game_page = GamePage(character, PAGES)
    game_page.set_current_page(12)
    
    print("="*80)
    print("TESTE: PÁGINA COM SKILL ROLL (DEX)")
    print("="*80)
    prompt = game_page.generate_prompt()
    print(prompt)
    
    print("\n" + "="*80)
    print("CHOICE SUMMARY:")
    print(game_page.get_choice_summary())
    
    # Testar página com opposed roll (página 4)
    print("\n\n" + "="*80)
    print("TESTE: PÁGINA COM OPPOSED ROLL (Fighting)")
    print("="*80)
    game_page.set_current_page(4)
    prompt = game_page.generate_prompt()
    print(prompt)

if __name__ == "__main__":
    test_complex_page()

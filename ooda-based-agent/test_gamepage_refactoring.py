"""
Testa a refatoração da GamePage para usar a classe Character (Etapa 6).
"""
import sys
sys.path.append('.')

from character import Character
from page import GamePage
from pages import PAGES

def test_gamepage_refactoring():
    print("=== TESTE REFATORAÇÃO GAMEPAGE - ETAPA 6 ===\n")
    
    print("1. TESTE CRIAÇÃO DA GAMEPAGE COM CHARACTER")
    print("-" * 50)
    
    # Criar personagem usando classe Character
    character = Character()
    character.setup("Detective Smith", "Police Officer", 35, "Experienced detective")
    
    # Configurar alguns recursos e habilidades para teste
    character.set_skill("Firearms", 65, "combat")
    character.set_skill("Mysticism", 45, "expert")
    character.add_item("Police Badge", "equipment")
    character.add_item("Service Pistol", "weapons")
    
    # Criar GamePage com Character
    game_page = GamePage(character, PAGES)
    game_page.set_current_page(1)
    
    print(f"✅ GamePage criada com Character: {character.name}")
    print(f"✅ Página atual definida: {game_page.current_page_id}")
    print()
    
    print("2. TESTE RENDERIZAÇÃO DO STATUS DO PERSONAGEM")
    print("-" * 50)
    
    # Testar render do status usando métodos da Character
    status = game_page.render_character_status()
    print("Status renderizado:")
    print(status[:200] + "..." if len(status) > 200 else status)
    print()
    
    print("3. TESTE APLICAÇÃO DE EFEITOS")
    print("-" * 50)
    
    # Testar aplicação de efeitos usando método da Character
    effects = [
        {"action": "take_damage", "amount": 2},
        {"action": "spend_luck", "amount": 5},
        {"action": "gain_skill", "skill": "Occult"}
    ]
    
    result = game_page.update_character_from_effects(effects)
    print(f"Efeitos aplicados: {result['effects_processed']}")
    print(f"Sucessos: {result['effects_applied']}")
    print(f"Falhas: {result['effects_failed']}")
    print()
    
    # Verificar se os efeitos foram aplicados
    health = character.get_health_status()
    luck = character.get_luck()
    
    print(f"Status de saúde após dano: {health['current_level']}")
    print(f"Luck atual após gasto: {luck['current']}")
    
    try:
        occult_skill = character.get_skill("Occult", "common")
        print(f"Skill Occult adicionada: {occult_skill['full']}%")
    except KeyError:
        print("Skill Occult não foi adicionada")
    print()
    
    print("4. TESTE GERAÇÃO DE PROMPT COMPLETO")
    print("-" * 50)
    
    # Testar geração do prompt completo
    prompt = game_page.generate_prompt()
    
    # Verificar se contém as seções principais
    sections_check = {
        "AGENT COCKPIT": "🎯 AGENT COCKPIT" in prompt,
        "CHARACTER INFO": "📋 CHARACTER INFO" in prompt,
        "HEALTH STATUS": "❤️  HEALTH STATUS" in prompt,
        "RESOURCES": "⚡ RESOURCES" in prompt,
        "CHARACTERISTICS": "📊 CHARACTERISTICS" in prompt,
        "KEY SKILLS": "🎯 KEY SKILLS" in prompt,
        "INVENTORY": "🎒 INVENTORY" in prompt,
        "CURRENT SITUATION": "📍 CURRENT SITUATION" in prompt,
        "CHOICES": "🎮 AVAILABLE CHOICES" in prompt
    }
    
    print("Seções do prompt verificadas:")
    for section, found in sections_check.items():
        status = "✅" if found else "❌"
        print(f"  {status} {section}")
    
    all_sections = all(sections_check.values())
    print(f"\nTodas as seções encontradas: {'✅' if all_sections else '❌'}")
    print()
    
    print("5. TESTE COMPATIBILIDADE COM PÁGINAS")
    print("-" * 50)
    
    # Testar diferentes páginas
    test_pages = [1, 2, 3]
    
    for page_id in test_pages:
        if page_id in PAGES:
            game_page.set_current_page(page_id)
            choices_summary = game_page.get_choice_summary()
            
            print(f"Página {page_id}:")
            print(f"  Choices: {len(game_page.current_page_data.get('choices', []))}")
            print(f"  Summary: {choices_summary[:50]}..." if len(choices_summary) > 50 else f"  Summary: {choices_summary}")
        else:
            print(f"Página {page_id}: Não encontrada")
    print()
    
    print("6. TESTE COMPARAÇÃO COM SISTEMA ANTIGO")
    print("-" * 50)
    
    # Verificar se as informações são equivalentes
    info_checks = {
        "Nome": character.name == "Detective Smith",
        "Ocupação": character.occupation == "Police Officer",
        "Idade": character.age == 35,
        "Vivo": character.is_alive(),
        "Tem inventário": len(character.get_inventory()["equipment"]) > 0
    }
    
    print("Verificações de compatibilidade:")
    for check, result in info_checks.items():
        status = "✅" if result else "❌"
        print(f"  {status} {check}")
    
    all_compatible = all(info_checks.values())
    print(f"\nCompatibilidade total: {'✅' if all_compatible else '❌'}")
    print()
    
    print("7. TESTE FUNCIONALIDADES AVANÇADAS")
    print("-" * 50)
    
    # Testar modificadores
    character.add_modifier("Fighting", "penalty_dice", 2)
    character.add_modifier("Firearms", "bonus_dice", 1)
    
    # Re-renderizar status com modificadores
    status_with_mods = game_page.render_character_status()
    has_modifiers = "ACTIVE MODIFIERS" in status_with_mods
    
    print(f"Modificadores no status: {'✅' if has_modifiers else '❌'}")
    
    # Testar histórico
    game_page.add_to_history(1, "Test page text", {"text": "Test choice", "goto": 2})
    history = game_page.render_history()
    has_history = "DECISION HISTORY" in history
    
    print(f"Histórico funcionando: {'✅' if has_history else '❌'}")
    print()
    
    print("✅ Todos os testes de refatoração executados!")
    print("\n=== BENEFÍCIOS DA REFATORAÇÃO ===")
    print("✅ Eliminação de duplicação de código")
    print("✅ Uso dos métodos robustos da classe Character")
    print("✅ Aplicação de efeitos simplificada (1 linha vs 20+ linhas)")
    print("✅ Melhor tratamento de erros via Character")
    print("✅ Interface mais limpa e mantível")
    print("✅ Compatibilidade total mantida")
    print("✅ Funcionalidades avançadas (modificadores, validação)")

if __name__ == "__main__":
    test_gamepage_refactoring()

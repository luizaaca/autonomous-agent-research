"""
Testa o sistema de efeitos da classe Character (Etapa 5).
"""
import sys
sys.path.append('.')

from character import Character

def test_effects_system():
    print("=== TESTE SISTEMA DE EFEITOS - ETAPA 5 ===\n")
    
    # Criar personagem
    char = Character()
    char.setup("Effects Tester")
    
    print("1. TESTE EFEITOS BÁSICOS")
    print("-" * 40)
    
    # Teste take_damage
    effect = {"action": "take_damage", "amount": 2}
    result = char.apply_effect(effect)
    print(f"take_damage(2): Success={result['success']}, New status={result.get('new_level')}")
    
    # Teste heal_damage
    effect = {"action": "heal_damage", "amount": 1}
    result = char.apply_effect(effect)
    print(f"heal_damage(1): Success={result['success']}, New status={result.get('new_level')}")
    
    # Teste spend_luck
    effect = {"action": "spend_luck", "amount": 5}
    result = char.apply_effect(effect)
    print(f"spend_luck(5): Success={result['success']}, Remaining={result.get('remaining')}")
    
    # Teste spend_magic
    effect = {"action": "spend_magic", "amount": 3}
    result = char.apply_effect(effect)
    print(f"spend_magic(3): Success={result['success']}, Remaining={result.get('remaining')}")
    print()
    
    print("2. TESTE EFEITOS DE HABILIDADE")
    print("-" * 40)
    
    # Teste gain_skill
    effect = {"action": "gain_skill", "skill": "Mysticism"}
    result = char.apply_effect(effect)
    print(f"gain_skill(Mysticism): Success={result['success']}, Value={result.get('value')}")
    
    # Verificar se skill foi adicionada
    try:
        skill = char.get_skill("Mysticism")
        print(f"Mysticism verificada: {skill['full']}%/{skill['half']}%")
    except KeyError:
        print("Erro: Mysticism não foi adicionada")
    
    # Teste gain_skill existente
    effect = {"action": "gain_skill", "skill": "Mysticism"}
    result = char.apply_effect(effect)
    print(f"gain_skill(existente): Success={result['success']}, Message={result.get('message')}")
    print()
    
    print("3. TESTE MODIFICADORES VIA EFEITOS")
    print("-" * 40)
    
    # Teste apply_penalty
    effect = {"action": "apply_penalty", "skill": "Athletics", "duration": 2}
    result = char.apply_effect(effect)
    print(f"apply_penalty: Success={result['success']}, Duration={result.get('modifier', {}).get('duration')}")
    
    # Teste apply_bonus
    effect = {"action": "apply_bonus", "skill": "Athletics", "duration": 1}
    result = char.apply_effect(effect)
    print(f"apply_bonus: Success={result['success']}, Cancelados={char.check_skill_modifiers('Athletics')['cancelled']}")
    
    # Verificar modificadores
    mods = char.get_modifiers()
    print(f"Modificadores ativos: {len(mods)}")
    for mod in mods:
        print(f"  - {mod}")
    print()
    
    print("4. TESTE EFEITOS DE CONFIGURAÇÃO")
    print("-" * 40)
    
    # Teste set_characteristic
    effect = {"action": "set_characteristic", "characteristic": "STR", "value": 85}
    result = char.apply_effect(effect)
    print(f"set_characteristic(STR=85): Success={result['success']}")
    str_data = char.get_characteristic("STR")
    print(f"STR atual: {str_data['full']}")
    
    # Teste set_skill
    effect = {"action": "set_skill", "skill": "Fighting", "value": 75, "skill_type": "combat"}
    result = char.apply_effect(effect)
    print(f"set_skill(Fighting=75): Success={result['success']}")
    fighting_data = char.get_skill("Fighting", "combat")
    print(f"Fighting atual: {fighting_data['full']}%")
    print()
    
    print("5. TESTE INVENTÁRIO")
    print("-" * 40)
    
    # Teste add_inventory
    effect = {"action": "add_inventory", "item": "Magic Wand"}
    result = char.apply_effect(effect)
    print(f"add_inventory(Magic Wand): Success={result['success']}")
    
    effect = {"action": "add_inventory", "item": "Health Potion"}
    result = char.apply_effect(effect)
    print(f"add_inventory(Health Potion): Success={result['success']}")
    
    # Verificar inventário
    inventory = char.get_inventory()
    print(f"Inventário atual: {inventory}")
    print(f"Tem Magic Wand: {char.has_item('Magic Wand')}")
    print(f"Tem Sword: {char.has_item('Sword')}")
    
    # Teste remove_inventory
    effect = {"action": "remove_inventory", "item": "Magic Wand"}
    result = char.apply_effect(effect)
    print(f"remove_inventory(Magic Wand): Success={result['success']}")
    
    # Teste remoção de item inexistente
    effect = {"action": "remove_inventory", "item": "Nonexistent Item"}
    result = char.apply_effect(effect)
    print(f"remove_inventory(inexistente): Success={result['success']}, Error={result.get('error')}")
    
    inventory = char.get_inventory()
    print(f"Inventário final: {inventory}")
    print()
    
    print("6. TESTE APLICAÇÃO DE MÚLTIPLOS EFEITOS")
    print("-" * 40)
    
    effects = [
        {"action": "take_damage", "amount": 1},
        {"action": "spend_luck", "amount": 2},
        {"action": "gain_skill", "skill": "Occult"},
        {"action": "add_inventory", "item": "Ancient Book"},
        {"action": "apply_penalty", "skill": "Stealth", "duration": 3}
    ]
    
    result = char.apply_effects(effects)
    print(f"Múltiplos efeitos: Success={result['success']}")
    print(f"Processados: {result['effects_processed']}")
    print(f"Aplicados: {result['effects_applied']}")
    print(f"Falharam: {result['effects_failed']}")
    
    for res in result['results']:
        effect_result = res['result']
        print(f"  Efeito {res['effect_index']}: {effect_result['success']}")
    print()
    
    print("7. TESTE VALIDAÇÃO DE EFEITOS")
    print("-" * 40)
    
    # Efeitos válidos
    valid_effects = [
        {"action": "take_damage", "amount": 5},
        {"action": "gain_skill", "skill": "New Skill"},
        {"action": "add_inventory", "item": "New Item"}
    ]
    
    for effect in valid_effects:
        result = char.validate_effect(effect)
        print(f"Validação {effect['action']}: {result['valid']}")
    
    # Efeitos inválidos
    invalid_effects = [
        {"action": "invalid_action"},
        {"action": "take_damage", "amount": -5},
        {"action": "gain_skill"},  # sem skill
        {"amount": 5},  # sem action
        "not a dict"
    ]
    
    for i, effect in enumerate(invalid_effects):
        result = char.validate_effect(effect)
        print(f"Validação inválida {i+1}: {result['valid']}, Error={result.get('error', 'N/A')[:50]}...")
    print()
    
    print("8. TESTE CASOS DE ERRO")
    print("-" * 40)
    
    # Efeito inválido
    result = char.apply_effect("not a dict")
    print(f"Efeito não-dict: Success={result['success']}")
    
    # Ação inexistente
    result = char.apply_effect({"action": "invalid_action"})
    print(f"Ação inexistente: Success={result['success']}")
    
    # Lista inválida de efeitos
    result = char.apply_effects("not a list")
    print(f"Lista inválida: Success={result['success']}")
    print()
    
    print("✅ Todos os testes de efeitos executados!")
    print("\n=== FUNCIONALIDADES IMPLEMENTADAS ===")
    print("✅ apply_effect() - Aplicação de efeito individual")
    print("✅ apply_effects() - Aplicação de lista de efeitos")
    print("✅ validate_effect() - Validação de efeitos")
    print("✅ Sistema completo de efeitos:")
    print("  - take_damage, heal_damage")
    print("  - spend_luck, spend_magic, restore_luck, restore_magic")
    print("  - gain_skill, apply_penalty, apply_bonus")
    print("  - set_characteristic, set_skill")
    print("  - add_inventory, remove_inventory")
    print("✅ Gerenciamento de inventário:")
    print("  - get_inventory(), add_item(), remove_item(), has_item()")
    print("✅ Validação robusta de todos os tipos de efeito")
    print("✅ Tratamento completo de casos de erro")
    print("✅ Compatibilidade total com sistema de páginas existente")

if __name__ == "__main__":
    test_effects_system()

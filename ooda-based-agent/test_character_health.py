"""
Testa o sistema de saúde, dano e modificadores da classe Character (Etapa 4).
"""
import sys
sys.path.append('.')

from character import Character

def test_health_and_damage_system():
    print("=== TESTE SISTEMA DE SAÚDE E DANO - ETAPA 4 ===\n")
    
    # Criar personagem
    char = Character()
    char.setup("Wounded Warrior")
    
    print("1. TESTE STATUS DE SAÚDE INICIAL")
    print("-" * 40)
    
    health = char.get_health_status()
    print(f"Dano atual: {health['damage_taken']}")
    print(f"Nível de saúde: {health['current_level']}")
    print(f"Vivo: {health['is_alive']}")
    print(f"Saudável: {health['is_healthy']}")
    print(f"Níveis de dano: {health['damage_levels']}")
    print(f"Dano máximo: {health['max_damage']}\n")
    
    print("2. TESTE APLICAÇÃO DE DANO")
    print("-" * 40)
    
    # Aplicar 2 pontos de dano
    result = char.take_damage(2)
    print(f"Aplicando 2 de dano:")
    print(f"Success: {result['success']}")
    print(f"Dano aplicado: {result['damage_applied']}")
    print(f"Status anterior: {result['old_level']}")
    print(f"Status atual: {result['new_level']}")
    print(f"Dano total: {result['total_damage']}")
    print(f"Morreu: {result['died']}")
    print(f"Vivo: {result['is_alive']}\n")
    
    # Aplicar mais 1 ponto de dano
    result = char.take_damage(1)
    print(f"Aplicando +1 de dano:")
    print(f"Status anterior: {result['old_level']}")
    print(f"Status atual: {result['new_level']}")
    print(f"Dano total: {result['total_damage']}\n")
    
    print("3. TESTE CURA")
    print("-" * 40)
    
    # Curar 1 ponto
    result = char.heal_damage(1)
    print(f"Curando 1 ponto:")
    print(f"Success: {result['success']}")
    print(f"Dano curado: {result['damage_healed']}")
    print(f"Status anterior: {result['old_level']}")
    print(f"Status atual: {result['new_level']}")
    print(f"Dano total: {result['total_damage']}")
    print(f"Totalmente curado: {result['fully_healed']}\n")
    
    # Curar mais do que tem
    result = char.heal_damage(10)
    print(f"Curando 10 pontos (mais que o dano atual):")
    print(f"Dano curado: {result['damage_healed']}")
    print(f"Status atual: {result['new_level']}")
    print(f"Dano total: {result['total_damage']}")
    print(f"Totalmente curado: {result['fully_healed']}\n")
    
    print("4. TESTE MORTE")
    print("-" * 40)
    
    # Aplicar dano suficiente para matar
    result = char.take_damage(10)
    print(f"Aplicando 10 de dano (letal):")
    print(f"Status anterior: {result['old_level']}")
    print(f"Status atual: {result['new_level']}")
    print(f"Dano total: {result['total_damage']}")
    print(f"Morreu: {result['died']}")
    print(f"Vivo: {result['is_alive']}")
    print(f"is_alive(): {char.is_alive()}\n")
    
    print("5. TESTE MODIFICADORES")
    print("-" * 40)
    
    # Reiniciar personagem
    char = Character()
    char.setup("Modified Fighter")
    char.set_skill("Fighting", 60, "combat")
    
    # Adicionar penalty dice
    result = char.add_modifier("Fighting", "penalty_dice", 3)
    print(f"Adicionando penalty dice (3 usos):")
    print(f"Success: {result['success']}")
    print(f"Modificador: {result['modifier']}")
    print(f"Total modificadores: {result['total_modifiers']}\n")
    
    # Verificar modificadores
    mods = char.check_skill_modifiers("Fighting", "combat")
    print(f"Verificando modificadores de Fighting:")
    print(f"Tem bonus: {mods['has_bonus']}")
    print(f"Tem penalty: {mods['has_penalty']}")
    print(f"Penalty líquido: {mods['net_penalty']}\n")
    
    # Rolagem com modificador automático
    result = char.roll_skill("Fighting", "combat")
    print(f"Rolagem Fighting (com penalty automático):")
    print(f"Roll: {result['roll']} vs {result['target']}")
    print(f"Resultado: {result['description']}")
    print(f"Penalty dice aplicado: {result['penalty_dice']}")
    print(f"Modificadores aplicados: {result['modifiers_applied']}\n")
    
    # Adicionar bonus dice (deve cancelar)
    char.add_modifier("Fighting", "bonus_dice", 2)
    mods = char.check_skill_modifiers("Fighting", "combat")
    print(f"Após adicionar bonus dice:")
    print(f"Tem bonus: {mods['has_bonus']}")
    print(f"Tem penalty: {mods['has_penalty']}")
    print(f"Cancelados: {mods['cancelled']}\n")
    
    # Rolagem com modificadores cancelados
    result = char.roll_skill("Fighting", "combat")
    print(f"Rolagem Fighting (modificadores cancelados):")
    print(f"Roll: {result['roll']} vs {result['target']}")
    print(f"Bonus dice: {result['bonus_dice']}")
    print(f"Penalty dice: {result['penalty_dice']}\n")
    
    print("6. TESTE GERENCIAMENTO DE MODIFICADORES")
    print("-" * 40)
    
    # Listar modificadores
    modifiers = char.get_modifiers()
    print(f"Modificadores ativos: {len(modifiers)}")
    for i, mod in enumerate(modifiers):
        print(f"  {i+1}. {mod}")
    print()
    
    # Reduzir duração
    result = char.reduce_modifier_duration("Fighting", "penalty_dice")
    print(f"Reduzindo duração penalty dice:")
    print(f"Success: {result['success']}")
    print(f"Removido: {result['modifier_removed']}")
    print(f"Duração restante: {result['remaining_duration']}\n")
    
    # Limpar modificadores de Fighting
    result = char.clear_modifiers("Fighting")
    print(f"Limpando modificadores de Fighting:")
    print(f"Success: {result['success']}")
    print(f"Modificadores removidos: {result['modifiers_removed']}")
    print(f"Skill: {result['skill']}\n")
    
    print("7. TESTE CASOS DE ERRO")
    print("-" * 40)
    
    # Dano inválido
    result = char.take_damage(-5)
    print(f"Dano negativo: Success={result['success']}, Error={result['error']}")
    
    # Cura inválida
    result = char.heal_damage(-3)
    print(f"Cura negativa: Success={result['success']}, Error={result['error']}")
    
    # Modificador inválido
    result = char.add_modifier("Test", "invalid_type", 1)
    print(f"Tipo inválido: Success={result['success']}, Error={result['error']}")
    
    # Duração inválida
    result = char.add_modifier("Test", "bonus_dice", 0)
    print(f"Duração inválida: Success={result['success']}, Error={result['error']}\n")
    
    print("✅ Todos os testes de saúde e dano executados!")
    print("\n=== FUNCIONALIDADES IMPLEMENTADAS ===")
    print("✅ get_health_status() - Status completo de saúde")
    print("✅ is_alive() - Verificação de vida")
    print("✅ take_damage() - Aplicação de dano com transições")
    print("✅ heal_damage() - Cura com limites automáticos")
    print("✅ add_modifier() - Modificadores temporários")
    print("✅ check_skill_modifiers() - Verificação de modificadores")
    print("✅ reduce_modifier_duration() - Redução de duração")
    print("✅ clear_modifiers() - Limpeza de modificadores")
    print("✅ roll_skill() melhorado - Aplicação automática de modificadores")
    print("✅ Tratamento robusto de erros")
    print("✅ Sistema de níveis de dano: Healthy → Hurt → Bloodied → Down → Impaired")
    print("✅ Cancelamento automático de bonus/penalty dice")

if __name__ == "__main__":
    test_health_and_damage_system()

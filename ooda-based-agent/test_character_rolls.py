"""
Testa o sistema de rolagens da classe Character (Etapa 3).
"""
import sys
sys.path.append('.')

from character import Character

def test_roll_system():
    print("=== TESTE SISTEMA DE ROLAGENS - ETAPA 3 ===\n")
    
    # Criar personagem com habilidades
    char = Character()
    char.setup("Test Character")
    
    # Configurar algumas habilidades para teste
    char.set_skill("Firearms", 65)
    char.set_skill("Stealth", 45, "expert")
    char.set_skill("Dodge", 30, "combat")
    
    print("1. TESTE ROLAGEM DE HABILIDADE")
    print("-" * 40)
    
    # Teste rolagem normal
    result = char.roll_skill("Firearms")
    print(f"Firearms roll: {result['roll']} vs {result['target']}")
    print(f"Resultado: {result['description']} (nível {result['level']})")
    print(f"Success: {result['success']}\n")
    
    # Teste com bonus dice
    result = char.roll_skill("Stealth", "expert", bonus_dice=True)
    print(f"Stealth (bonus dice): {result['roll']} vs {result['target']}")
    print(f"Resultado: {result['description']} (nível {result['level']})")
    print(f"Bonus dice aplicado: {result['bonus_dice']}\n")
    
    # Teste com penalty dice
    result = char.roll_skill("Dodge", "combat", penalty_dice=True)
    print(f"Dodge (penalty dice): {result['roll']} vs {result['target']}")
    print(f"Resultado: {result['description']} (nível {result['level']})")
    print(f"Penalty dice aplicado: {result['penalty_dice']}\n")
    
    # Teste dificuldade hard
    result = char.roll_skill("Firearms", difficulty="hard")
    print(f"Firearms (hard): {result['roll']} vs {result['target']} (half)")
    print(f"Resultado: {result['description']} (nível {result['level']})\n")
    
    print("2. TESTE ROLAGEM DE CARACTERÍSTICA")
    print("-" * 40)
    
    # Teste rolagem de STR
    result = char.roll_characteristic("STR")
    print(f"STR roll: {result['roll']} vs {result['target']}")
    print(f"Resultado: {result['description']} (nível {result['level']})")
    print(f"Success: {result['success']}\n")
    
    # Teste com bonus dice
    result = char.roll_characteristic("DEX", bonus_dice=True)
    print(f"DEX (bonus dice): {result['roll']} vs {result['target']}")
    print(f"Resultado: {result['description']} (nível {result['level']})\n")
    
    print("3. TESTE ROLAGEM DE SORTE")
    print("-" * 40)
    
    # Teste rolagem de Luck
    result = char.roll_luck()
    print(f"Luck roll: {result['roll']} vs {result['target']}")
    print(f"Resultado: {result['description']} (nível {result['level']})")
    print(f"Success: {result['success']}\n")
    
    print("4. TESTE ROLAGEM OPOSTA")
    print("-" * 40)
    
    # Teste opposed roll
    result = char.opposed_roll("Firearms", "common", 50, 25)
    print(f"Teste oposto - Firearms vs 50:")
    print(f"Minha rolagem: {result['my_roll']['roll']} vs {result['my_roll']['target']}")
    print(f"Oponente: {result['opponent_roll']['roll']} vs {result['opponent_roll']['target']}")
    print(f"Meu resultado: {result['my_roll']['description']}")
    print(f"Oponente: {result['opponent_roll']['description']}")
    print(f"Resultado final: {result['outcome']}\n")
    
    print("5. TESTE CASOS DE ERRO")
    print("-" * 40)
    
    # Teste skill inexistente
    result = char.roll_skill("NonexistentSkill")
    print(f"Skill inexistente: Success={result['success']}, Error={result['error']}\n")
    
    # Teste característica inexistente
    result = char.roll_characteristic("INVALID")
    print(f"Característica inexistente: Success={result['success']}, Error={result['error']}\n")
    
    print("✅ Todos os testes de rolagem executados!")
    print("\n=== FUNCIONALIDADES IMPLEMENTADAS ===")
    print("✅ roll_skill() - Rolagens de habilidade com bonus/penalty dice")
    print("✅ roll_characteristic() - Rolagens de características")
    print("✅ roll_luck() - Rolagens de sorte")
    print("✅ opposed_roll() - Testes opostos")
    print("✅ _make_d100_roll() - Sistema D100 com bonus/penalty dice")
    print("✅ _evaluate_roll_result() - Avaliação de níveis de sucesso")
    print("✅ Suporte para dificuldades (regular/hard)")
    print("✅ Tratamento de erros")

if __name__ == "__main__":
    test_roll_system()

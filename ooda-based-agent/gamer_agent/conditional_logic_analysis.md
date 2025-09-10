# ETAPA 1 - ANÁLISE DA LÓGICA CONDICIONAL ATUAL

## Padrões Condicionais Identificados no `pages.py`

### 1. Estruturas de Escolha Básicas
- **Escolhas Simples**: Apenas `goto` e `text`
- **Escolhas com Efeitos**: Incluem `effects` para modificar estado do personagem

### 2. Sistema de Ocupação (Occupation)
```json
{
    "set-occupation": "Police Officer|Social Worker|Nurse"
}
```
- **Páginas com set-occupation**: 1 (escolha inicial da profissão)
- **Ocupações disponíveis**: Police Officer, Social Worker, Nurse

### 3. Lógica Condicional por Ocupação
```json
{
    "conditional_on": "occupation",
    "paths": {
        "Police Officer": { "text": "...", "goto": 18 },
        "default": { "text": "...", "roll": "POW", "results": {...} }
    }
}
```
- **Página 13**: Condicional baseada em ocupação (Police Officer vs default)

### 4. Sistema de Rolagens (Skill Rolls)
```json
{
    "roll": "Skill_Name",
    "results": {
        "5": {"goto": X},
        "4": {"goto": Y},
        "3": {"goto": Z},
        "2": {"goto": W},
        "1": {"goto": V}
    }
}
```
- **Skills identificados**: DEX, POW, INT, STR, CON, Stealth, Observation, Athletics, Magic, Drive
- **Dificuldades**: Normal e Hard

### 5. Rolagens de Sorte (Luck Rolls)
```json
{
    "luck_roll": true,
    "results": {
        "3": {"goto": X},
        "2": {"goto": Y}
    }
}
```
- **Páginas com luck_roll**: 17, 52

### 6. Rolagens Opostas (Opposed Rolls)
```json
{
    "opposed_roll": "Fighting",
    "opponent_skill": {"full": 40, "half": 20},
    "outcomes": {
        "win": {"goto": X},
        "lose": {"goto": Y, "effects": [...]},
        "draw": {"goto": Z}
    }
}
```
- **Skill principal**: Fighting
- **Estrutura complexa**: opponent_skill com valores full/half

### 7. Sistema de Efeitos (Effects)
```json
{
    "effects": [
        {"action": "take_damage", "amount": 2},
        {"action": "heal_damage", "amount": 4},
        {"action": "gain_skill", "skill": "Impello"},
        {"action": "spend_magic", "amount": 1}
    ]
}
```
- **Ações identificadas**: 
  - `take_damage` (mais comum)
  - `heal_damage`
  - `gain_skill` 
  - `spend_magic`

### 8. Condicionais Simples Baseadas em Estado
```json
{
    "text": "Se você é um Policial",
    "goto": X
}
```
- **Páginas**: 8, 44, 43 (condicionais explícitas no texto)

### 9. Dados Especiais
- **Bonus Dice**: `"bonus_dice": True` (página 26 - Magic roll)
- **Difficulty**: `"difficulty": "hard"` (página 53 - DEX roll)

## Complexidade Estrutural

### Níveis de Aninhamento:
1. **Nível 1**: Escolha simples com goto
2. **Nível 2**: Escolha com efeitos
3. **Nível 3**: Escolha com rolagem
4. **Nível 4**: Escolha condicional por ocupação
5. **Nível 5**: Rolagem oposta com estrutura complexa

### Padrões de Controle de Fluxo:
- **Sequencial**: goto simples
- **Condicional**: occupation paths
- **Probabilístico**: skill rolls com múltiplos outcomes
- **Interativo**: opposed rolls com win/lose/draw

### Dependências de Estado:
- **Character State**: occupation, damage, skills
- **Game State**: magic points, equipment
- **Context State**: previous choices, current page

## Conclusões para ETAPA 2

### Requisitos do DecisionController:
1. **Suporte a condicionais**: `conditional_on` com paths
2. **Sistema de rolagens**: skill, luck, opposed
3. **Gerenciamento de efeitos**: damage, healing, skills, magic
4. **Contexto de ocupação**: Police Officer, Social Worker, Nurse
5. **Estados complexos**: opponent_skill, bonus_dice, difficulty

### Estrutura de dados necessária:
- Character state (occupation, damage, skills, magic)
- Game context (current page, history)
- Choice evaluation engine
- Effect application system
- Roll resolution mechanism

### Prioridades de implementação:
1. **Básico**: goto simples e efeitos
2. **Médio**: skill rolls e condicionais de ocupação  
3. **Avançado**: opposed rolls e estados complexos

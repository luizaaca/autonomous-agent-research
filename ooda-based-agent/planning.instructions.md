````instructions
```

### Implementação da Classe GamePage (Setembro 2025)

**Objetivo Concluído**: ✅ Criar uma classe GamePage que funciona como cockpit/dashboard para o agente autônomo.

**Funcionalidades Implementadas**:
- **Estrutura Completa**: Classe `GamePage` com header (instruções) e body (status do personagem)
- **Interface Cockpit**: Visual dashboard mostrando atributos, saúde, habilidades, recursos, inventário e histórico
- **Renderização Modular**: Métodos separados para cada seção (header, character_status, current_situation, history)
- **Prompt Generation**: Método `generate_prompt()` que cria prompt completo para LLMs
- **Sistema de Efeitos**: Método `update_character_from_effects()` para aplicar efeitos das escolhas
- **Histórico Inteligente**: Sistema de tracking de decisões com limite automático
- **Compatibilidade**: Integração completa com estruturas existentes (character_sheet, pages.py)

**Características do Cockpit**:
- 🎯 Header com instruções claras para o LLM sobre sua role e objetivos
- 📋 Informações básicas do personagem (nome, ocupação, idade)  
- ❤️ Status de saúde visual com ícones (💚 Healthy, 💛 Hurt, 🧡 Bloodied, etc.)
- ⚡ Recursos atuais (luck, magic points, movement)
- 🎯 Habilidades principais com percentuais (full/half)
- 🎒 Inventário (equipamentos e armas)
- ⚠️ Modificadores ativos (penalidades, bônus temporários)
- 📍 Situação atual detalhada com página e texto narrativo
- 🎮 Escolhas disponíveis formatadas com números e descrições
- 📚 Histórico das últimas decisões para evitar loops

**Teste Realizado**: 
- ✅ Execução bem-sucedida com página 1 do jogo
- ✅ Renderização completa do cockpit com personagem "Detective Smith"
- ✅ Exibição correta de 3 escolhas de ocupação
- ✅ Formatação visual clara e legível para LLMs

**Próximos Passos Sugeridos**:
1. Integrar a classe nos notebooks existentes
2. Testar com cenários mais complexos (combat, skill rolls, etc.)
3. Otimizar formatação do prompt para melhor performance com LLMs

### Correção do Formato das Escolhas (Setembro 2025)

**Objetivo Concluído**: ✅ Modificar a classe GamePage para exibir objetos choice completos compatíveis com processamento.

**Problema Identificado**: 
- A classe estava mostrando apenas o texto das escolhas (`choice.get('text')`)
- O agente precisava responder com o objeto choice completo para processamento pelo sistema
- O histórico não preservava os objetos originais

**Modificações Implementadas**:
- **`render_current_situation()`**: Agora exibe o objeto choice completo: `[1] {'roll': 'DEX', 'results': {...}}`
- **Instruções atualizadas**: LLM agora recebe exemplos de como responder com objetos completos
- **`add_to_history()`**: Modificado para aceitar e armazenar objetos choice completos
- **`render_history()`**: Exibe objetos choice completos no histórico
- **`get_choice_summary()`**: Debug mostra objetos completos

**Testes Realizados**:
- ✅ **Escolhas simples**: `{'text': 'Se você é um Policial', 'goto': 9, 'set-occupation': 'Police Officer'}`
- ✅ **Skill rolls complexos**: `{'roll': 'DEX', 'results': {'5': {'goto': 34, 'effects': [...]}, ...}}`
- ✅ **Opposed rolls**: `{'opposed_roll': 'Fighting', 'opponent_skill': {'full': 40, 'half': 20}, 'outcomes': {...}}`
- ✅ **Histórico preservado**: Objetos choice completos mantidos no histórico

**Resultado**: 
O agente agora pode responder exatamente no formato esperado pelo sistema de processamento, preservando toda a informação necessária para execução correta das escolhas (efeitos, rolls, condições, etc.).

```` INSTRUÇÕES DE PLANEJAMENTO

Sempre use este arquivo para planejar mudanças significativas na estrutura de dados ou na lógica do agente. Documente o objetivo, o plano de ação e os detalhes do plano aqui antes de fazer alterações no código. Use a formatação de ckecklist para rastrear o progresso. Entende o teor do projeto e continue o desenvolvimento de forma incremental anexando ao fim do arquivo.

## Objetivo Principal

Criar um agente OODA que pode interpretar e interagir com a estrutura de dados do jogo de forma eficaz, conforme arquivo `README.md`.

## Plano de Ação Atual
- [x] **Analisar a Estrutura de Dados Atual**: Compreender completamente o formato e os tipos de dados usados no arquivo `pages.py`.
- [x] **Definir Especificações Formais**: Documentar formalmente a estrutura de dados e os tipos esperados para cada campo.
- [x] **Criar uma classe ou struct para representar uma estrutura de dados chamada page.py**: Implementar uma representação formal da estrutura de dados para facilitar a manipulação e validação dos prompts. Essa estrutura será composta por 2 partes, header e body, e será nosso prompt para o llm. Header conterá as instruções do jogo, informando que o modelo é um jogador e que o jogo será seguindo em sua ficha. No body deve constar a ficha no estado atual em cada iteração. Quero que essa estrutura represente a tela cockpit de um gamer, ele consegue seus atributos, consegue ver o status de saude, habilidades que ele possui, o historico das decisões anteriors e os objetos etc. Vamos montar essa classe e printar a cada iteração, posteriormente ela será enviada como prompt para o llm. Use os documentos do projeto para entender o contexto.
- [x] **Corrigir formato das escolhas para compatibilidade com processamento**: Modificar a classe GamePage para exibir objetos choice completos ao invés de apenas texto, garantindo que o agente responda no formato exato esperado pelo sistema de processamento.
- [ ] **Integrar a classe GamePage com os notebooks existentes**: Atualizar os notebooks para usar a nova classe GamePage ao invés de prompts simples.
- [ ] **Testar o sistema completo**: Executar cenários de teste para validar a integração entre a classe GamePage e o agente OODA.
- [ ] **Otimizar o prompt para LLMs**: Refinar a formatação e conteúdo do prompt gerado para melhor performance com modelos de linguagem.

### Especificação Formal para o Objeto `choices`
```Python
# Specification for the 'choices' object in pages.py
#
# The 'choices' object is a list of choice dictionaries. Each dictionary can have one of the following structures:
#
# 1. Simple Navigation:
#    - "text": str (optional) - The text displayed to the user for this choice.
#    - "goto": int - The page number to navigate to.
#    - "effects": list[dict] (optional) - A list of effects to apply.
#      - "action": str - The name of the action (e.g., "heal_damage", "take_damage", "gain_skill", "apply_penalty", "spend_magic", "spend_luck").
#      - "amount": int (optional) - The amount for the action.
#      - "skill": str (optional) - The skill to be affected.
#      - "duration": int (optional) - The duration of the effect.
#      - "condition": str (optional) - A condition for the effect to be applied (e.g., "full_health").
#
# 2. Skill Roll:
#    - "text": str (optional) - The text for the choice.
#    - "roll": str - The name of the skill to roll (e.g., "Stealth", "Magic", "DEX", "POW", "Athletics", "Observation", "INT", "Fighting").
#    - "difficulty": str (optional) - The difficulty of the roll (e.g., "hard").
#    - "bonus_dice": bool (optional) - Whether to grant a bonus dice.
#    - "luck_roll": bool (optional) - If it is a luck roll.
#    - "results": dict - A dictionary mapping roll outcomes to results.
#      - keys: str - The outcome of the roll (e.g., "5", "4", "3", "2", "1").
#      - values: dict or int - A dictionary with "goto" and optional "effects", or just an integer for the "goto" page.
#
# 3. Opposed Skill Roll:
#    - "text": str (optional) - The text for the choice.
#    - "opposed_roll": str - The skill for the opposed roll (e.g., "Fighting").
#    - "opponent_skill": dict - The opponent's skill values.
#      - "full": int - The full skill value.
#      - "half": int - The half skill value.
#    - "outcomes": dict - A dictionary mapping outcomes to results.
#      - keys: str - The outcome ("win", "lose", "draw").
#      - values: dict - A dictionary with "goto" and optional "effects".
#
# 4. Conditional Choice:
#    - "conditional_on": str - The character attribute to check (e.g., "occupation").
#    - "paths": dict - A dictionary mapping attribute values to choices.
#      - keys: str - The value of the attribute (e.g., "Police Officer") or "default".
#      - values: dict - A choice dictionary (can be any of the structures above).
#
# If the 'choices' list is empty, it signifies an end state.
```

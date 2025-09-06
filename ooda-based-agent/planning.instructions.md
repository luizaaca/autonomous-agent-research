# INSTRUÇÕES DE PLANEJAMENTO

Sempre use este arquivo para planejar mudanças significativas na estrutura de dados ou na lógica do agente. Documente o objetivo, o plano de ação e os detalhes do plano aqui antes de fazer alterações no código. Use a formatação de ckecklist para rastrear o progresso. Entende o teor do projeto e continue o desenvolvimento de forma incremental anexando ao fim do arquivo.

## Objetivo Principal

Criar um agente OODA que pode interpretar e interagir com a estrutura de dados do jogo de forma eficaz, conforme arquivo `README.md`.

## Plano de Ação
Analisar `pages.py` e identificar padrões na estrutura de dados para melhorar a lógica de decisão do agente.

- [x] Examinar a estrutura de dados em `pages.py` e identificar as estruturas possiveis para o objeto `choices` e produzir uma especificação formal a ser salva no fim deste arquivo.
- [x] Revisar o código do agente para garantir que ele possa interpretar todas as variações do objeto `choices` conforme a especificação formal.
- [ ] Testar o agente com diferentes cenários para garantir que ele possa tomar decisões corretas com base na estrutura de dados.
- [ ] Documentar quaisquer limitações ou áreas para melhorias futuras na lógica do agente.
- [ ] Identificar no texto das pages instruções de ação e efeitos que ainda não estão refletidos em choices
- [x] Adicionar opções choices para as páginas com instruções de ação e efeitos sem o campo choices

## Insruções adicionais
- Sempre, mas SEMPRE mesmo, re-leia os arquivos que precisar editar antes de fazer qualquer alteração para atualizar as referencias.
- Sempre confirme com o usuario antes de iniciar cada item do plano e adicione o resultado das ações ao fim deste arquivo.

## Resultados das Ações (adicione resultados aqui conforme o plano é executado)

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

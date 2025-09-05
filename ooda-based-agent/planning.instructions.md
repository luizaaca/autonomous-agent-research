# INSTRUÇÕES DE PLANEJAMENTO

Sempre use este arquivo para planejar mudanças significativas na estrutura de dados ou na lógica do agente. Documente o objetivo, o plano de ação e os detalhes do plano aqui antes de fazer alterações no código. Use a formatação de ckecklist para rastrear o progresso. Entende o teor do projeto e continue o desenvolvimento de forma incremental anexando ao fim do arquivo.

# Objetivo Principal

Transformar `pages.py` em um "motor de jogo" puramente declarativo, movendo toda a lógica de mudança de estado (dano, cura, penalidades) para dentro da estrutura `choices`. O `Agent` no notebook se tornará um executor simples que interpreta essas instruções, eliminando a necessidade de analisar texto ou lógica implícita.

## Fase 1: Padrões de Estrutura de Dados

1. Para Testes de Perícia (roll) e Sorte (luck_roll): Utilizaremos um dicionário results com chaves numéricas que representam uma hierarquia de sucesso.

    **Níveis de Sucesso** (a serem retornados pela função `make_check`):
    - `5`: Critical Success
    - `4`: Hard Success
    - `3`: Success
    - `2`: Failure
    - `1`: Fumble

    **Estrutura em `pages.py`:**
    Lógica do Agente: O agente obterá seu nível de sucesso (ex: 4) e procurará a chave `4` em `results`. Se não encontrar, procurará a `3`, e assim por diante, garantindo que um resultado melhor seja tratado, no mínimo, como o próximo nível inferior definido.

2. Para Testes Opostos (opposed_roll): Utilizaremos um dicionário `outcomes` com chaves `win`, `lose`, `draw`. A perícia do oponente será modelada de forma idêntica à do jogador.

    **Estrutura em `pages.py`:**
    Lógica do Agente: O agente rolará para si e para o oponente usando a mesma função `make_check`, comparará os níveis de sucesso numéricos para determinar `win`, `lose` ou `draw`, e então selecionará o resultado correspondente em `outcomes`.

3. Comandos de Efeitos (`effects`): A lista de ações possíveis dentro de um efeito permanece:
```json
[
    {"action": "take_damage", "amount": "<int>"},
    {"action": "heal_status", "status": "<str>"},
    {"action": "apply_penalty", "skill": "<str>", "duration": "<str>"},
    {"action": "spend_luck", "amount": "<int>"}
]
```

## Fase 2: Implementação Sistemática em `pages.py`

Irei percorrer o arquivo `pages.py` e aplicar este novo padrão de forma incremental, apresentando cada bloco de alterações para sua aprovação antes de aplicá-las. A ordem será:

- Refatorar todas as páginas com `opposed_roll`.
- Refatorar todas as páginas com `roll`.
- Refatorar todas as páginas com `luck_roll`.
- Refatorar escolhas simples que possuem efeitos (como cura).

## Fase 3: Atualização do Agente (`advanced-pagination-based-ooda-agent.ipynb`)

Após a refatoração de `pages.py`, a lógica do `Agent` será atualizada:

- **Atualizar `make_check`**: A função será modificada para retornar os níveis de sucesso numéricos (5 a 1).
- **Reescrever `perform_action`**: A função será simplificada para interpretar as novas estruturas `results` (com busca hierárquica) e `outcomes` (com comparação de níveis), aplicando os `effects` e determinando o `goto` de forma declarativa.
- **Remover Lógica Obsoleta**: Toda a lógica de análise de texto e os campos de `effect` no nível da página serão removidos.

Tarefas_concluidas:
- [x] Refatorar todas as páginas com `opposed_roll`.
- [x] Refatorar todas as páginas com `roll`.
- [x] Refatorar todas as páginas com `luck_roll`.
- [x] Refatorar escolhas simples que possuem efeitos (como cura).
- [x] Atualizar `make_check` no Agent considerando os novos níveis de sucesso.


## Plano de Ação (Revisado)

- [x] **Ação 1.1: Modificar a Ficha de Personagem (`create_character_sheet`)**
- [x] **Ação 1.2: Adicionar seção `penalties` para rastrear penalidades ativas e sua duração.**
- [x] **Ação 2: Implementar `apply_penalty` e `heal_status` no Agente**
- [x] **Ação 3: Atualizar a Lógica de Decisão (`_llm_decide`)**
- [x] **Ação 4: Atualizar o Loop Principal (`run`)**
- [x] **Ação 5: Reescrever `perform_action`**
- [x] **Ação 6: Remover Lógica Obsoleta**

### Detalhes do Plano

1.  **Modificar a Ficha de Personagem**: Adicionar uma seção `penalties` à estrutura da ficha em `create_character_sheet` para rastrear penalidades ativas e sua duração.

2.  **Implementar `apply_penalty`**: Criar a função `apply_penalty` na classe `Agent` para gerenciar as penalidades na ficha do personagem.

3.  **Atualizar a Lógica de Decisão (`_llm_decide`)**:
    *   O método será modificado para verificar os pré-requisitos de cada escolha (ex: custo de Sorte).
    *   Se um pré-requisito não for atendido, a escolha receberá uma flag `unavailable: True`.
    *   Ao listar as escolhas, uma mensagem indicará quais estão indisponíveis e por quê.
    *   A lógica de decisão do agente será instruída a não selecionar opções marcadas como indisponíveis.

4.  **Atualizar o Loop Principal (`run`)**: O método `run` será ajustado para que, se nenhuma ação válida for escolhida, o agente permaneça na página atual.

5.  **Reescrever `perform_action`**: A função será reescrita para interpretar as novas estruturas de dados (`results` e `outcomes`) de `pages.py`, tornando o agente um executor declarativo.

## Solicitação do Usuário (05/09/2025)

**Usuário:** "quero que crie um novo arquivo .v3.ipynb quebrando as celulas de codigo e intercalando com celulas que explicam em detalhes. Quero que faça isso, def a def ou seja, função a função. comece inserindo o contexto e o plano no arquivo planning, depois siga step a step conforme as instuções, planeje e depois act 1 a 1"

## Plano de Ação: Refatoração para v3

- [x] **Ação 8: Criar o arquivo `advanced-pagination-based-ooda-agent.v3.ipynb`**
- [x] **Ação 9: Migrar e detalhar as funções globais**
    - [x] **9.1:** Mover `create_character_sheet` para sua própria célula com explicação detalhada.
    - [x] **9.2:** Mover `setup_character` para sua própria célula com explicação detalhada.
    - [x] **9.3:** Mover `make_check` para sua própria célula com explicação detalhada.
- [x] **Ação 10: Migrar e detalhar a classe `Agent` método a método**
    - [x] **10.1:** Criar a definição da classe `Agent` com `__init__` e `__repr__`, com explicação.
    - [x] **10.2:** Mover `_llm_decide` para sua própria célula com explicação detalhada.
    - [x] **10.3:** Mover `perform_action` para sua própria célula com explicação detalhada.
    - [x] **10.4:** Mover `run` para sua própria célula com explicação detalhada.
    - [x] **10.5:** Mover os métodos auxiliares (`_observe`, `_orient`) para sua própria célula com explicação detalhada.
- [x] **Ação 11: Migrar o ponto de entrada (`main`)**
- [x] **Ação 12: Marcar todas as tarefas da refatoração v3 como concluídas.**
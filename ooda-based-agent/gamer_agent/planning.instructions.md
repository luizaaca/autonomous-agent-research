# INSTRUÇÕES DE PLANEJAMENTO

Sempre use este arquivo para planejar mudanças significativas na estrutura de dados ou na lógica do agente. Documente o objetivo, o plano de ação e os detalhes do plano aqui antes de fazer alterações no código. Use a formatação de ckecklist para rastrear o progresso. Entende o teor do projeto e continue o desenvolvimento de forma incremental anexando ao fim do arquivo.

## Objetivo Principal

Criar um agente OODA que pode interpretar e interagir com a estrutura de dados do jogo de forma eficaz, conforme arquivo `ooda-based-agent\gamer_agent\automatica_gaming_agent.md`.

## Plano de Ação e tarefas

### FASE 4: Refatoração da UI e Lógica de Decisão (v1.4) - ✅ COMPLETO

**Status**: ✅ **IMPLEMENTAÇÃO COMPLETA**

**Objetivo**: Melhorar a clareza da interface de usuário (UI) e introduzir variabilidade no comportamento do agente de demonstração.

**Decisões Arquiteturais Implementadas:**
- ✅ **Separação do Histórico**: O histórico de decisões foi movido para um painel dedicado, separado das escolhas disponíveis, para uma UI mais limpa.
- ✅ **Choices Descritivas**: As opções de escolha agora exibem detalhes de suas ações (`goto`, `roll`, `effects`), eliminando a ambiguidade de "escolhas sem texto".
- ✅ **Decisão Aleatória no Modo Demo**: O `DefaultDecisionController` agora seleciona uma escolha aleatória quando há múltiplas opções simples, tornando a navegação menos determinística.

**Tarefas de Implementação Concluídas:**

#### Subcomponente 1: Refatoração do Cockpit (UI) - ✅ COMPLETO
- ✅ **cockpit.py `render_game_screen()`**: Layout principal reorganizado para incluir um painel de histórico separado.
- ✅ **cockpit.py `_build_history_panel()`**: Novo método criado para renderizar o painel de histórico.
- ✅ **cockpit.py `_format_choice_text()`**: Novo método auxiliar para formatar o texto da escolha com detalhes de suas ações.
- ✅ **cockpit.py `_build_choices_panel()`**: Refatorado para usar `_format_choice_text` e remover a lógica de histórico.

#### Subcomponente 2: Lógica de Decisão Aleatória - ✅ COMPLETO
- ✅ **default_decision_controller.py `_select_from_valid_choices()`**: Lógica atualizada para usar `random.choice()` quando há múltiplas escolhas simples e não condicionais.

**✅ BENEFÍCIOS IMPLEMENTADOS:**
- ✅ **Clareza da Interface**: A separação do histórico e as escolhas descritivas tornam a tela de jogo muito mais fácil de entender.
- ✅ **Variabilidade do Agente**: O modo de demonstração agora pode explorar diferentes caminhos na história de forma autônoma.
- ✅ **Manutenibilidade**: O código do `Cockpit` está mais organizado e com responsabilidades mais claras.

---
# INSTRUÇÕ### FASE 0: Correção Est### FASE 1: PlayerInputAdapter Architecture (v1.2) - ✅ COMPLETO

**Status**: ✅ IMPLEMENTAÇÃO COMPLETA (Todos os passos finalizados com sucesso)

**Decisões Arquiteturais Confirmadas:**
- ✅ Opção C: Evolução DecisionController → PlayerInputAdapter
- ✅ Retorno: choice_index (int) em vez de choice dict  
- ✅ Construtor Agent: `Agent(character, game_repository, player_input_adapter)`
- ✅ Ocupação definida dinamicamente via `"set-occupation"` effect
- ✅ Character inicia sem ocupação (occupation=None)ges.py (v1.2) - ✅ CONCLUÍDO

**Status**: ✅ IMPLEMENTADO

**Objetivo**: Converter escolhas com pré-requisitos implícitos para o padrão `conditional_on`.

**Correções Realizadas:**
- ✅ **Página 6**: `"Se você é um Policial, identifique-se"` → `conditional_on: "occupation"`
- ✅ **Página 43**: `"Se Knuckles já estava contido e você é..."` → `conditional_on: "occupation"`  
- ✅ **Página 44**: `"Se você é Enfermeiro"` → `conditional_on: "occupation"`
- ✅ **Página 74**: `"Se você é Assistente Social"` → `conditional_on: "occupation"`

**Novos Padrões Implementados:**
- ✅ Padrão `conditional_on` com `paths` para diferentes ocupações
- ✅ Opção `default` para casos onde ocupação não é adequada
- ✅ Efeito `add_history_log` para feedback de sistema
- ✅ Atributo `requires` para pré-requisitos adicionais (ex: `knuckles_restrained`)

**Benefícios:**
- ✅ Estrutura compatível com PlayerInputAdapter
- ✅ Validação adequada de pré-requisitos de ocupação
- ✅ Feedback claro para tentativas inválidas
- ✅ Suporte a múltiplas ocupações na mesma escolha

### FASE 1: PlayerInputAdapter Architecture (v1.2) - 📋 PLANEJAMENTO CONFIRMADOS DE PLANEJAMENTO

Sempre use este arquivo para planejar mudanças significativas na estrutura de dados ou na lógica do agente. Documente o objetivo, o plano de ação e os detalhes do plano aqui antes de fazer alterações no código. Use a formatação de ckecklist para rastrear o progresso. Entende o teor do projeto e continue o desenvolvimento de forma incremental anexando ao fim do arquivo.

## Objetivo Principal

Criar um agente OODA que pode interpretar e interagir com a estrutura de dados do jogo de forma eficaz, conforme arquivo `ooda-based-agent\gamer_agent\automatica_gaming_agent.md`.

## Plano de Ação e tarefas

### FASE 1: PlayerInputAdapter Architecture (v1.2) - 🟡 EM PROGRESSO

**Status**:  IMPLEMENTAÇÃO PARCIAL (Passo 1 ✅ + Cockpit ✅, Agent e main.py pendentes)

**Decisões Arquiteturais Confirmadas:**
- ✅ Opção C: Evolução DecisionController → PlayerInputAdapter
- ✅ Retorno: choice_index (int) em vez de choice dict  
- ✅ Construtor Agent: `Agent(character, game_repository, player_input_adapter)`
- ✅ Ocupação definida dinamicamente via `"set-occupation"` effect
- ✅ Character inicia sem ocupação (occupation=None)

**Tarefas de Implementação:**

#### Passo 1: Criar Interface e Adaptadores - ✅ COMPLETO
- ✅ Criar `player_input_adapter.py` com interface abstrata
- ✅ Criar `player_adapters.py` com implementações:
  - ✅ `DemoPlayerAdapter` (internaliza lógica DefaultDecisionController)
    - ✅ `_format_compact_cockpit()` - layout tabular 4 linhas para 480p
  - ✅ `HumanPlayerAdapter` (console input loop)
    - ✅ `_format_detailed_cockpit()` - layout completo e legível
  - ✅ `LLMPlayerAdapter` (API integration)
    - ✅ `_format_structured_cockpit()` - formato otimizado para LLM parsing

**✅ MELHORIAS ARQUITETURAIS EXTRAS IMPLEMENTADAS:**
- ✅ **Separação de responsabilidades**: `cockpit.render_character_status()` retorna `Dict[str, Any]`
- ✅ **Interface atualizada**: Todos `get_decision()` usam `character_data: Dict[str, Any]`
- ✅ **Formatação responsiva**: Cada adapter formata dados conforme sua necessidade
- ✅ **Cockpit refatorado**: Dados estruturados + método auxiliar `_format_character_status_for_prompt()`

#### Passo 2: Refatorar Agent - ✅ COMPLETO
- ✅ Modificar construtor para novo signature (`Agent(character, game_repository, player_input_adapter)`)
- ✅ Atualizar OODA loop para usar PlayerInputAdapter
- ✅ Implementar conversão choice_index → choice dict
- ✅ Imports atualizados (removido DecisionController, adicionado PlayerInputAdapter)
- ✅ Método `_decide()` implementado conforme arquitetura v1.2
- ✅ Manter validação de regras no Agent (retry loop + feedback de erro)
- ✅ Tratar ocupação dinâmica via "set-occupation" (detecção + log informativo)

#### Passo 3: Refatorar Cockpit - ✅ COMPLETO
- ✅ Garantir rendering adequado para todos adapters (dados estruturados implementados)
- ✅ Adicionar prefixos [SYSTEM]/[ERROR] para mensagens
- ✅ Renomear GamePage → Cockpit
- ✅ Implementar render_game_screen() com rich.Panel e rich.Table
- ✅ Integrar histórico nas escolhas disponíveis
- ✅ Formatar choices como "[1] - texto da escolha"

#### Passo 4: Atualizar main.py - ✅ COMPLETO
- ✅ Implementar argparse para seleção de player type (`--player {demo,human,llm}`)
- ✅ Criar Character sem ocupação inicial (occupation=None)
- ✅ Configurar player adapter baseado em argumentos com validação de GEMINI_API_KEY
- ✅ Usar novo construtor Agent (`Agent(character, game_repository, player_input_adapter)`)
- ✅ Tratamento de exceções e feedback claro ao usuário
- ✅ Documentação inline completa com exemplos de uso

**Arquivos a serem criados/modificados:**
- ✅ `player_input_adapter.py` (COMPLETO)
- ✅ `player_adapters.py` (COMPLETO - 3 adapters + formatação)
- ✅ `cockpit.py` (COMPLETO - dados estruturados + compatibilidade)
- ✅ `agent.py` (COMPLETO - construtor + OODA loop + PlayerInputAdapter integrado + Circuit Breaker)
- ✅ `main.py` (COMPLETO - argparse + nova inicialização + dependency injection)
- ✅ `automatica_gaming_agent.md` (documentação v1.2)
- ✅ `planning.instructions.md` (este arquivo)

### FASE 3: Sistema de UI/Logging Melhorado - ✅ COMPLETO

**Status**: ✅ **IMPLEMENTAÇÃO COMPLETA**

**Objetivo**: Implementar sistema de "tela de video-game" compacta com logging JSON separado e controle manual de fluxo.

**Decisões Arquiteturais Implementadas:**
- ✅ **Interface Compacta**: Cockpit renderiza informações em formato tabular tipo "video-game"
- ✅ **Histórico Integrado**: Últimas 3 jogadas aparecem na seção de choices
- ✅ **Logging Separado**: Dados JSON estruturados mostram código completo das choices
- ✅ **Controle Manual**: Todos os modos (demo/humano/llm) requerem ENTER para avançar
- ✅ **Output Limpo**: Removidos prints de diagnóstico desnecessários

**Tarefas de Implementação Concluídas:**

#### Subcomponente 1: Refatoração do Cockpit - ✅ COMPLETO
- ✅ **cockpit.py**: Classe GamePage → Cockpit
- ✅ **render_game_screen()**: Interface unificada usando rich.Panel e rich.Table
- ✅ **_build_choices_panel()**: Histórico integrado + choices formatadas como "[1] - texto"
- ✅ **Resultado**: Tela compacta tipo "video-game" com informações organizadas

#### Subcomponente 2: Sistema de Logging JSON - ✅ COMPLETO
- ✅ **agent.py _log_turn_summary()**: Log limpo com código completo da choice
- ✅ **Estrutura JSON**: page, choice_selected.choice_data, execution_result
- ✅ **Resultado**: Separação clara entre UI (cockpit) e dados (JSON)

#### Subcomponente 3: Controle de Fluxo Manual - ✅ COMPLETO
- ✅ **agent.py run()**: Pausa manual após cada log JSON
- ✅ **Limpeza de Output**: Removidos prints de diagnóstico de _observe(), _orient()
- ✅ **Resultado**: Controle total do usuário sobre o ritmo do jogo

**✅ BENEFÍCIOS IMPLEMENTADOS:**
- ✅ **Experiência Unificada**: Todos os modos têm a mesma interface compacta
- ✅ **Controle Total**: Usuário avança no seu próprio ritmo
- ✅ **Separação Clara**: UI visual separada dos dados técnicos
- ✅ **Legibilidade**: Choices em texto, código em JSON, histórico integrado

### FASE 2: Sistema de Inicialização Randômica + Circuit Breaker - ✅ COMPLETO

**Status**: ✅ **IMPLEMENTAÇÃO COMPLETA**

**Objetivo**: Implementar sistema robusto de inicialização de personagem + proteção contra loops infinitos conforme "The Domestic" RPG.

**Decisões Arquiteturais Implementadas:**
- ✅ **Circuit Breaker Robusto**: Monitora tanto falhas de validação (`_decide`) quanto de execução (`perform_action`).
- ✅ **Terminação Segura**: Encerra o agente se o mesmo erro ocorrer 3x consecutivas.
- ✅ **Inicialização Randômica**: Atributos e recursos são gerados aleatoriamente no `__init__` do `Character`.
- ✅ **Inicialização de Ocupação Dinâmica**: Método `set_occupation` em `Character` aplica os bônus e habilidades.
- ✅ **Magic Skill Garantida**: Habilidade "Magic" é sempre inicializada com 50% para todos os personagens.

**Tarefas de Implementação Concluídas:**

#### Subcomponente 1: Circuit Breaker Pattern (Refatorado) - ✅ COMPLETO
- ✅ **agent.py `run()`**: Lógica do Circuit Breaker movida para um bloco `try...except` em torno de `perform_action()`.
- ✅ **agent.py `_decide()`**: Mantém a validação de regras, mas o contador principal agora é acionado por falhas de execução.
- ✅ **Contador Unificado**: `failed_choices_count` é incrementado tanto por falhas de validação quanto de execução.
- ✅ **Reset em Sucesso**: Contador é zerado após qualquer ação bem-sucedida.

**✅ BENEFÍCIOS IMPLEMENTADOS:**
- ✅ **Proteção Abrangente**: Previne loops causados por erros de lógica, dados inválidos ou falhas de execução.
- ✅ **Estabilidade Aprimorada**: Garante que o agente não trave em estados irrecuperáveis.

#### Subcomponente 2: Inicialização Randômica e Dinâmica de Character - ✅ COMPLETO
- ✅ **character.py `__init__`**: Agora chama `_initialize_random_stats()` para gerar valores base.
- ✅ **character.py `_initialize_random_stats()`**: Novo método que implementa as regras de "The Domestic" (3d6*5 para atributos, etc.).
- ✅ **character.py `setup()`**: Refatorado para orquestrar a inicialização. Garante que "Magic" seja sempre 50%.
- ✅ **character.py `set_occupation()`**: Novo método que aplica os bônus de uma ocupação específica.
- ✅ **agent.py `_process_effects()`**: Agora chama `character.set_occupation()` quando o efeito `"set-occupation"` é encontrado.

**✅ BENEFÍCIOS IMPLEMENTADOS:**
- ✅ **Fidelidade ao Jogo**: Personagens são criados conforme as regras do RPG "The Domestic".
- ✅ **Flexibilidade**: A ocupação pode ser definida a qualquer momento, e os atributos são ajustados corretamente.
- ✅ **Correção da Causa Raiz**: A inicialização garantida de "Magic" elimina o bug original do loop infinito.

#### Subcomponente 3: Integração e Testes - ✅ COMPLETO
- ✅ **Teste de Circuit Breaker**: Validado que o loop infinito não ocorre mais.
- ✅ **Teste de Inicialização**: Verificado que os personagens são criados com stats aleatórios e "Magic" presente.
- ✅ **Teste de Compatibilidade**: Confirmado que o efeito "set-occupation" funciona como esperado.
- ✅ **Documentação**: `planning.instructions.md` (este arquivo) atualizado para refletir a conclusão da FASE 2.
```
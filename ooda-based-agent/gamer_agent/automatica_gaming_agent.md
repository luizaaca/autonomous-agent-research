# Documento de Design Técnico: Agente de Jogo Automático

**Versão:** 1.3
**Autor:** @luizaaca
**Data:** 2025-09-07
**Atualização:** Sistema de UI/Logging Melhorado implementado

## 1. Visão Geral

Este documento detalha a arquitetura e as especificações para um sistema de agente de jogo avançado. O objetivo é criar uma estrutura robusta e extensível que suporte múltiplos modos de interação (demonstração, jogador humano e IA via LLM) e que seja baseada em uma análise completa das mecânicas do jogo "The Domestic".

O design segue as melhores práticas de desenvolvimento de jogos, incluindo a separação de responsabilidades, o uso de padrões de design como **Repository** e **Dependency Injection**, e a criação de uma especificação detalhada da ficha de personagem e da lógica condicional do jogo.

---

## 2. Arquitetura

A arquitetura do sistema busca seguir princípios de design limpo, com clara separação de responsabilidades, e evoluiu para um design extensível que suporta múltiplos tipos de jogadores.

### 2.1. Arquitetura de Componentes (Estado Atual - v1.1)

A implementação atual utiliza o padrão `DecisionController` com injeção de dependência:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    Character    │    │ GameRepository  │    │ DecisionCtrlrs  │
│                 │    │                 │    │                 │
│ • Backstory     │    │ • Padrão Repo   │    │ • Default       │
│ • Ocupação      │    │ • Cache+Valid   │    │ • Random        │
│ • Habilidades   │    │ • 112 páginas   │    │ • Retorna Dict  │
│ • game_backstry │    │ • Interface .get│    │ • (Usado atual) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ▲                      ▲                      ▲
         │                      │                      │
         └──────────────────────┼──────────────────────┘
                                │
                        ┌─────────────────┐
                        │     Agent       │
                        │                 │
                        │ • OODA Loop     │
                        │ • Cockpit       │
                        │ • DI Pattern    │
                        └─────────────────┘
                                ▲
                                │
                        ┌─────────────────┐
                        │    main.py      │
                        │                 │
                        │ • Entry Point   │
                        │ • Orchestrator  │
                        │ • Scenario Cfg  │
                        └─────────────────┘
```

### 2.2. Arquitetura Alvo com Player Adapters (v1.2 - Implementação Confirmada)

**DECISÕES ARQUITETURAIS CONFIRMADAS:**
- **Evolução do DecisionController → PlayerInputAdapter** (Opção C)
- **Retorno: choice_index (int)** em vez de choice dict
- **Construtor Agent: `Agent(character, game_repository, player_input_adapter)`**
- **Ocupação definida dinamicamente** via `"set-occupation"` effect

Para suportar diferentes interfaces de jogador (automática, humana, IA), a arquitetura evolui usando o padrão **Adapter**. Isso desacopla a **lógica de decisão** da **captura de entrada**, substituindo o `DecisionController` por `PlayerInputAdapter`.

O diagrama abaixo ilustra esta arquitetura alvo confirmada:

```
        ┌─────────────┐
        │   main.py   │
        │ • argparse  │
        │ • player    │
        │   selection │
        └─────────────┘
               │
        (Cria e Injeta)
               │
               ▼
        ┌─────────────┐
        │    Agent    │
        │ • character │
        │ • game_repo │
        │ • player_   │
        │   adapter   │
        └─────────────┘
      ┌─────────┼───────────┬────────────────┐
    (Usa)     (Usa)       (Usa)            (Usa)
      │         │           │                │
      ▼         ▼           ▼                ▼
┌─────────┐ ┌─────────┐ ┌───────┐ ┌────────────────────┐
│Character│ │GameRepo │ │Cockpit│ │ PlayerInputAdapter │
│• No occ │ │• 112 pgs│ │• Rich │ │    (Interface)     │
│  initial│ │• Cache  │ │• Video│ │ • get_decision()   │
│• Dynamic│ │         │ │  Game │ │ • returns int      │
│         │ │         │ │• JSON │ │                    │
│         │ │         │ │  Log  │ │                    │
└─────────┘ └─────────┘ └───────┘ └────────────────────┘
                                             ▲
                                             │
                                       (Implementa)
                        ┌────────────────────┼────────────────────┐
                        │                    │                    │
                        ▼                    ▼                    ▼
               ┌────────────────┐   ┌────────────────┐   ┌────────────────┐
               │  DemoAdapter   │   │ HumanAdapter   │   │   LLMAdapter   │
               │• Uses Default  │   │• Console I/O   │   │• API Call      │
               │  Controller    │   │• Input Loop    │   │• Response Parse│
               │• Returns Index │   │• Validation    │   │• Error Handle  │
               └────────────────┘   └────────────────┘   └────────────────┘
```


### 2.3. Fluxo do Jogo (Ciclo OODA) - v1.2 Confirmado

O fluxo de decisão principal segue o ciclo OODA, com a interação do `PlayerInputAdapter` retornando **choice_index (int)**.

**FLUXO CONFIRMADO:**
1. PlayerInputAdapter retorna `choice_index` (int, base 1)
2. Agent converte para base 0: `chosen_choice = choices[choice_index - 1]`
3. Agent processa efeitos (incluindo `"set-occupation"`)
4. Validação de regras permanece no Agent

```
[main.py]          [Agent]               [Character]     [PlayerInputAdapter]
    │                  │                      │                    │
    │ agent.run()      │                      │                    │
    │─────────────────>│                      │                    │
    │                  │                      │                    │
    │                  │<──────────────────────────────────────────┐
    │                  │ Loop: Ciclo OODA     │                    │
    │                  │                      │                    │
    │                  │ 1.Observe (Lê estado)│                    │
    │                  │─────────────────────>│                    │
    │                  │<─────────────────────│                    │
    │                  │                      │                    │
    │                  │ 2. Orient (Prepara cockpit)               │
    │                  │─────────────────────>│                    │
    │                  │<─────────────────────│                    │
    │                  │                      │                    │
    │                  │ 3. Decide (get_decision) → returns int    │
    │                  │──────────────────────────────────────────>│
    │                  │                      │ Renderiza cockpit  │
    │                  │                      │ e obtém input      │
    │                  │                      │<───────────────────│        
    │                  │                      │───────────────────>│        
    │                  │                      │                    │
    │                  │ Retorna choice_index (int)                │
    │                  │<------------------------------------------│
    │                  │                      │                    │
    │                  │ 4. Get choice dict: choices[index-1]      │
    │                  │─────────────────────>│                    │
    │                  │                      │                    │
    │                  │ 5. Valida Escolha + Processa Efeitos      │
    │                  │<─────────────────────┐                    │
    │                  │─────────────────────>│                    │
    │                  │                      │                    │
    │                  │┌─────────────────────────────────────────┐│
    │                  ││ AGENT                                   ││
    │                  ││ alt: Escolha Inválida                   ││
    │                  ││                                         ││
    │                  ││ add_history_log("Erro...")              ││
    │                  ││─────┐                                   ││
    │                  ││ <───┘                                   ││
    │                  ││ (Reinicia o ciclo na mesma página)      ││
    │                  │└─────────────────────────────────────────┘│
    │                  │┌─────────────────────────────────────────┐│
    │                  ││ AGENT                                   ││
    │                  ││ else: Escolha Válida                    ││
    │                  ││                                         ││
    │                  ││ 6. Act (Aplica efeitos + set-occupation)││
    │                  ││─────┐                                   ││
    │                  ││ <───┘                                   ││
    │                  ││                                         ││
    │                  ││ (Avança para próxima página)            ││
    │                  │└─────────────────────────────────────────┘│
    │                  │                                           │
    │                  │─────────────────────END───────────────────│
    │                                                             
```

Este fluxo garante que o `Agent` mantenha a autoridade sobre a lógica e as regras do jogo, enquanto os `Adapters` focam exclusivamente na responsabilidade de interface com o jogador (seja ele um script, um humano ou uma IA).

---

### 2.4. Sistema de UI/Logging Melhorado (v1.3 - Implementado)

**MELHORIAS IMPLEMENTADAS:**
- **Interface "Video-Game"**: Cockpit compacto usando `rich.Panel` e `rich.Table`.
- **Logging JSON Separado**: Dados técnicos em formato JSON estruturado.
- **Controle Manual**: Pausa com ENTER em todos os modos.
- **Histórico Separado**: Últimas jogadas aparecem em um painel dedicado para maior clareza.
- **Choices Descritivas**: As opções de escolha agora detalham suas ações (e.g., `goto`, `roll`, `effects`).

### Fluxo de UI/Logging (v1.3):

```
[COCKPIT - TELA DE VIDEO-GAME]
┌─────────────────────────────┐
│ 📋 PERSONAGEM │ ⚡ RECURSOS │
│ Nome: Agent   │ Sorte: 75/75 │
│ Ocupação: N/A │ Magia: 14/14 │
├─────────────────────────────┤
│ 📜 HISTÓRICO DE DECISÕES    │
│ Página 1: Escolheu "Se você é um Policial (Police Officer)" (goto: 9)
├─────────────────────────────┤
│ SITUAÇÃO ATUAL              │
│ ...texto da página atual... │
├─────────────────────────────┤
│ 🎯 ESCOLHAS DISPONÍVEIS     │
│ ESCOLHAS ATUAIS:            │
│ [1] - (goto: 17)            │
└─────────────────────────────┘

📋 LOG DA JOGADA:
{
  "page": 9,
  "choice_selected": {
    "index": 1,
    "choice_data": {
      "goto": 17
    }
  },
  "execution_result": "Executada com sucesso"
}

> Pressione ENTER para continuar...
```

### Características do Sistema:

1. **Interface Compacta**: Informações organizadas em tabelas visuais.
2. **Separação Clara**: UI visual separada dos dados técnicos JSON.
3. **Histórico Dedicado**: O histórico de decisões é exibido em seu próprio painel.
4. **Choices Informativas**: As escolhas mostram os detalhes de suas ações, eliminando ambiguidades.
5. **Controle Total**: Usuário avança no próprio ritmo.

---

## 3. Especificação da Ficha de Personagem

A ficha do personagem é a estrutura de dados central que representa o estado do jogador. A seguir, uma análise completa de cada campo, com os valores possíveis identificados no código-fonte (`character.py`) e no conteúdo do jogo (`pages.py`).

### 3.1. Estrutura Base (`_create_base_sheet`)

```json
{
    "info": {
        "name": "string",
        "occupation": "string | null",
        "age": "int",
        "backstory": "string"
    },
    "contacts": {},
    "case_files": [],
    "magic": {
        "spells": [],
        "signare": []
    },
    "characteristics": {
        "STR": {"full": "int", "half": "int"},
        "CON": {"full": "int", "half": "int"},
        "DEX": {"full": "int", "half": "int"},
        "INT": {"full": "int", "half": "int"},
        "POW": {"full": "int", "half": "int"}
    },
    "resources": {
        "luck": {"starting": "int", "current": "int"},
        "magic_pts": {"starting": "int", "current": "int"},
        "mov": 8
    },
    "skills": {
        "common": {},
        "combat": {},
        "expert": {}
    },
    "status": {
        "damage_levels": [],
        "damage_taken": "int",
        "modifiers": []
    },
    "inventory": {
        "equipment": [],
        "weapons": []
    },
    "page_history": []
}
```

### 3.2. Valores Possíveis por Campo

#### `info.occupation`
As ocupações definem os atributos e habilidades iniciais do personagem. **IMPORTANTE: A ocupação é definida dinamicamente durante o jogo via efeito `"set-occupation"`.**
- `Police Officer`
- `Social Worker`
- `Nurse`
- `null` (Estado inicial - sem ocupação definida)

#### `characteristics`
Atributos principais do personagem. Os valores são definidos pela ocupação.
- `STR` (Força)
- `CON` (Constituição)
- `DEX` (Destreza)
- `INT` (Inteligência)
- `POW` (Poder)

#### `skills.common`
Habilidades básicas disponíveis para todos os personagens.
- `Athletics`
- `Drive`
- `Navigate`
- `Observation`
- `Read Person`
- `Research`
- `Social`
- `Stealth`

#### `skills.combat`
Habilidades de combate.
- `Fighting`
- `Firearms`

#### `skills.expert`
Habilidades especializadas, geralmente adquiridas durante o jogo.
- `Law` (Inicial para Police Officer)
- `Medicine` (Inicial para Nurse)
- `Magic` (Inicial para todas as ocupações)
- `Impello` (Ganhável)
- `Scindere` (Ganhável)
- `Animal Handling` (Ganhável)

#### `magic.spells`
Feitiços que o personagem pode aprender e usar.
- `Werelight` (Implícito como feitiço inicial)
- `Impello`
- `Scindere`

#### `status.damage_levels`
Representa os estágios de saúde do personagem.
- `Healthy`
- `Hurt`
- `Bloodied`
- `Down`
- `Impaired` (Estado de "morte" ou incapacitação)

#### `status.modifiers`
Efeitos temporários que afetam as rolagens de dados.
- `type`: `penalty_dice` | `bonus_dice`
- `skill`: Nome da habilidade afetada (e.g., "Fighting")
- `duration`: Número de usos restantes

#### `inventory`
Itens que o personagem pode adquirir. Embora o sistema suporte a adição de itens, a história atual menciona os seguintes itens que podem ser considerados parte do inventário em uma implementação futura:
- **Equipment**: `warrant card`, `sausages`, `bandages`, `Health Emergency Badge`.
- **Weapons**: `cricket bat`, `masonry hammer`, `carriage clock`.

---

## 4. Análise da Lógica Condicional

O fluxo do jogo é determinado por uma série de escolhas e condições. A análise a seguir detalha os padrões de controle de fluxo e as ações que modificam o estado do jogo, com base em `pages.py` e `character.py`.

### 4.1. Padrões de Controle de Fluxo

- **Navegação Simples**: A escolha leva diretamente para outra página.
  - `{"text": "...", "goto": 10}`
- **Escolha Condicional por Ocupação**: O caminho a seguir depende da ocupação do personagem.
  - `{"conditional_on": "occupation", "paths": {"Police Officer": {...}, "default": {...}}}`
- **Rolagem de Habilidade/Característica**: O resultado de uma rolagem de dados determina a próxima página.
  - `{"roll": "Magic", "results": {"5": {...}, "2": {...}}}`
- **Rolagem de Sorte**: Um tipo especial de rolagem que usa os pontos de sorte do personagem.
  - `{"luck_roll": true, "results": {...}}}`
- **Rolagem Oposta**: Uma disputa entre o personagem e um oponente.
  - `{"opposed_roll": "Fighting", "opponent_skill": {...}, "outcomes": {"win": {...}, "lose": {...}}}`
- **Escolha com Pré-requisitos (Implícita)**: ✅ **CORRIGIDO EM v1.2** - Convertido para `conditional_on` pattern.
  - **Antes**: `{"text": "Se você é um Policial, identifique-se", "goto": 19}` 
  - **Agora**: `{"conditional_on": "occupation", "paths": {"Police Officer": {...}, "default": {...}}}`
  - **Páginas Atualizadas**: 6, 43, 44, 74 

### 4.2. Ações e Efeitos (`effects`)

Estas são as ações que modificam a ficha do personagem.

| Ação              | Parâmetros          | Descrição                                                 | Exemplo (`pages.py`) |
| ----------------- | ------------------- | --------------------------------------------------------- | -------------------- |
| `take_damage`     | `amount: int`       | Aplica dano ao personagem.                                | Página 12, 48, 89    |
| `heal_damage`     | `amount: int`       | Cura o dano do personagem.                                | Página 2             |
| `spend_magic`     | `amount: int`       | Gasta pontos de magia.                                    | Página 26, 41, 69    |
| `spend_luck`      | `amount: int`       | Gasta pontos de sorte.                                    | Página 85            |
| `gain_skill`      | `skill: str`        | Adquire uma nova habilidade (geralmente expert).          | Página 10, 92        |
| `apply_penalty`   | `skill: str`, `duration: int` | Aplica uma penalidade (penalty dice) a uma habilidade. | Página 60            |
| `set-occupation`  | `string`            | Define a ocupação inicial do personagem.                  | Página 1             |

---

## 5. Arquitetura da Interface do Jogador (Player Interface)

Para acomodar diferentes modos de jogo (automático, humano e IA), propõe-se o uso do padrão de design **Adapter**. Este padrão permite que a lógica principal do jogo (`Agent`) interaja com diferentes tipos de "controladores" de jogador através de uma interface comum, sem precisar conhecer os detalhes de implementação de cada um.

### 5.1. O Padrão Adapter

A arquitetura será composta por:
1.  **`PlayerInputAdapter` (Interface Abstrata)**: Define o contrato que todos os adaptadores de entrada devem seguir.
2.  **Implementações Concretas**: Classes que implementam a interface para cada modo de jogo.
3.  **`Agent` (Consumidor)**: A classe `Agent` utilizará um `PlayerInputAdapter` para obter a decisão do jogador a cada turno.

### 5.2. `PlayerInputAdapter` (Interface)

Será definida uma classe base abstrata em Python.

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class PlayerInputAdapter(ABC):
    """
    Interface abstrata para adaptadores de entrada do jogador.
    Define o contrato para obter uma decisão de um jogador,
    seja ele um humano, uma IA ou um script de demonstração.
    """
    @abstractmethod
    def get_decision(self, available_choices: List[Dict[str, Any]], cockpit_state: str) -> int:
        """
        Obtém o índice da escolha selecionada pelo jogador.

        Args:
            available_choices: A lista de objetos de escolha disponíveis na página atual.
            cockpit_state: Uma representação em string do estado atual do jogo (o cockpit)
                           para fornecer contexto ao jogador.

        Returns:
            O índice (base 1) da escolha selecionada.
        """
        pass
```

### 5.3. Implementações Concretas

#### a) `DemoPlayerAdapter`
- **Propósito**: Executar o jogo de forma não interativa para demonstrações ou testes.
- **Lógica**: Utilizará a lógica do `DefaultDecisionController`. Se houver múltiplas escolhas simples (não condicionais), uma será selecionada **aleatoriamente** para variar a jogabilidade. Caso contrário (escolha única ou condicional), a primeira opção válida será selecionada.
- **Fluxo**: `Agent` chama `get_decision` → `DemoPlayerAdapter` aplica lógica de decisão → Encontra choice no array → Retorna o índice da escolha (int).
- **Implementação**: Interno ao adapter, sem exposição do DecisionController.

#### b) `HumanPlayerAdapter`
- **Propósito**: Permitir que um jogador humano jogue através do terminal.
- **Lógica**:
    1.  Implementa um laço de entrada (`input loop`).
    2.  Renderiza o `cockpit_state` no terminal a cada turno.
    3.  Exibe as `available_choices` formatadas com um número (e.g., `[1] Bater na porta`, `[2] Olhar pela janela`).
    4.  Aguarda o usuário digitar um número e pressionar Enter.
    5.  Valida a entrada: se não for um número ou estiver fora do intervalo de escolhas válidas, exibe uma mensagem de erro e solicita a entrada novamente.
    6.  Retorna o número da escolha válida.

#### c) `LLMPlayerAdapter`
- **Propósito**: Permitir que um agente de IA (LLM) jogue o jogo.
- **Lógica**:
    1.  Recebe o `cockpit_state`, que já é um prompt formatado para LLMs (compactar visualizaçao adotando informações em tabelas).
    2.  Envia este prompt para uma API de LLM (e.g., Google AI, OpenAI).
    3.  Aguarda a resposta da API.
    4.  Processa a resposta para extrair um único número correspondente à escolha.
    5.  Valida a resposta: se a resposta não for um número ou estiver fora do intervalo, tenta processar novamente ou retorna um valor de erro.
    6.  Retorna o número da escolha.

### 5.4. Tratamento de Escolhas Inválidas

A responsabilidade de **obter** a escolha é do `PlayerInputAdapter` (retorna choice_index), mas a de **validar** a escolha contra as regras do jogo (e.g., pré-requisitos de ocupação) permanece com o `Agent`.

**FLUXO CONFIRMADO (v1.2):**
1.  O `Agent` determina as escolhas válidas para a página atual.
2.  O `Agent` chama `choice_index = player_input_adapter.get_decision(available_choices, cockpit_state)` (retorna int).
3.  O `Agent` obtém a escolha: `chosen_choice = available_choices[choice_index - 1]` (converte para base 0).
4.  O `Agent` verifica se a escolha selecionada é genuinamente válida de acordo com o estado atual do personagem.
5.  **Se a escolha for inválida**:
    - O `Agent` **não** avança para a próxima página.
    - Uma mensagem de erro é adicionada ao histórico do `cockpit`. Ex: `"Tentativa de usar autoridade policial falhou. Ocupação atual: Enfermeiro. Por favor, escolha novamente."`
    - O `Agent` repete o passo 2, apresentando novamente as mesmas opções ao jogador no mesmo turno.
6.  **Se a escolha for válida**:
    - O `Agent` processa os efeitos da escolha (incluindo `"set-occupation"`) e avança para a próxima página.

Esta abordagem garante que a interface do jogador (humano ou IA) possa tentar qualquer ação, mas o motor do jogo (`Agent`) tem a autoridade final para garantir que as regras sejam cumpridas, fornecendo feedback claro em caso de falha.

---

## 6. Roteiro de Implementação

Esta seção descreve os passos práticos para implementar a arquitetura de `PlayerInputAdapter` no código existente.

### 6.1. Estrutura de Arquivos

Serão criados os seguintes arquivos no diretório `gamer_agent/`:

- `player_input_adapter.py`: Conterá a classe abstrata `PlayerInputAdapter`.
- `player_adapters.py`: Conterá as implementações concretas: `DemoPlayerAdapter`, `HumanPlayerAdapter`, e `LLMPlayerAdapter`. Manter as implementações juntas neste arquivo simplifica a gestão de dependências.

### 6.2. Passo 1: Criar a Interface e os Adaptadores

- **`player_input_adapter.py`**:
  - Criar a classe `PlayerInputAdapter(ABC)` exatamente como especificado na seção 5.2.

- **`player_adapters.py`**:
  - Importar `PlayerInputAdapter` e outras dependências necessárias.
  - Implementar `DemoPlayerAdapter(PlayerInputAdapter)`:
    - Internalizar a lógica de decisão do `DefaultDecisionController` atual.
    - O método `get_decision` aplicará a lógica e retornará o índice da escolha (int).
    - **Não** expor `DefaultDecisionController` externamente.
  - Implementar `HumanPlayerAdapter(PlayerInputAdapter)`:
    - O método `get_decision` implementará o loop de input no console, tratando entradas inválidas (não numéricas, fora do range) até que uma escolha válida seja inserida.
    - Retorna o índice da escolha válida (int).
  - Implementar `LLMPlayerAdapter(PlayerInputAdapter)`:
    - O método `get_decision` conterá a lógica para chamar a API do LLM.
    - Processar resposta da API para extrair o índice da escolha.
    - Incluir tratamento de erro para respostas mal formatadas da API.
    - Retorna o índice da escolha (int).

### 6.3. Passo 2: Refatorar a Classe `Agent`

A classe `Agent` em `agent.py` será modificada para usar o sistema de injeção de dependência com `PlayerInputAdapter`.

- **Construtor (`__init__`)**:
  - **MUDANÇA CONFIRMADA**: Modificar a assinatura para `__init__(self, character: Character, game_repository: GameRepository, player_input_adapter: PlayerInputAdapter)`.
  - Armazenar `self.player_input_adapter = player_input_adapter`.
  - Remover a instanciação direta do `DefaultDecisionController`.
  - **Character sem ocupação inicial**: Ocupação será definida via `"set-occupation"` effect.

- **Método `run` (OODA Loop)**:
  - **Observe**: O agente já observa o estado.
  - **Orient**: O agente determina as escolhas disponíveis.
  - **Decide**:
    - Chamar `choice_index = self.player_input_adapter.get_decision(available_choices, cockpit_state)`.
    - **Conversão**: `chosen_choice = available_choices[choice_index - 1]` (converter para base 0).
  - **Validação**: Após obter `chosen_choice`, o `Agent` valida se a escolha é permitida pelas regras do jogo.
    - **Se inválida**:
      - Adicionar uma mensagem ao histórico do `character`. Ex: `self.character.add_history_log("Invalid choice: 'Use police authority' requires 'Police Officer' occupation. Please try again.")`.
      - Chamar `continue` no loop para recomeçar o ciclo OODA na mesma página, sem alterar o estado do jogo.
    - **Se válida**:
      - Continuar com a execução da escolha.
  - **Act**: Aplicar os efeitos da escolha (incluindo `"set-occupation"` se não houver ocupação previa, deve validar e retornar opção inválida) e atualizar a página atual.

### 6.4. Passo 3: Refatorar a Classe `Cockpit`

A classe `Cockpit` em `cockpit.py` precisa garantir que as mensagens de erro de escolha inválida sejam exibidas.

- **Método `render_page`**:
  - O método já exibe o `page_history`. A lógica de adicionar a mensagem de erro no `Agent` (passo 2) é suficiente por enquanto, nenhuma grande mudança é necessária aqui, desde que o histórico seja renderizado de forma clara. Adicionar um prefixo como `[SYSTEM]` ou `[ERROR]` às mensagens de log para diferenciá-las das ações do jogo.
  - Esse método deve retornar um objeto com todas as informações necessarias para renderização pelo adapter.
  - Cada adapter vai fazer sua renderização de acordo com sua necessidade

### 6.5. Passo 4: Atualizar o Ponto de Entrada (`main.py`)

O arquivo `main.py` será o responsável por configurar e injetar o adaptador de jogador correto.

- **Lógica de Inicialização**:
  - Usar `argparse` para ler um argumento de linha de comando, e.g., `--player {demo,human,llm}`.
  - **Character sem ocupação inicial**: `character = Character(name="Agent", occupation=None)`.
  - Com base no argumento, instanciar o adaptador correspondente:
    ```python
    if args.player == 'human':
        player_adapter = HumanPlayerAdapter()
    elif args.player == 'llm':
        player_adapter = LLMPlayerAdapter(api_key=os.getenv("GEMINI_API_KEY"))
    else: # default to demo
        player_adapter = DemoPlayerAdapter()  # Sem DecisionController externo
    ```
  - Instanciar o `Agent` com o adaptador escolhido:
    ```python
    agent = Agent(
        character=character,
        game_repository=game_repo,
        player_input_adapter=player_adapter
    )
    ```
  - Iniciar o loop do jogo: `agent.run()`.

Com este roteiro, a implementação se torna uma tarefa estruturada de criar os novos módulos e refatorar os existentes para acomodar a nova arquitetura flexível.

---

## 7. Status da Implementação Atual (v1.3)

### ✅ Componentes Implementados:

#### `Agent` (OODA Core)
- **Status**: Completamente implementado e testado
- **Características v1.3**:
  - Loop OODA simplificado com pause manual universal
  - Logging JSON estruturado via `_log_turn_summary()`
  - Interface limpa sem prints de diagnóstico
  - Controle de entrada para todos os player adapters

#### `Cockpit` (Interface "Video-Game")
- **Status**: Implementado com redesign completo
- **Características v1.3**:
  - Layout compacto usando `rich.Panel` e `rich.Table`
  - **Histórico exibido em painel dedicado** para maior clareza.
  - **Formato descritivo para choices**, detalhando suas ações (e.g., `[1] - (goto: 17)`).
  - Separação visual clara entre informações.

#### `PlayerInputAdapter` (Arquitetura Flexível)
- **Status**: Totalmente implementado com todos os adapters
- **Implementações disponíveis**:
  - `DemoAdapter`: Simulação automática para testes, **com lógica de decisão aleatória para escolhas simples**.
  - `HumanAdapter`: Interface para jogador humano.
  - `LLMAdapter`: Integração com IA (estrutura preparada).

#### `Character` & `GameRepository`
- **Status**: Implementados e funcionais
- **Características**: Sistema completo de stats, inventory e content management.

### 🧪 Teste de Validação:
```bash
# Sistema testado com sucesso em:
python main.py --player demo

# Output confirma:
✅ Interface cockpit compacta e reorganizada
✅ Choices no formato descritivo
✅ Histórico em painel separado
✅ Logging JSON separado
✅ Controle manual com ENTER
```

### 📋 Próximos Passos:
- **Expansão de Content**: Adicionar mais páginas do jogo
- **LLM Integration**: Implementar chamadas de API no LLMAdapter
- **Performance**: Otimizações para históricos longos
- **Testing**: Suíte de testes automatizados
# Especificação Arquitetural: MVP para Jogo de Texto Autônomo

## Visão Geral
Este documento define a arquitetura refinada para o projeto "Agente de Jogo Autônomo", baseada na análise crítica realizada e nas melhores práticas da indústria de jogos. A arquitetura adota o padrão MVP (Model-View-Presenter) como estrutura principal, garantindo separação clara de responsabilidades.

## Princípios Arquiteturais Fundamentais

1. **Separação de Responsabilidades Rigorosa**: Cada componente tem uma única responsabilidade bem definida
2. **Princípio Aberto/Fechado**: Extensível sem modificação do código existente
3. **Injeção de Dependências**: Todos os componentes recebem suas dependências
4. **Testabilidade**: Arquitetura projetada para facilitar testes automatizados
5. **Conteúdo Separado de Código**: Dados do jogo em formato estruturado (YAML)

## Diagrama de Componentes

```
.--------------------.      .----------------------.      .------------------------.
|      main.py       |----->|  PlayerStrategy      |<---->|         Agent          |
| (Composition Root) |      | (Strategy Pattern)   |      |(Presenter/Orchestrator)|
'--------------------'      '----------------------'      '-----------+------------'
                                    ^                                  |
                                    | Implementa                       | Usa
                                    |                                  |
-----------------------------------------------------|                 |
.--------------------.      .----------------------. |    .------------+-----------.
| HumanStrategy      |      |   DemoStrategy       | |    |        Cockpit         |
'--------------------'      '----------------------' |    | (View/Rendering)       |
                                                     |    '-----------+------------'
.--------------------.                               |                 |
|   LLMStrategy      |                               |                 | Usa
|                    |                               |    .------------+-----------.
'--------------------'                               |    |        Character       |
-----------------------------------------------------|    |      (Model/State)     |
                                                          '-----------+------------'
                                                                       | Usa
                                                          .------------+-----------.
                                                          |      GameRepository    |
                                                          | (Data Access Layer)    |
                                                          '------------------------'
```

## Fluxo Arquitetural Correto (MVP)

### 1. Fluxo de Dados Principal
```
1. Presenter (Agent) solicita estado ao Model
   ↓
2. Model (Character + GameRepository) retorna dados para Presenter
   ↓
3. Presenter passa dados para View
   ↓
4. View (Cockpit + Renderer) renderiza conforme necessário
   ↓
5. View notifica Presenter de eventos de entrada
   ↓
6. Presenter processa entrada e atualiza Model
```

### 2. Ciclo OODA no Agent (Presenter)
```python
def run(self):
    while self.character.is_alive() and not self.game_repository.is_game_complete():
        # O - Observe
        game_state = self.cockpit.get_current_state()
        
        # O - Orient
        render_output = self.renderer.render(game_state)
        
        # D - Decide
        choice_index = self.input_strategy.get_decision(render_output)
        
        # A - Act
        self.perform_action(choice_index)
```

### 3. Responsabilidades Claras

**Model (Dados):**
- `Character`: Encapsula estado do personagem e regras de negócio
- `GameRepository`: Gerencia conteúdo do jogo e lógica de navegação

**Presenter (Lógica):**
- `Agent`: Orquestra o ciclo OODA, é o "cérebro" do jogo
- Responsável por: 
  - Controlar o fluxo do jogo
  - Processar decisões
  - Atualizar o modelo
  - Coordenar entre View e Model

**View (UI):**
- `Cockpit`: Agregador de dados (fachada para o estado do jogo)
- `IRenderer` + Implementações: Estratégias de renderização
  - `ConsoleRenderer`: Para interface console
  - `LLMPromptRenderer`: Para formatação de prompts LLM
  - `HtmlRenderer` (futuro): Para interface web

## Estrutura de Conteúdo (YAML)

### Schema de Páginas
```yaml
id: 1
title: "Bem-vindo à Aventura"
content: "Você está em uma floresta sombria..."
choices:
  - id: 1
    text: "Seguir para o norte"
    conditions: 
      stamina: ">5"
    effects: 
      stamina: "-2"
  - id: 2
    text: "Descansar"
    effects: 
      stamina: "+3"
```

### Validação de Schema
- Schema JSON definido em `content/schema.json`
- Validação automática no carregamento do conteúdo
- Garante integridade dos dados do jogo

## Estratégias de Input (Player Strategies)

### Interface Comum
```python
class PlayerStrategy(ABC):
    @abstractmethod
    def get_decision(self, render_output) -> int:
        """Obtém decisão do jogador (índice da escolha)"""
        pass
```

### Implementações
- `HumanStrategy`: Recebe entrada do console
- `DemoStrategy`: Lógica de decisão automática (aleatória)
- `LLMStrategy`: Interage com API de LLM para tomar decisões

## Fluxo de Renderização

### Passo a Passo
1. `Agent` solicita estado atual ao `Cockpit`
2. `Cockpit` agrega dados do `Character` e `GameRepository`
3. `Agent` passa o estado para o `Renderer` apropriado
4. `Renderer` gera saída formatada (console, prompt LLM, etc.)
5. `Agent` passa a saída para o `PlayerStrategy`
6. `PlayerStrategy` obtém decisão do jogador/IA

### Exemplo de Renderização para Console
```
┌──────────────────────────────────────────────────────────┐
│ Aventura                                               │
├──────────────────────────────────────────────────────────┤
│ Você está em uma floresta sombria...                    │
├──────────────────────────────────────────────────────────┤
│ Atributo    Valor                                       │
│─────────────────────────────────────────────────────────│
│ Vida        10                                          │
│ Energia     8                                           │
│ Sorte       5                                           │
│ Magia       5                                           │
├──────────────────────────────────────────────────────────┤
│ Escolhas Disponíveis                                   │
├──────────────────────────────────────────────────────────┤
│ 1. Seguir para o norte [condição: stamina > 5] [efeitos: stamina -2] │
│ 2. Descansar [efeitos: stamina +3]                      │
└──────────────────────────────────────────────────────────┘

Digite o número da escolha desejada:
```

### Exemplo de Renderização para LLM
```
### JOGO DE RPG DE TEXTOS
Você está jogando um jogo de RPG de textos. Sua tarefa é escolher a próxima ação.

## Bem-vindo à Aventura
Você está em uma floresta sombria...

## Histórico
pagina 1: Escolheu ação X com resultado Y
pagina 2: ...

## STATUS DO PERSONAGEM
- Vida: 10
- Energia: 8
- Sorte: 5
- Magia: 5

## ATRIBUTOS
- DEX 60
- INT 70
- STR 65
- CON 60
- POW 70

## Skills
- Fighting 60
- Athletics 55
- Social 65

## ESCOLHAS DISPONÍVEIS
1. Seguir para o norte [condição: stamina > 5] [efeitos: stamina -2]
2. Descansar [efeitos: stamina +3]

## INSTRUÇÕES
Analise a situação e escolha a ação mais adequada. Responda APENAS com o número da escolha (1, 2, etc.).
Não inclua explicações ou texto adicional. Apenas o número da escolha.
```

## Critérios de Qualidade Arquitetural

1. **Testes Automatizados**: 
   - 90%+ cobertura para Character
   - 85%+ cobertura para GameRepository
   - Testes de integração para fluxo completo

2. **Separação Código-Conteúdo**:
   - Conteúdo em YAML validado por schema
   - Sistema de loader robusto
   - Scripts de validação automatizados

3. **Extensibilidade**:
   - Novos formatos de renderização sem modificar o Agent
   - Novas estratégias de input sem modificar o Cockpit
   - Suporte a múltiplos idiomas sem alteração de código

4. **Resiliência**:
   - Tratamento robusto de erros para LLM
   - Fallbacks adequados para falhas
   - Retry com backoff para APIs externas

## Notas para Implementação

1. **Priorize Testes**: Sem testes, qualquer refatoração é arriscada
2. **Comece Simples**: Implemente primeiro o fluxo básico antes de adicionar complexidade
3. **Evite God Objects**: Mantenha responsabilidades bem definidas
4. **Documente Decisões**: Use arquitetura baseada em documentação
5. **Mantenha o Fluxo MVP**: Nunca inverta a direção das dependências

Esta arquitetura garante que o projeto seja robusto, manutenível e escalável, permitindo que evolua de um protótipo funcional para um produto comercial viável.
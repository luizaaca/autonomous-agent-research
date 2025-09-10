# gamer_agent: Agente Autônomo para Jogos Narrativos

Este módulo implementa um agente autônomo capaz de navegar e tomar decisões em jogos narrativos baseados em páginas, como "The Domestic". A arquitetura é extensível, permitindo múltiplos modos de interação: demonstração automática, jogador humano e IA via LLM.

**Versão:** 0.1.4

## Principais mudanças nesta versão
- Refatoração completa da interface Cockpit, com painéis de atributos e histórico detalhado.
- Integração do LLMPlayerAdapter utilizando OpenRouter (API via variável de ambiente).
- Correções de bugs e melhorias na arquitetura dos adapters.
- Documentação revisada para refletir o novo fluxo de decisão e integração.

## Visão Geral da Implementação

- **Arquitetura OODA Loop:** O agente opera em ciclos de Observação, Orientação, Decisão e Ação, garantindo funcionamento contínuo e adaptativo.
- **Componentes Principais:**
  - `Character`: Modela o personagem, inventário, habilidades e estado.
  - `GameRepository`: Gerencia o mundo do jogo, páginas e transições.
  - `Cockpit`: Interface de controle e visualização, com painel de debug do estado do personagem.
  - `PlayerStrategy`: Estratégias de decisão (humano, demo, LLM).
- **Extensibilidade:** Suporte a novos tipos de estratégia e lógica condicional via injeção de dependências.

## Funcionalidades Entregues

- Navegação automática por páginas do jogo, com registro de decisões.
- Suporte a múltiplos modos de jogador (demo, humano, LLM).
- Painel de debug para inspeção do estado do personagem.
- Lógica de decisão modular, incluindo integração com LLM (OpenRouter API).
- Sistema de cache e invalidação para garantir atualização do estado.
- Estrutura pronta para expansão de regras, inventário e habilidades.

## Como Usar

1. **Pré-requisitos:** Python 3.12+, instalar dependências do projeto (ver requirements.txt).
2. **Execução Básica:**
   ```bash
   cd ooda-based-agent/gamer_agent
   python main.py
   ```
3. **Modos de Jogador:**
   - **Demo:** Executa navegação automática.
   - **Humano:** Permite entrada manual de decisões.
   - **LLM:** Requer configuração da variável de ambiente `OPENROUTER_API_KEY` para integração com LLM.
4. **Configuração do LLM:**
   - Defina a variável de ambiente:
     ```bash
     export OPENROUTER_API_KEY=seu_token_aqui
     ```
   - O agente usará o LLM para tomar decisões nas páginas do jogo.

## Estrutura dos Arquivos

- `agent.py`, `character.py`, `game_repository.py`: Núcleo do agente e lógica do jogo.
- `cockpit.py`: Interface de controle e painel de debug.
- `player_strategy.py`: Estratégias de decisão (humano, demo, LLM).
- `test_cockpit.py`: Testes unitários do Cockpit.
- Documentação técnica: `automatica_gaming_agent.md`, `conditional_logic_analysis.md`, etc.

## Extensão e Customização

- Para adicionar novas regras, páginas ou habilidades, edite os arquivos de lógica e repositório.
- Para integrar novos modelos LLM, adapte o módulo de estratégia (`player_strategy.py`).

## Roadmap

- Refatoração da arquitetura na v 0.2

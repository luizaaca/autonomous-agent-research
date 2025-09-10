"""
Player Adapters Module - Implementações concretas dos adaptadores de entrada

Este módulo contém as implementações concretas da interface PlayerInputAdapter
para diferentes modos de jogo: demonstração, humano e IA.
"""

from player_strategy_interface import PlayerStrategy
from typing import Dict, List, Any, Optional
from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns
from rich.text import Text
from rich.console import Console
from typing import Tuple, Optional
import json
import os, re
import random
import requests


class RenderConsole:
    """
    Encapsula toda a lógica de renderização da UI do jogo para um jogador humano,
    utilizando a biblioteca Rich para criar um "cockpit" informativo no console.
    """

    def __init__(self, debug: bool = False):
        self.console = Console()
        self._debug = debug

    def render_game_screen(
        self,
        choices: List[Dict[str, Any]],
        character_data: Dict[str, Any],
        history: List[Dict[str, Any]],
        current_page_data: Dict[str, Any],
        current_page_number: int,
    ) -> None:
        """
        Renderiza e exibe a tela de jogo completa, incluindo status, histórico,
        situação atual e escolhas.

        Este é o método principal que centraliza toda a UI do jogo.
        """
        # 1. Limpar console
        os.system("cls" if os.name == "nt" else "clear")
        self.console.clear()

        print(
            f"[RenderConsole] Renderizando tela do jogo - Página {current_page_number}\ncharacter_data keys: {list(character_data.keys())}, history entries: {len(history)}, choices: {len(choices)}"
        )
        # 2. Construir painéis de status
        info_panel = self._build_info_table(character_data)
        resources_panel = self._build_resources_table(character_data)
        attributes_panel = self._build_attributes_table(character_data)
        skills_panel = self._build_skills_table(character_data)

        status_layout = Columns(
            [info_panel, resources_panel, attributes_panel, skills_panel],
            equal=True,
            expand=True,
        )

        # 3. Construir painel de histórico
        history_panel = self._build_history_panel(history)

        # 4. Construir painel da situação atual
        page_text = current_page_data.get("text", "Página não encontrada.")
        page_panel = Panel(
            Text(page_text, style="white"), title="SITUAÇÃO ATUAL", border_style="cyan"
        )

        # 5. Construir painel de escolhas
        choices_panel = self._build_choices_panel(choices)

        # 6. Montar layout principal em um grid
        main_grid = Table.grid(padding=(1, 0), expand=True)
        main_grid.add_column()
        main_grid.add_row(status_layout)
        if history_panel:
            main_grid.add_row("")
            main_grid.add_row(history_panel)
        main_grid.add_row("")
        main_grid.add_row(page_panel)
        main_grid.add_row("")
        main_grid.add_row(choices_panel)

        main_panel = Panel(
            main_grid,
            title=f"🎮 COCKPIT - PÁGINA {current_page_number}",
            border_style="bold blue",
            expand=False,
        )

        # 7. Renderizar na tela
        self.console.print(main_panel)

    def _build_info_table(self, status_data: Dict[str, Any]) -> Panel:
        """Cria a tabela de informações básicas e saúde."""
        table = Table.grid(padding=(0, 1))
        table.add_column(style="bold cyan", justify="left")
        table.add_column(justify="left")

        info = status_data["character_info"]
        health = status_data["health_status"]

        table.add_row("NOME:", info["name"])
        table.add_row("OCUPAÇÃO:", info["occupation"])
        table.add_row("IDADE:", str(info["age"]))
        table.add_row(
            "SAÚDE:",
            f"{health['icon']} {health['current_level']} (Dano: {health['damage_taken']})",
        )

        return Panel(table, title="📋 PERSONAGEM", border_style="green")

    def _build_resources_table(self, status_data: Dict[str, Any]) -> Panel:
        """Cria a tabela de recursos (Sorte, Magia)."""
        table = Table.grid(padding=(0, 1))
        table.add_column(style="bold yellow", justify="left")
        table.add_column(justify="left")

        resources = status_data["resources"]

        table.add_row(
            "SORTE:", f"{resources['luck']['current']}/{resources['luck']['starting']}"
        )
        table.add_row(
            "MAGIA:",
            f"{resources['magic']['current']}/{resources['magic']['starting']}",
        )

        return Panel(table, title="⚡ RECURSOS", border_style="yellow")

    def _build_attributes_table(self, status_data: Dict[str, Any]) -> Panel:
        """Cria a tabela de atributos (características)."""
        table = Table.grid(padding=(0, 1))
        table.add_column(style="bold red", justify="left")
        table.add_column(justify="left", max_width=2)

        characteristics = status_data.get("characteristics", {})

        if not characteristics:
            table.add_row("N/A", "")
        else:
            for name, values in characteristics.items():
                table.add_row(f"{name}:", str(values.get("full", "")))

        return Panel(table, title="📊 ATRIBUTOS", border_style="red")

    def _build_skills_table(self, status_data: Dict[str, Any]) -> Panel:
        """Cria a tabela de habilidades."""
        table = Table.grid(padding=(0, 1))
        table.add_column(style="bold blue", justify="left")
        table.add_column(justify="left", max_width=2)

        skills = status_data.get("skills", {})

        if not skills:
            table.add_row("Nenhuma", "")
        else:
            for name, values in sorted(skills.items()):
                table.add_row(f"{name}:", f"{values.get('full', 0)}%")

        return Panel(table, title="🎯 HABILIDADES", border_style="blue")

    def _build_history_panel(self, history: List[Dict[str, Any]]) -> Optional[Panel]:
        """
        Cria um painel com o histórico das últimas decisões do jogador.
        Retorna None se não houver histórico.
        """
        if not history:
            return None

        content = Text()
        # Mostrar últimas 5 jogadas
        recent_history = history[-5:]

        for entry in recent_history:
            if isinstance(entry, dict):
                page_num = entry.get("page_number", 0)
                choice_made = entry.get("choice_made", {})

                choice_text = choice_made.get("text", "")
                # Se não houver texto, formata a ação para dar contexto
                if not choice_text:
                    choice_text = self._format_choice_text(choice_made)
                else:
                    choice_text = f'"{choice_text}"'

                # Construir string de resultado detalhado
                result_parts = []
                if "roll_result" in choice_made:
                    success_str = "SUCESSO" if choice_made.get("success") else "FALHA"
                    skill = choice_made.get("skill_used", "N/A")
                    roll = choice_made.get("roll_result", "N/A")
                    target = choice_made.get("target_value", "N/A")
                    result_parts.append(
                        f"Rolagem de {skill}: {roll} vs {target} -> {success_str}"
                    )

                if "effects_applied" in choice_made and choice_made["effects_applied"]:
                    effects_str_parts = []
                    for eff in choice_made["effects_applied"]:
                        action = eff.get("action", "unknown")
                        param = eff.get("amount") or eff.get("skill") or ""
                        effects_str_parts.append(f"{action}({param})")
                    result_parts.append(f"Efeitos: {', '.join(effects_str_parts)}")

                if "goto_executed" in choice_made:
                    result_parts.append(f"goto: {choice_made['goto_executed']}")

                result_info = ""
                if result_parts:
                    result_info = f" -> Resultado: {'; '.join(result_parts)}"

                history_line = (
                    f"Página {page_num}: Escolheu {choice_text}{result_info}\n"
                )
                content.append(history_line, style="dim white")

        return Panel(content, title="📜 HISTÓRICO DE DECISÕES", border_style="yellow")

    def _build_choices_panel(self, choices: List[Dict[str, Any]]) -> Panel:
        """
        Cria o painel que exibe apenas as escolhas atualmente disponíveis para o jogador.
        A lógica de histórico foi movida para _build_history_panel.
        """
        content = Text()

        if not choices:
            content.append(
                "🏁 FIM DO JOGO - Nenhuma escolha disponível.", style="bold red"
            )
        else:
            content.append("ESCOLHAS ATUAIS:\n", style="bold cyan")
            for i, choice in enumerate(choices, 1):
                # Formata a escolha de forma detalhada
                formatted_text = self._format_choice_text(choice)

                # Adicionar prefixo [SYSTEM] ou [ERROR] se for mensagem de sistema
                if formatted_text.startswith("[SYSTEM]") or formatted_text.startswith(
                    "[ERROR]"
                ):
                    content.append(f"  {formatted_text}\n", style="bold red")
                else:
                    content.append(f"[{i}] - {formatted_text}\n", style="white")

        return Panel(content, title="🎯 ESCOLHAS DISPONÍVEIS", border_style="magenta")

    def _format_choice_text(self, choice: Dict[str, Any]) -> str:
        """
        Formata o dicionário de uma escolha em um texto descritivo e legível.
        """
        # Se a escolha tiver um texto explícito, use-o como base
        text = choice.get("text", "")

        details = []
        # Adiciona detalhes sobre as ações da escolha
        if "goto" in choice:
            details.append(f"goto: {choice['goto']}")
        if "set-occupation" in choice:
            details.append(f"set-occupation: '{choice['set-occupation']}'")
        if "roll" in choice:
            details.append(f"roll: {choice['roll']}")
        if "luck_roll" in choice:
            details.append("roll: luck")
        if "opposed_roll" in choice:
            details.append(f"opposed_roll: {choice['opposed_roll']}")
        if "effects" in choice:
            effects_desc = []
            for effect in choice["effects"]:
                action = effect.get("action", "unknown_action")
                if action == "take_damage":
                    effects_desc.append(f"damage: {effect.get('amount', '?')}")
                elif action == "gain_skill":
                    effects_desc.append(f"gain_skill: {effect.get('skill', '?')}")
                elif action == "spend_magic":
                    effects_desc.append(f"spend_magic: {effect.get('amount', '?')}")
                else:
                    effects_desc.append(action)
            details.append(f"effects: {', '.join(effects_desc)}")

        # Monta a string final
        if details:
            details_str = f"({', '.join(details)})"
            return f"{text} {details_str}" if text else details_str

        return text or "Ação sem descrição"


class DemoPlayerAdapter(PlayerStrategy):
    """
    Adapter para execução automática/demonstração.
    Internaliza a lógica do DefaultDecisionController para tomar decisões automáticas.
    """

    def __init__(self, debug: bool = False):
        """
        Inicializa o DemoPlayerAdapter.

        Args:
            debug: Se True, exibe informações de debug durante a decisão.
        """
        self._debug = debug
        self._last_decision_reason = ""
        self.renderer = RenderConsole(debug)

    def get_decision(
        self,
        available_choices: List[Dict[str, Any]],
        character_data: Dict[str, Any],
        history: List[Dict[str, Any]],
        current_page_data: Dict[str, Any],
        current_page_number: int,
    ) -> Tuple[int, str]:
        """
        Toma decisão automática baseada na lógica internalizada do DefaultDecisionController.

        Args:
            available_choices: Lista de choices disponíveis
            character_data: Dados estruturados do personagem
            history: Histórico de decisões anteriores

        Returns:
            Índice (base 1) da escolha selecionada
        """
        if self._debug:
            print(f"[DemoPlayerAdapter] Processando {len(available_choices)} choices")

        self.renderer.render_game_screen(
            choices=available_choices,
            character_data=character_data,
            history=history,
            current_page_data=current_page_data,
            current_page_number=current_page_number,
        )

        # Validação básica
        if not available_choices:
            raise Exception("Lista de choices vazia - não é possível tomar decisão")

        if len(available_choices) > 1:
            selected_index = random.choice(range(len(available_choices)))
            self._last_decision_reason = (
                f"Seleção aleatória entre {len(available_choices)} opções básicas."
            )
        else:
            selected_index = 0
            self._last_decision_reason = "Única escolha básica disponível."

        choice_text = available_choices[selected_index].get(
            "text", str(available_choices[selected_index])[:50]
        )
        print(f"[DemoPlayerAdapter] Razão: {self._last_decision_reason}")
        print(
            f"[DemoPlayerAdapter] Selecionada choice {selected_index + 1}: {choice_text}"
        )

        return selected_index + 1, self._last_decision_reason


class HumanPlayerAdapter(PlayerStrategy):
    """
    Adapter para jogador humano via console.
    Implementa input loop com validação para capturar escolhas do usuário.
    """

    def __init__(self, debug: bool = False):
        self.console = Console()
        self._debug = debug
        self.renderer = RenderConsole(debug)

    def get_decision(
        self,
        available_choices: List[Dict[str, Any]],
        character_data: Dict[str, Any],
        history: List[Dict[str, Any]],
        current_page_data: Dict[str, Any],
        current_page_number: int,
    ) -> Tuple[int, str]:
        """
        Captura decisão do jogador humano via console input.

        Args:
            available_choices: Lista de choices disponíveis
            character_data: Dados estruturados do personagem do cockpit

        Returns:
            Índice (base 1) da escolha selecionada
        """
        # Exibir estado atual do jogo formatado

        # Loop de input com validação
        while True:
            try:
                self.renderer = RenderConsole()
                self.renderer.render_game_screen(
                    choices=available_choices,
                    character_data=character_data,
                    history=history,
                    current_page_data=current_page_data,
                    current_page_number=current_page_number,
                )
                user_input = input(
                    f"\nDigite sua escolha (1-{len(available_choices)}): "
                ).strip()

                choice_index = int(user_input)

                if 1 <= choice_index <= len(available_choices):
                    print(
                        f"\n✅ Escolha selecionada: [{choice_index}] {self._format_choice_for_display(available_choices[choice_index - 1])}"
                    )
                    return (
                        choice_index,
                        "Decisão tomada pelo jogador humano via console.",
                    )
                else:
                    print(
                        f"❌ Erro: Digite um número entre 1 e {len(available_choices)}"
                    )
            except ValueError:
                print("❌ Erro: Digite apenas números")
            except KeyboardInterrupt:
                print("\n\n🛑 Jogo interrompido pelo usuário")
                raise Exception("Jogo interrompido pelo usuário")
            except Exception as e:
                print(f"❌ Erro inesperado: {e}")

    def _format_detailed_cockpit(self, character_data: Dict[str, Any]) -> str:
        """
        Formata dados do personagem em formato detalhado para jogador humano.

        Args:
            character_data: Dados estruturados do personagem do cockpit

        Returns:
            String formatada de forma detalhada e legível
        """
        lines = []

        # Informações básicas
        char_info = character_data.get("character_info", {})
        lines.append("📋 INFORMAÇÕES DO PERSONAGEM")
        lines.append(f"├─ Nome: {char_info.get('name', 'Unknown')}")
        lines.append(f"├─ Ocupação: {char_info.get('occupation', 'N/A')}")
        lines.append(f"└─ Idade: {char_info.get('age', 0)}")
        lines.append("")

        # Status de saúde
        health = character_data.get("health_status", {})
        lines.append("❤️  STATUS DE SAÚDE")
        lines.append(
            f"└─ {health.get('icon', '❓')} {health.get('current_level', 'Unknown')} (Dano: {health.get('damage_taken', 0)})"
        )
        lines.append("")

        # Recursos
        resources = character_data.get("resources", {})
        luck = resources.get("luck", {})
        magic = resources.get("magic", {})
        lines.append("⚡ RECURSOS")
        lines.append(f"├─ Sorte: {luck.get('current', 0)}/{luck.get('starting', 0)}")
        lines.append(
            f"├─ Pontos de Magia: {magic.get('current', 0)}/{magic.get('starting', 0)}"
        )
        lines.append(f"└─ Movimento: {resources.get('movement', 8)}")
        lines.append("")

        # Características
        characteristics = character_data.get("characteristics", {})
        if characteristics:
            lines.append("📊 CARACTERÍSTICAS")
            for char_name in ["STR", "CON", "DEX", "INT", "POW"]:
                char_data = characteristics.get(char_name, {})
                if char_data:
                    lines.append(
                        f"├─ {char_name}: {char_data.get('full', 0)} (Metade: {char_data.get('half', 0)})"
                    )
            lines.append("")

        # Habilidades
        skills = character_data.get("skills", {})
        if skills:
            lines.append("🎯 HABILIDADES PRINCIPAIS")

            # Habilidades comuns
            common_skills = skills.get("common", {})
            for skill_name, skill_data in common_skills.items():
                lines.append(
                    f"├─ {skill_name}: {skill_data.get('full', 0)}% (Metade: {skill_data.get('half', 0)}%)"
                )

            # Habilidades de combate
            combat_skills = skills.get("combat", {})
            for skill_name, skill_data in combat_skills.items():
                lines.append(
                    f"├─ {skill_name}: {skill_data.get('full', 0)}% (Metade: {skill_data.get('half', 0)}%)"
                )
            lines.append("")

        # Inventário
        inventory = character_data.get("inventory", {})
        lines.append("🎒 INVENTÁRIO")
        if inventory.get("equipment"):
            lines.append("├─ Equipamentos: " + ", ".join(inventory["equipment"]))
        if inventory.get("weapons"):
            lines.append("├─ Armas: " + ", ".join(inventory["weapons"]))
        if not inventory.get("equipment") and not inventory.get("weapons"):
            lines.append("└─ Vazio")
        lines.append("")

        # Modificadores ativos
        modifiers = character_data.get("modifiers", [])
        if modifiers:
            lines.append("⚠️  MODIFICADORES ATIVOS")
            for mod in modifiers:
                skill = mod.get("skill", "Geral")
                mod_type = mod.get("type", "Desconhecido")
                duration = mod.get("duration", "Desconhecido")
                lines.append(f"├─ {skill}: {mod_type} ({duration})")
            lines.append("")

        return "\n".join(lines)

    def _format_choice_for_display(self, choice: Dict[str, Any]) -> str:
        """
        Formata uma choice para exibição amigável ao usuário.

        Args:
            choice: Choice a ser formatada

        Returns:
            String formatada para exibição
        """
        # Se tem texto, usar o texto
        if "text" in choice:
            return choice["text"]

        # Se é conditional_on, mostrar informação sobre condicional
        if "conditional_on" in choice:
            return f"Escolha condicional (baseada em {choice['conditional_on']})"

        # Se tem roll, mostrar informação sobre rolagem
        if "roll" in choice:
            return f"Rolar dados para {choice['roll']}"

        if "luck_roll" in choice:
            return "Rolar dados de sorte"

        if "opposed_roll" in choice:
            return f"Rolagem oposta: {choice['opposed_roll']}"

        # Fallback: mostrar goto ou string genérica
        if "goto" in choice:
            return f"Ir para página {choice['goto']}"

        return "Escolha disponível"


import openai


class LLMPlayerAdapter(PlayerStrategy):
    """
    Adapter para IA via API de LLM.
    Envia o estado do jogo para uma API de LLM e processa a resposta.
    """

    def __init__(self, debug: bool = False):
        """
        Inicializa o LLMPlayerAdapter.

        Args:
            api_key: Chave da API do LLM (pode ser None para usar variável de ambiente)
            model: Modelo a ser usado (default: gemini-pro)
        """
        self._debug = debug
        self.console = Console()

    def get_decision(
        self,
        available_choices: List[Dict[str, Any]],
        character_data: Dict[str, Any],
        history: List[Dict[str, Any]],
        current_page_data: Dict[str, Any],
        current_page_number: int,
    ) -> Tuple[int, str]:
        """
        Obtém decisão de uma API de LLM.

        Args:
            available_choices: Lista de choices disponíveis
            character_data: Dados estruturados do personagem do cockpit

        Returns:
            Índice (base 1) da escolha selecionada
        """

        try:
            # Loop de input com validação
            counter = 0
            while True:
                counter += 1
                if counter > 3:
                    raise Exception("Número máximo de tentativas excedido")

                prompt = self._build_llm_prompt(
                    choices=available_choices,
                    character_data=character_data,
                    history=history,
                    current_page_data=current_page_data,
                    current_page_number=current_page_number,
                )
                self.console.clear()
                if self._debug:
                    self.console.print(
                        f"[LLMPlayerAdapter] Enviando prompt para LLM (tamanho {len(prompt)} caracteres)"
                    )
                self.console.print(prompt)
                self.console.print("\n" + "-" * 50 + "\n")

                choice, reason = self._call_openrouter_api(prompt)

                user_input = choice

                # Verificar se é um número
                choice_index = int(user_input)
                return choice_index, reason
        except Exception as e:
            print(f"[LLMPlayerAdapter] Erro na API: {e}")
            raise e

    def _call_openrouter_api(self, prompt: str) -> Tuple[int, str]:
        api_key = os.getenv("OPENROUTER_API_KEY")

        if not api_key:
            raise Exception("OPENROUTER_API_KEY não configurada no ambiente.")
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        sys_prompt = """### PAPEL E OBJETIVO
Você é um agente de IA focado em tomar decisões estratégicas em um livro-jogo. Seu objetivo é analisar o cenário apresentado e escolher a melhor ação possível com base nos dados fornecidos, justificando sua escolha de forma lógica.

### DADOS DE ENTRADA
Você receberá as seguintes informações:
1.  **PAGINA ATUAL**: O texto descritivo da situação corrente.
2.  **ESTADO ATUAL DO PERSONAGEM**: Atributos, inventário e condição do personagem.
3.  **HISTÓRICO DE DECISÕES**: Ações tomadas anteriormente.
4.  **ESCOLHAS DISPONÍVEIS**: Uma lista numerada de ações que você pode tomar.

### TAREFA
1.  Analise rigorosamente todos os DADOS DE ENTRADA.
2.  Avalie as ESCOLHAS DISPONÍVEIS em relação ao ESTADO ATUAL DO PERSONAGEM e ao contexto da PAGINA ATUAL.
3.  Selecione o número da escolha que maximiza as chances de sucesso ou que seja mais coerente com os objetivos do personagem.
4.  Formule uma justificativa concisa e lógica para a escolha feita.

### FORMATO DE SAÍDA OBRIGATÓRIO
Sua resposta deve ser um **bloco de código Markdown** contendo um único objeto JSON válido. Não inclua nenhum outro texto fora do bloco de código. O objeto JSON deve ter duas chaves:
- `choice`: um número inteiro (integer).
- `reason`: uma string (string) com a justificativa.

**EXEMPLO DE SAÍDA VÁLIDA:**
```json
{
  "choice": 2,
  "reason": "A escolha de usar o item 'chave de ferro' é a mais lógica, pois a descrição da página menciona uma 'porta trancada' e a chave está no meu inventário. Tentar forçar a porta poderia causar dano ou alertar inimigos."
}
```
"""

        payload = {
            "model": "openai/gpt-5",  # ou outro modelo suportado
            "messages": [
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        }

        if self._debug:
            print(f"[LLMPlayerAdapter] Enviando payload para API: {payload}")

        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        choice, reason = self._process_llm_response(
            response.json()["choices"][0]["message"]["content"]
        )

        if self._debug:
            print(
                f"[LLMPlayerAdapter] Resposta da API: {response.status_code} - {response.text}"
            )
            print(
                f"[LLMPlayerAdapter] Resposta processada: choice={choice}, reason={reason}"
            )

        if choice is None or reason is None:
            raise Exception("Resposta do LLM inválida ou mal formatada.")

        return (choice, reason)

    def _process_llm_response(self, raw_response: str) -> Tuple[int, str]:
        """
        Processa a resposta bruta do LLM para extrair o número da escolha e a razão.

        A função espera encontrar um bloco de código Markdown com um JSON válido dentro.
        Ex:
        ```json
        {
        "choice": 1,
        "reason": "Esta é a melhor escolha por causa de X."
        }
        ```

        Args:
            raw_response: A string de resposta completa retornada pela API do LLM.

        Returns:
            Uma tupla contendo (choice_number, reason_text) se o processamento for bem-sucedido.
            Retorna None se o bloco JSON não for encontrado, for inválido ou se as chaves
            esperadas não estiverem presentes.
        """
        # 1. Extrair o conteúdo do bloco de código JSON usando expressão regular
        #    - re.DOTALL faz com que '.' também corresponda a quebras de linha.
        match = re.search(r"```json\s*(\{.*?\})\s*```", raw_response, re.DOTALL)

        if not match:
            print(
                f"ERRO DE PROCESSAMENTO: Bloco de código JSON não encontrado na resposta.\nResposta recebida: {raw_response}"
            )
            return None

        json_string = match.group(1)

        # 2. Tentar converter (parse) a string extraída em um dicionário Python
        try:
            data = json.loads(json_string)

            # 3. Validar a estrutura do dicionário
            if not isinstance(data, dict):
                print(
                    f"ERRO DE PROCESSAMENTO: JSON extraído não é um objeto (dicionário).\nJSON: {json_string}"
                )
                return None

            choice = data.get("choice")
            reason = data.get("reason")

            # Validar se as chaves existem e têm os tipos corretos
            if not isinstance(choice, int):
                print(
                    f"ERRO DE PROCESSAMENTO: Chave 'choice' ausente ou não é um inteiro.\nJSON: {json_string}"
                )
                raise Exception(f"Chave 'choice' inválida: {choice}")

            if not isinstance(reason, str) or not reason.strip():
                print(
                    f"ERRO DE PROCESSAMENTO: Chave 'reason' ausente, não é uma string ou está vazia.\nJSON: {json_string}"
                )
                raise Exception(f"Chave 'reason' inválida: {reason}")

            # 4. Retornar os dados validados
            return choice, reason

        except json.JSONDecodeError as ej:
            print(
                f"ERRO DE PROCESSAMENTO: Falha ao decodificar JSON.\nString extraída: {json_string}"
            )
            raise ej

    def _build_llm_prompt(
        self,
        choices: List[Dict[str, Any]],
        character_data: Dict[str, Any],
        history: List[Dict[str, Any]],
        current_page_data: Dict[str, Any],
        current_page_number: int,
    ) -> str:
        """
        Constrói prompt formatado para enviar ao LLM.

        Args:
            available_choices: Lista de choices disponíveis
            character_data: Dados estruturados do personagem do cockpit

        Returns:
            Prompt formatado para o LLM
        """
        # Formatar dados do personagem de forma estruturada para LLM
        structured_cockpit = self._format_structured_cockpit(character_data)

        # Construir prompt no formato YAML
        prompt_parts = [
            "#=============== INÍCIO DO COCKPIT DO JOGO ===============",
            "",
            "CONTEXTO_DA_PAGINA:",
            f"  ID_PAGINA: {current_page_number}",
            "  NARRATIVA: >",
            f"    {current_page_data.get('text', '')}",
            "  INSTRUCOES_MECANICAS: >",
            f"    {current_page_data.get('mechanics_instructions', 'Nenhuma')}",
            "",
            "ESTADO_DO_PERSONAGEM:",
            structured_cockpit,
            "",
            "HISTORICO_DE_DECISOES:",
        ]

        # Adicionar histórico de decisões
        if not history:
            prompt_parts.append("  - Vazio")
        else:
            for entry in history[-5:]:
                page_num = entry.get("page_number", "N/A")
                choice_index = int(entry.get("choice_index")) + 1
                choice_made = entry.get("choice_made", {}).get("text", "Follow-up action")
                reason = entry.get("reason", "N/A")
                prompt_parts.append(
                    f"  - Página: {page_num} > id_escolha: {choice_index} > {choice_made} > Motivo: {reason}"
                )

        # Adicionar escolhas disponíveis
        prompt_parts.append("")
        prompt_parts.append("ESCOLHAS_DISPONIVEIS:")

        for i, choice in enumerate(choices, 1):
            prompt_parts.append(f"  - id: {i}")
            prompt_parts.append(f"    texto: \"{choice.get('text', 'N/A')}\"")

            # Coletar consequências mecânicas
            mechanics = []
            for key in ["set-occupation", "roll", "goto", "effects"]:
                if key in choice:
                    mechanics.append(f"{key}: {choice[key]}")

            mechanics_str = "; ".join(mechanics) if mechanics else "Nenhuma"
            prompt_parts.append(f'    consequencias_mecanicas: "{mechanics_str}"')

        prompt_parts.append("")
        prompt_parts.append("#=============== FIM DO COCKPIT DO JOGO ===============")

        return "\n".join(prompt_parts)

    def _format_choice_for_display(self, choice: Dict[str, Any]) -> str:
        """
        Formata uma choice para exibição amigável ao usuário.

        Args:
            choice: Choice a ser formatada

        Returns:
            String formatada para exibição
        """
        # Se tem texto, usar o texto
        if "text" in choice:
            return choice["text"]

        # Se é conditional_on, mostrar informação sobre condicional
        if "conditional_on" in choice:
            return f"Escolha condicional (baseada em {choice['conditional_on']})"

        # Se tem roll, mostrar informação sobre rolagem
        if "roll" in choice:
            return f"Rolar dados para {choice['roll']}"

        if "luck_roll" in choice:
            return "Rolar dados de sorte"

        if "opposed_roll" in choice:
            return f"Rolagem oposta: {choice['opposed_roll']}"

        # Fallback: mostrar goto ou string genérica
        if "goto" in choice:
            return f"Ir para página {choice['goto']}"

        return "Escolha disponível"

    def _format_structured_cockpit(self, character_data: Dict[str, Any]) -> str:
        """
        Formata dados do personagem de forma estruturada e otimizada para LLM.

        Args:
            character_data: Dados estruturados do personagem do cockpit

        Returns:
            String formatada e estruturada para processamento por LLM
        """
        lines = []

        # Informações essenciais em formato JSON-like para fácil parsing
        char_info = character_data.get("character_info", {})
        health = character_data.get("health_status", {})
        resources = character_data.get("resources", {})

        lines.append("  PERFIL:")
        lines.append(f"    Nome: {char_info.get('name', 'Unknown')}")
        lines.append(f"    Ocupacao: {char_info.get('occupation', 'N/A')}")
        lines.append(f"    Status: {health.get('current_level', 'Unknown')}")
        lines.append(f"    Dano: {health.get('damage_taken', 0)}/4")
        lines.append(
            f"    Sorte: {resources.get('luck', {}).get('current', 0)}/{resources.get('luck', {}).get('starting', 0)}"
        )
        lines.append(
            f"    Magia: {resources.get('magic', {}).get('current', 0)}/{resources.get('magic', {}).get('starting', 0)}"
        )
        lines.append("")

        # Características importantes
        characteristics = character_data.get("characteristics", {})
        if characteristics:
            lines.append("  CARACTERISTICAS:")
            char_list = []
            for char_name in ["STR", "CON", "DEX", "INT", "POW"]:
                char_data = characteristics.get(char_name, {})
                if char_data:
                    char_list.append(f"{char_name}:{char_data.get('full', 0)}")
            lines.append(f"    {' '.join(char_list)}")
            lines.append("")

        # Habilidades mais relevantes
        skills = character_data.get("skills", {})
        if skills:
            lines.append("  PERICIAS:")
            # Formatar habilidades de forma mais legível
            skills_str = ", ".join(
                [f"{k}:{v.get('full', 0)}%" for k, v in skills.items()]
            )
            lines.append(f"    {skills_str}")
            lines.append("")

        # Inventário resumido
        inventory = character_data.get("inventory", {})
        items = []
        if inventory.get("equipment"):
            items.extend(inventory["equipment"])
        if inventory.get("weapons"):
            items.extend(inventory["weapons"])

        if items:
            lines.append(f"  INVENTARIO: {', '.join(items[:5])}")  # Primeiros 5 items
        else:
            lines.append("  INVENTARIO: Vazio")
        lines.append("")

        # Modificadores ativos (resumidos)
        modifiers = character_data.get("modifiers", [])
        if modifiers:
            mod_summary = [
                f"{mod.get('skill', 'Geral')}:{mod.get('type', 'Desconhecido')}"
                for mod in modifiers[:3]
            ]
            lines.append(f"  MODIFICADORES_ATIVOS: {' '.join(mod_summary)}")
        else:
            lines.append("  MODIFICADORES_ATIVOS: Nenhum")

        return "\n".join(lines)

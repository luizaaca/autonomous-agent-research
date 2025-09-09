"""
Player Adapters Module - Implementações concretas dos adaptadores de entrada

Este módulo contém as implementações concretas da interface PlayerInputAdapter
para diferentes modos de jogo: demonstração, humano e IA.
"""

from player_input_adapter import PlayerInputAdapter
from typing import Dict, List, Any, Optional
from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns
from rich.text import Text
from rich.console import Console
import os
import random


class RenderConsole:
    """
    Encapsula toda a lógica de renderização da UI do jogo para um jogador humano,
    utilizando a biblioteca Rich para criar um "cockpit" informativo no console.
    """
    def __init__(self):
        self.console = Console()

    def render_game_screen(self, choices: List[Dict[str, Any]], character_data: Dict[str, Any], history: List[Dict[str, Any]], current_page_data: Dict[str, Any], current_page_number: int) -> None:
        """
        Renderiza e exibe a tela de jogo completa, incluindo status, histórico,
        situação atual e escolhas.
        
        Este é o método principal que centraliza toda a UI do jogo.
        """
        # 1. Limpar console
        os.system("cls" if os.name == "nt" else "clear")
        self.console.clear()

        print(f"[RenderConsole] Renderizando tela do jogo - Página {current_page_number}\ncharacter_data keys: {list(character_data.keys())}, history entries: {len(history)}, choices: {len(choices)}")
        # 2. Construir painéis de status
        info_panel = self._build_info_table(character_data)
        resources_panel = self._build_resources_table(character_data)
        attributes_panel = self._build_attributes_table(character_data)
        skills_panel = self._build_skills_table(character_data)

        status_layout = Columns([
            info_panel,
            resources_panel,
            attributes_panel,
            skills_panel
        ], equal=True)

        # 3. Construir painel de histórico
        history_panel = self._build_history_panel(history)

        # 4. Construir painel da situação atual
        page_text = current_page_data.get('text', 'Página não encontrada.')
        page_panel = Panel(
            Text(page_text, style="white"),
            title="SITUAÇÃO ATUAL",
            border_style="cyan"
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
            expand=False
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
        table.add_row("SAÚDE:", f"{health['icon']} {health['current_level']} (Dano: {health['damage_taken']})")
        
        return Panel(table, title="📋 PERSONAGEM", border_style="green")
    
    def _build_resources_table(self, status_data: Dict[str, Any]) -> Panel:
        """Cria a tabela de recursos (Sorte, Magia)."""
        table = Table.grid(padding=(0, 1))
        table.add_column(style="bold yellow", justify="left")
        table.add_column(justify="left")
        
        resources = status_data["resources"]

        table.add_row("SORTE:", f"{resources['luck']['current']}/{resources['luck']['starting']}")
        table.add_row("MAGIA:", f"{resources['magic']['current']}/{resources['magic']['starting']}")

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
                table.add_row(f"{name}:", str(values.get('full', '')))
            
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
                page_num = entry.get('page_number', 0)
                choice_made = entry.get('choice_made', {})
                
                choice_text = choice_made.get('text', '')
                # Se não houver texto, formata a ação para dar contexto
                if not choice_text:
                    choice_text = self._format_choice_text(choice_made)
                else:
                    choice_text = f'"{choice_text}"'

                # Construir string de resultado detalhado
                result_parts = []
                if 'roll_result' in choice_made:
                    success_str = "SUCESSO" if choice_made.get('success') else "FALHA"
                    skill = choice_made.get('skill_used', 'N/A')
                    roll = choice_made.get('roll_result', 'N/A')
                    target = choice_made.get('target_value', 'N/A')
                    result_parts.append(f"Rolagem de {skill}: {roll} vs {target} -> {success_str}")

                if 'effects_applied' in choice_made and choice_made['effects_applied']:
                    effects_str_parts = []
                    for eff in choice_made['effects_applied']:
                        action = eff.get('action', 'unknown')
                        param = eff.get('amount') or eff.get('skill') or ''
                        effects_str_parts.append(f"{action}({param})")
                    result_parts.append(f"Efeitos: {', '.join(effects_str_parts)}")

                if 'goto_executed' in choice_made:
                    result_parts.append(f"goto: {choice_made['goto_executed']}")
                
                result_info = ""
                if result_parts:
                    result_info = f" -> Resultado: {'; '.join(result_parts)}"

                history_line = f"Página {page_num}: Escolheu {choice_text}{result_info}\n"
                content.append(history_line, style="dim white")
        
        return Panel(content, title="📜 HISTÓRICO DE DECISÕES", border_style="yellow")
    
    def _build_choices_panel(self, choices: List[Dict[str, Any]]) -> Panel:
        """
        Cria o painel que exibe apenas as escolhas atualmente disponíveis para o jogador.
        A lógica de histórico foi movida para _build_history_panel.
        """
        content = Text()
        
        if not choices:
            content.append("🏁 FIM DO JOGO - Nenhuma escolha disponível.", style="bold red")
        else:
            content.append("ESCOLHAS ATUAIS:\n", style="bold cyan")
            for i, choice in enumerate(choices, 1):
                # Formata a escolha de forma detalhada
                formatted_text = self._format_choice_text(choice)
                
                # Adicionar prefixo [SYSTEM] ou [ERROR] se for mensagem de sistema
                if formatted_text.startswith('[SYSTEM]') or formatted_text.startswith('[ERROR]'):
                    content.append(f"  {formatted_text}\n", style="bold red")
                else:
                    content.append(f"[{i}] - {formatted_text}\n", style="white")
        
        return Panel(content, title="🎯 ESCOLHAS DISPONÍVEIS", border_style="magenta")

    def _format_choice_text(self, choice: Dict[str, Any]) -> str:
        """
        Formata o dicionário de uma escolha em um texto descritivo e legível.
        """
        # Se a escolha tiver um texto explícito, use-o como base
        text = choice.get('text', '')

        details = []
        # Adiciona detalhes sobre as ações da escolha
        if 'goto' in choice:
            details.append(f"goto: {choice['goto']}")
        if 'set-occupation' in choice:
            details.append(f"set-occupation: '{choice['set-occupation']}'")
        if 'roll' in choice:
            details.append(f"roll: {choice['roll']}")
        if 'luck_roll' in choice:
            details.append("roll: luck")
        if 'opposed_roll' in choice:
            details.append(f"opposed_roll: {choice['opposed_roll']}")
        if 'effects' in choice:
            effects_desc = []
            for effect in choice['effects']:
                action = effect.get('action', 'unknown_action')
                if action == 'take_damage':
                    effects_desc.append(f"damage: {effect.get('amount', '?')}")
                elif action == 'gain_skill':
                    effects_desc.append(f"gain_skill: {effect.get('skill', '?')}")
                elif action == 'spend_magic':
                    effects_desc.append(f"spend_magic: {effect.get('amount', '?')}")
                else:
                    effects_desc.append(action)
            details.append(f"effects: {', '.join(effects_desc)}")

        # Monta a string final
        if details:
            details_str = f"({', '.join(details)})"
            return f"{text} {details_str}" if text else details_str
        
        return text or "Ação sem descrição"


class DemoPlayerAdapter(PlayerInputAdapter):
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
        self.debug = debug
        self.renderer = RenderConsole()
        self._last_decision_reason = ""
    
    def get_decision(self, available_choices: List[Dict[str, Any]], character_data: Dict[str, Any], history: List[Dict[str, Any]], current_page_data: Dict[str, Any], current_page_number: int ) -> int:
        """
        Toma decisão automática baseada na lógica internalizada do DefaultDecisionController.
        
        Args:
            available_choices: Lista de choices disponíveis
            character_data: Dados estruturados do personagem 
            history: Histórico de decisões anteriores 

        Returns:
            Índice (base 1) da escolha selecionada
        """
        if self.debug:
            print(f"[DemoPlayerAdapter] Processando {len(available_choices)} choices")

        self.renderer.render_game_screen(
            choices=available_choices,
            character_data=character_data,
            history=history,
            current_page_data=current_page_data,
            current_page_number=current_page_number
        )

        # Validação básica
        if not available_choices:
            raise Exception("Lista de choices vazia - não é possível tomar decisão")
        
        if len(available_choices) > 1:
            selected_index = random.choice(range(len(available_choices)))
            self._last_decision_reason = f"Seleção aleatória entre {len(available_choices)} opções básicas."
        else:
            selected_index = 0
            self._last_decision_reason = "Única escolha básica disponível."

        choice_text = available_choices[selected_index].get('text', str(available_choices[selected_index])[:50])
        print(f"[DemoPlayerAdapter] Razão: {self._last_decision_reason}")
        print(f"[DemoPlayerAdapter] Selecionada choice {selected_index + 1}: {choice_text}")
        
        return selected_index + 1


class HumanPlayerAdapter(PlayerInputAdapter):
    """
    Adapter para jogador humano via console.
    Implementa input loop com validação para capturar escolhas do usuário.
    """

    def get_decision(self, available_choices: List[Dict[str, Any]], character_data: Dict[str, Any], history: List[Dict[str, Any]], current_page_data: Dict[str, Any], current_page_number: int) -> int:
        """
        Captura decisão do jogador humano via console input.
        
        Args:
            available_choices: Lista de choices disponíveis
            character_data: Dados estruturados do personagem do cockpit
            
        Returns:
            Índice (base 1) da escolha selecionada
        """
        # Exibir estado atual do jogo formatado
        formatted_cockpit = self._format_detailed_cockpit(character_data)
        
        print("\n" + "="*80)
        print("📱 ESTADO ATUAL DO JOGO:")
        print("="*80)
        print(formatted_cockpit)
        print("="*80)
        
        # Exibir choices disponíveis
        print("\n🎯 ESCOLHAS DISPONÍVEIS:")
        print("-"*40)
        
        for i, choice in enumerate(available_choices, 1):
            choice_text = self._format_choice_for_display(choice)
            print(f"[{i}] {choice_text}")
        
        print("-"*40)
        
        # Loop de input com validação
        while True:
            try:
                user_input = input(f"\nDigite sua escolha (1-{len(available_choices)}): ").strip()
                
                # Verificar se é um número
                choice_index = int(user_input)
                
                # Verificar se está no range válido
                if 1 <= choice_index <= len(available_choices):
                    print(f"\n✅ Escolha selecionada: [{choice_index}] {self._format_choice_for_display(available_choices[choice_index - 1])}")
                    return choice_index
                else:
                    print(f"❌ Erro: Digite um número entre 1 e {len(available_choices)}")
                    
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
        char_info = character_data.get('character_info', {})
        lines.append("📋 INFORMAÇÕES DO PERSONAGEM")
        lines.append(f"├─ Nome: {char_info.get('name', 'Unknown')}")
        lines.append(f"├─ Ocupação: {char_info.get('occupation', 'N/A')}")
        lines.append(f"└─ Idade: {char_info.get('age', 0)}")
        lines.append("")
        
        # Status de saúde
        health = character_data.get('health_status', {})
        lines.append("❤️  STATUS DE SAÚDE")
        lines.append(f"└─ {health.get('icon', '❓')} {health.get('current_level', 'Unknown')} (Dano: {health.get('damage_taken', 0)})")
        lines.append("")
        
        # Recursos
        resources = character_data.get('resources', {})
        luck = resources.get('luck', {})
        magic = resources.get('magic', {})
        lines.append("⚡ RECURSOS")
        lines.append(f"├─ Sorte: {luck.get('current', 0)}/{luck.get('starting', 0)}")
        lines.append(f"├─ Pontos de Magia: {magic.get('current', 0)}/{magic.get('starting', 0)}")
        lines.append(f"└─ Movimento: {resources.get('movement', 8)}")
        lines.append("")
        
        # Características
        characteristics = character_data.get('characteristics', {})
        if characteristics:
            lines.append("📊 CARACTERÍSTICAS")
            for char_name in ["STR", "CON", "DEX", "INT", "POW"]:
                char_data = characteristics.get(char_name, {})
                if char_data:
                    lines.append(f"├─ {char_name}: {char_data.get('full', 0)} (Metade: {char_data.get('half', 0)})")
            lines.append("")
        
        # Habilidades
        skills = character_data.get('skills', {})
        if skills:
            lines.append("🎯 HABILIDADES PRINCIPAIS")
            
            # Habilidades comuns
            common_skills = skills.get('common', {})
            for skill_name, skill_data in common_skills.items():
                lines.append(f"├─ {skill_name}: {skill_data.get('full', 0)}% (Metade: {skill_data.get('half', 0)}%)")
            
            # Habilidades de combate
            combat_skills = skills.get('combat', {})
            for skill_name, skill_data in combat_skills.items():
                lines.append(f"├─ {skill_name}: {skill_data.get('full', 0)}% (Metade: {skill_data.get('half', 0)}%)")
            lines.append("")
        
        # Inventário
        inventory = character_data.get('inventory', {})
        lines.append("🎒 INVENTÁRIO")
        if inventory.get('equipment'):
            lines.append("├─ Equipamentos: " + ", ".join(inventory['equipment']))
        if inventory.get('weapons'):
            lines.append("├─ Armas: " + ", ".join(inventory['weapons']))
        if not inventory.get('equipment') and not inventory.get('weapons'):
            lines.append("└─ Vazio")
        lines.append("")
        
        # Modificadores ativos
        modifiers = character_data.get('modifiers', [])
        if modifiers:
            lines.append("⚠️  MODIFICADORES ATIVOS")
            for mod in modifiers:
                skill = mod.get('skill', 'Geral')
                mod_type = mod.get('type', 'Desconhecido')
                duration = mod.get('duration', 'Desconhecido')
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
        if 'text' in choice:
            return choice['text']
        
        # Se é conditional_on, mostrar informação sobre condicional
        if 'conditional_on' in choice:
            return f"Escolha condicional (baseada em {choice['conditional_on']})"
        
        # Se tem roll, mostrar informação sobre rolagem
        if 'roll' in choice:
            return f"Rolar dados para {choice['roll']}"
        
        if 'luck_roll' in choice:
            return "Rolar dados de sorte"
        
        if 'opposed_roll' in choice:
            return f"Rolagem oposta: {choice['opposed_roll']}"
        
        # Fallback: mostrar goto ou string genérica
        if 'goto' in choice:
            return f"Ir para página {choice['goto']}"
        
        return "Escolha disponível"


class LLMPlayerAdapter(PlayerInputAdapter):
    """
    Adapter para IA via API de LLM.
    Envia o estado do jogo para uma API de LLM e processa a resposta.
    """
    
    def __init__(self, api_key: str = None, model: str = "gemini-pro"):
        """
        Inicializa o LLMPlayerAdapter.
        
        Args:
            api_key: Chave da API do LLM (pode ser None para usar variável de ambiente)
            model: Modelo a ser usado (default: gemini-pro)
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model
        
        if not self.api_key:
            print("⚠️  Aviso: API key não fornecida. LLMPlayerAdapter usará fallback para DemoPlayerAdapter")
            self._fallback_adapter = DemoPlayerAdapter(debug=True)

    def get_decision(self, available_choices: List[Dict[str, Any]], character_data: Dict[str, Any], history: List[Dict[str, Any]], current_page_data: Dict[str, Any], current_page_number: int) -> int:
        """
        Obtém decisão de uma API de LLM.
        
        Args:
            available_choices: Lista de choices disponíveis
            character_data: Dados estruturados do personagem do cockpit
            
        Returns:
            Índice (base 1) da escolha selecionada
        """
        # Se não há API key, usar fallback
        if not self.api_key:
            print("[LLMPlayerAdapter] Usando fallback DemoPlayerAdapter")
            return self._fallback_adapter.get_decision(available_choices, character_data)
        
        try:
            # Construir prompt para LLM
            prompt = self._build_llm_prompt(available_choices, character_data)
            
            # TODO: Implementar chamada real para API do LLM
            # Por enquanto, usar lógica demo como placeholder
            print("[LLMPlayerAdapter] API integration não implementada ainda - usando lógica demo")
            
            # Placeholder: selecionar primeira choice válida
            for i, choice in enumerate(available_choices):
                if 'goto' in choice or any(key in choice for key in ['roll', 'luck_roll', 'opposed_roll']):
                    return i + 1
            
            # Fallback final
            return 1
            
        except Exception as e:
            print(f"[LLMPlayerAdapter] Erro na API: {e} - usando fallback")
            return self._fallback_adapter.get_decision(available_choices, character_data)
    
    def _build_llm_prompt(self, available_choices: List[Dict[str, Any]], character_data: Dict[str, Any]) -> str:
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
        
        prompt_parts = [
            "Você é um agente inteligente jogando um RPG baseado em texto.",
            "Analise o estado atual do jogo e escolha a melhor ação.",
            "Você deve avaliar as escolhas, considerar suas habilidades, saúde, inventário e histórico.",
            "",
            "ESTADO ATUAL DO PERSONAGEM:",
            structured_cockpit,
            "",
            "ESCOLHAS DISPONÍVEIS:",
        ]
        
        for i, choice in enumerate(available_choices, 1):
            choice_desc = choice.get('text', f"Escolha {i}")
            prompt_parts.append(f"{i}. {choice_desc}")
        
        prompt_parts.extend([
            "",
            f"Responda APENAS com o número da escolha (1-{len(available_choices)}).",
            "Não inclua explicações ou texto adicional.",
        ])
        
        return "\n".join(prompt_parts)
    
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
        char_info = character_data.get('character_info', {})
        health = character_data.get('health_status', {})
        resources = character_data.get('resources', {})
        
        lines.append("CHARACTER_PROFILE:")
        lines.append(f"  Name: {char_info.get('name', 'Unknown')}")
        lines.append(f"  Occupation: {char_info.get('occupation', 'N/A')}")
        lines.append(f"  Health: {health.get('current_level', 'Unknown')} (Damage: {health.get('damage_taken', 0)})")
        lines.append(f"  Luck: {resources.get('luck', {}).get('current', 0)}/{resources.get('luck', {}).get('starting', 0)}")
        lines.append(f"  Magic: {resources.get('magic', {}).get('current', 0)}/{resources.get('magic', {}).get('starting', 0)}")
        lines.append("")
        
        # Características importantes
        characteristics = character_data.get('characteristics', {})
        if characteristics:
            lines.append("CHARACTERISTICS:")
            char_list = []
            for char_name in ["STR", "CON", "DEX", "INT", "POW"]:
                char_data = characteristics.get(char_name, {})
                if char_data:
                    char_list.append(f"{char_name}:{char_data.get('full', 0)}")
            lines.append(f"  {' '.join(char_list)}")
            lines.append("")
        
        # Habilidades mais relevantes
        skills = character_data.get('skills', {})
        if skills:
            lines.append("KEY_SKILLS:")
            skill_list = []
            
            # Pegar as 3 habilidades mais altas de cada categoria
            common_skills = skills.get('common', {})
            sorted_common = sorted(common_skills.items(), key=lambda x: x[1].get('full', 0), reverse=True)[:3]
            for skill_name, skill_data in sorted_common:
                skill_list.append(f"{skill_name}:{skill_data.get('full', 0)}%")
            
            combat_skills = skills.get('combat', {})
            for skill_name, skill_data in combat_skills.items():
                skill_list.append(f"{skill_name}:{skill_data.get('full', 0)}%")
            
            lines.append(f"  {' '.join(skill_list)}")
            lines.append("")
        
        # Inventário resumido
        inventory = character_data.get('inventory', {})
        items = []
        if inventory.get('equipment'):
            items.extend(inventory['equipment'])
        if inventory.get('weapons'):
            items.extend(inventory['weapons'])
        
        if items:
            lines.append(f"INVENTORY: {', '.join(items[:5])}")  # Primeiros 5 items
        else:
            lines.append("INVENTORY: Empty")
        lines.append("")
        
        # Modificadores ativos (resumidos)
        modifiers = character_data.get('modifiers', [])
        if modifiers:
            mod_summary = [f"{mod.get('skill', 'General')}:{mod.get('type', 'Unknown')}" for mod in modifiers[:3]]
            lines.append(f"ACTIVE_MODIFIERS: {' '.join(mod_summary)}")
        else:
            lines.append("ACTIVE_MODIFIERS: None")
        
        return "\n".join(lines)

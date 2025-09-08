"""
Page Module - Cockpit/Dashboard para Agente Autônomo

Este módulo implementa a classe GamePage que serve como interface cockpit/dashboard
para o agente autônomo, fornecendo uma visão completa do estado do jogo formatada
como prompt para LLMs.

A estrutura é dividida em:
- Header: Instruções fixas do jogo
- Body: Estado atual do personagem (ficha, status, inventário, histórico)
"""

from typing import Dict, List, Any, Optional
import json
from character import Character
from rich.console import Console
from rich.panel import Panel
from rich.table import Table, Column
from rich.text import Text
from rich.columns import Columns


class Cockpit:
    """
    Representa a tela de jogo, renderizando todas as informações de forma unificada.
    Usa a biblioteca rich para criar uma interface de "tela de video-game".
    
    Esta classe encapsula toda a informação necessária para exibir o estado do jogo
    de forma compacta e organizada, separando a apresentação da lógica de decisão.
    """
    
    def __init__(self, character: Character, pages_data: Dict[int, Dict]):
        """
        Inicializa o Cockpit.
        
        Args:
            character: Instância da classe Character
            pages_data: Dicionário com todas as páginas do jogo
        """
        self.character = character
        self.pages_data = pages_data
        self.current_page_number = None
        self.current_page_data = None
        self.console = Console()
        self._cached_status_data = None
        
    def set_current_page(self, page_number: int):
        """Define a página atual do jogo."""
        self.current_page_number = page_number
        
        # Compatibilidade com objetos GameData que têm método .get()
        if hasattr(self.pages_data, 'get'):
            self.current_page_data = self.pages_data.get(page_number, {})
        else:
            # Fallback para dicionários diretos
            self.current_page_data = self.pages_data.get(page_number, {})
    
    def force_refresh(self):
        """
        Força a atualização dos dados do personagem na próxima renderização.
        Este método deve ser chamado sempre que o estado do personagem for alterado
        externamente (ex: após aplicar efeitos como 'set-occupation').
        """
        # Invalidar os dados de status para forçar a coleta na próxima renderização
        self._cached_status_data = None
    
    def render_game_screen(self) -> None:
        """
        Renderiza e exibe a tela de jogo completa, incluindo status, histórico,
        situação atual e escolhas.
        
        Este é o método principal que centraliza toda a UI do jogo.
        """
        # 1. Limpar console
        self.console.clear()

        # 2. Obter dados do personagem
        status_data = self._get_character_status_data()
        
        # 3. Construir painéis de status
        info_panel = self._build_info_table(status_data)
        resources_panel = self._build_resources_table(status_data)
        attributes_panel = self._build_attributes_table(status_data)
        skills_panel = self._build_skills_table(status_data)
        
        status_layout = Columns([
            info_panel,
            resources_panel,
            attributes_panel,
            skills_panel
        ], equal=True)

        # 4. Construir painel de histórico
        history_panel = self._build_history_panel()

        # 5. Construir painel da situação atual
        page_text = self.current_page_data.get('text', 'Página não encontrada.')
        page_panel = Panel(
            Text(page_text, style="white"),
            title="SITUAÇÃO ATUAL",
            border_style="cyan"
        )
        
        # 6. Construir painel de escolhas
        choices = self.current_page_data.get('choices', [])
        choices_panel = self._build_choices_panel(choices)
        
        # 7. Montar layout principal em um grid
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
            title=f"🎮 COCKPIT - PÁGINA {self.current_page_number}",
            border_style="bold blue",
            expand=False
        )
        
        # 8. Renderizar na tela
        self.console.print(main_panel)
        
        # DEBUG: Exibir atributos do objeto Character abaixo do cockpit
        debug_data = {
            "name": self.character.name,
            "occupation": self.character.occupation,
            "age": self.character.age,
            "health": self.character.get_health_status(),
            "luck": self.character.get_luck(),
            "magic": self.character.get_magic_points(),
            "characteristics": {k: self.character.get_characteristic(k) for k in ["STR", "CON", "DEX", "INT", "POW"]},
            "skills": self.character.get_all_skills(),
            "inventory": self.character.get_inventory(),
            "modifiers": self.character.get_modifiers(),
            "history": self.character.get_history()[-3:]  # últimas 3 decisões
        }
        debug_json = json.dumps(debug_data, indent=2, ensure_ascii=False)
        self.console.print(Panel(Text(debug_json, style="dim"), title="DEBUG: Character State", border_style="red"))
    
    def _get_character_status_data(self) -> Dict[str, Any]:
        """
        Coleta e estrutura os dados do personagem para renderização.
        Utiliza um cache para evitar recálculos desnecessários, a menos que force_refresh seja chamado.
        """
        # Se os dados já estiverem em cache, retorná-los
        if self._cached_status_data is not None:
            return self._cached_status_data
            
        # Status de saúde
        health_status = self.character.get_health_status()
        current_health = health_status["current_level"]
        damage_taken = health_status["damage_taken"]
        
        health_icons = {
            "Healthy": "💚", "Hurt": "💛", "Bloodied": "🧡",
            "Down": "❤️", "Impaired": "💜"
        }
        
        # Recursos
        luck_data = self.character.get_luck()
        magic_data = self.character.get_magic_points()
        
        # Características
        characteristics = {}
        char_names = ["STR", "CON", "DEX", "INT", "POW"]
        for char_name in char_names:
            try:
                char_data = self.character.get_characteristic(char_name)
                characteristics[char_name] = char_data
            except KeyError:
                continue
        
        # Habilidades - NOTA: Idealmente, a classe Character deveria fornecer um método get_all_skills()
        skills = {
            "common": {},
            "combat": {},
            "expert": {}
        }
        all_character_skills = self.character.get_all_skills()
        for category, skill_list in all_character_skills.items():
            if category in skills:
                skills[category] = skill_list

        self._cached_status_data = {
            "info": {
                "name": self.character.name,
                "occupation": self.character.occupation or "N/A",
                "age": self.character.age
            },
            "health": {
                "icon": health_icons.get(current_health, '❓'),
                "level": current_health,
                "damage": damage_taken,
            },
            "resources": {
                "luck": f"{luck_data['current']}/{luck_data['starting']}",
                "magic": f"{magic_data['current']}/{magic_data['starting']}",
            },
            "characteristics": characteristics,
            "skills": skills
        }
        
        return self._cached_status_data
    
    def _build_info_table(self, status_data: Dict[str, Any]) -> Panel:
        """Cria a tabela de informações básicas e saúde."""
        table = Table.grid(padding=(0, 1))
        table.add_column(style="bold cyan", justify="left")
        table.add_column(justify="left")
        
        info = status_data["info"]
        health = status_data["health"]
        
        table.add_row("NOME:", info["name"])
        table.add_row("OCUPAÇÃO:", info["occupation"])
        table.add_row("IDADE:", str(info["age"]))
        table.add_row("SAÚDE:", f"{health['icon']} {health['level']} (Dano: {health['damage']})")
        
        return Panel(table, title="📋 PERSONAGEM", border_style="green")
    
    def _build_resources_table(self, status_data: Dict[str, Any]) -> Panel:
        """Cria a tabela de recursos (Sorte, Magia)."""
        table = Table.grid(padding=(0, 1))
        table.add_column(style="bold yellow", justify="left")
        table.add_column(justify="left")
        
        resources = status_data["resources"]
        
        table.add_row("SORTE:", resources["luck"])
        table.add_row("MAGIA:", resources["magic"])
        
        return Panel(table, title="⚡ RECURSOS", border_style="yellow")

    def _build_attributes_table(self, status_data: Dict[str, Any]) -> Panel:
        """Cria a tabela de atributos (características)."""
        table = Table.grid(padding=(0, 1))
        table.add_column(style="bold red", justify="left")
        table.add_column(justify="left")
        
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
        table.add_column(justify="left")
        
        skills = status_data.get("skills", {})
        all_skills = {
            **skills.get("common", {}),
            **skills.get("combat", {}),
            **skills.get("expert", {})
        }
        
        if not all_skills:
            table.add_row("Nenhuma", "")
        else:
            for name, values in sorted(all_skills.items()):
                table.add_row(f"{name}:", f"{values.get('full', 0)}%")
            
        return Panel(table, title="🎯 HABILIDADES", border_style="blue")

    def _build_history_panel(self) -> Optional[Panel]:
        """
        Cria um painel com o histórico das últimas decisões do jogador.
        Retorna None se não houver histórico.
        """
        history = self.character.get_history()
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
    
    def _smart_truncate_text(self, text: str, max_chars: int = 50) -> str:
        """
        Trunca texto preservando palavras completas nos últimos N caracteres.
        
        Args:
            text: Texto a ser truncado
            max_chars: Número máximo de caracteres (padrão: 50)
            
        Returns:
            Texto truncado de forma inteligente com "..." no início
        """
        if len(text) <= max_chars:
            return text
        
        # Pegar os últimos max_chars caracteres
        truncated = text[-max_chars:]
        
        # Encontrar o primeiro espaço para não cortar palavras
        first_space = truncated.find(' ')
        if first_space > 0 and first_space < len(truncated) - 1:
            truncated = truncated[first_space + 1:]
        
        # Adicionar indicador de truncamento
        return f"...{truncated}"
        
    def render_header(self) -> str:
        """
        Renderiza o cabeçalho com instruções fixas do jogo.
        
        Returns:
            String formatada com as instruções para o LLM
        """
        header = """
═══════════════════════════════════════════════════════════════════════════════
🎯 AGENT COCKPIT - AUTONOMOUS GAME NAVIGATION SYSTEM
═══════════════════════════════════════════════════════════════════════════════

ROLE: You are an autonomous agent playing a text-based RPG adventure.
OBJECTIVE: Navigate through the story making optimal decisions to achieve your goals.
SYSTEM: OODA Loop (Observe, Orient, Decide, Act)

INSTRUCTIONS:
• Read the CURRENT SITUATION carefully
• Review your CHARACTER STATUS and capabilities  
• Analyze available CHOICES based on your skills and resources
• Consider the DECISION HISTORY to avoid loops
• Choose the action that best advances your objectives
• Explain your reasoning briefly before stating your choice

═══════════════════════════════════════════════════════════════════════════════
"""
        return header.strip()
    
    def render_character_status(self) -> Dict[str, Any]:
        """
        Retorna o status atual do personagem como objeto estruturado.
        
        Returns:
            Dicionário com todas as informações do personagem organizadas por categoria
        """
        # Status de saúde usando o novo sistema
        health_status = self.character.get_health_status()
        current_health = health_status["current_level"]
        damage_taken = health_status["damage_taken"]
        
        health_icons = {
            "Healthy": "💚",
            "Hurt": "💛", 
            "Bloodied": "🧡",
            "Down": "❤️",
            "Impaired": "💜"
        }
        
        # Recursos usando métodos da Character
        luck_data = self.character.get_luck()
        magic_data = self.character.get_magic_points()
        
        # Características principais usando métodos da Character
        characteristics = {}
        char_names = ["STR", "CON", "DEX", "INT", "POW"]
        for char_name in char_names:
            try:
                char_data = self.character.get_characteristic(char_name)
                characteristics[char_name] = {
                    "full": char_data['full'],
                    "half": char_data['half']
                }
            except KeyError:
                continue
        
        # Habilidades organizadas por categoria
        skills = {
            "common": {},
            "combat": {}
        }
        
        # Habilidades comuns
        common_skill_names = ["Athletics", "Drive", "Navigate", "Observation", "Read Person", "Research"]
        for skill_name in common_skill_names:
            try:
                skill_data = self.character.get_skill(skill_name, "common")
                skills["common"][skill_name] = {
                    "full": skill_data['full'],
                    "half": skill_data['half']
                }
            except KeyError:
                continue
        
        # Habilidades de combate
        combat_skill_names = ["Fighting", "Firearms"]
        for skill_name in combat_skill_names:
            try:
                skill_data = self.character.get_skill(skill_name, "combat")
                skills["combat"][skill_name] = {
                    "full": skill_data['full'],
                    "half": skill_data['half']
                }
            except KeyError:
                continue
        
        # Inventário usando métodos da Character
        inventory = self.character.get_inventory()
        
        # Modificadores ativos usando métodos da Character
        modifiers = self.character.get_modifiers()
        
        # Retornar objeto estruturado
        return {
            "character_info": {
                "name": self.character.name,
                "occupation": self.character.occupation,
                "age": self.character.age
            },
            "health_status": {
                "current_level": current_health,
                "damage_taken": damage_taken,
                "icon": health_icons.get(current_health, '❓')
            },
            "resources": {
                "luck": {
                    "current": luck_data['current'],
                    "starting": luck_data['starting']
                },
                "magic": {
                    "current": magic_data['current'],
                    "starting": magic_data['starting']
                },
                "movement": 8
            },
            "characteristics": characteristics,
            "skills": skills,
            "inventory": {
                "equipment": inventory.get('equipment', []),
                "weapons": inventory.get('weapons', [])
            },
            "modifiers": modifiers if modifiers else []
        }
    
    def render_current_situation(self) -> str:
        """
        Renderiza a situação atual (página atual e opções disponíveis).
        
        Returns:
            String formatada com a situação atual do jogo
        """
        if not self.current_page_data:
            return "📍 CURRENT SITUATION\n└─ No current page data available"
            
        situation = f"""
📍 CURRENT SITUATION - PAGE {self.current_page_number}
{'-' * 70}
{self.current_page_data.get('text', 'No description available')}
{'-' * 70}
"""
        
        # Renderizar escolhas disponíveis
        choices = self.current_page_data.get('choices', [])
        if not choices:
            situation += "\n🏁 END STATE - No more choices available\n"
            return situation
            
        situation += "\n🎮 AVAILABLE CHOICES:\n"
        
        for i, choice in enumerate(choices, 1):
            if isinstance(choice, dict):
                # Exibir o objeto choice completo formatado
                situation += f"\n[{i}] {choice}\n"
                    
        return situation.strip()
    
    def render_history(self, max_entries: int = 3) -> str:
        """
        Renderiza o histórico de decisões em formato JSON estruturado
    
        Args:
            max_entries: Número máximo de entradas a exibir (padrão: 3)
            
        Returns:
            String JSON formatada com o histórico das decisões
        """
        history = self.character.get_history()
        
        if not history:
            return json.dumps({
                "history_summary": "Nenhuma decisão registrada ainda",
                "total_decisions": 0,
                "entries": []
            }, indent=2, ensure_ascii=False)
        
        # Limitar o número de entradas
        recent_history = history[-max_entries:] if len(history) > max_entries else history
        
        formatted_entries = []
        
        for i, entry in enumerate(recent_history, 1):
            # APENAS formato moderno (dicionário) - SEM suporte legado
            if not isinstance(entry, dict):
                print(f"AVISO: Entrada de histórico inválida ignorada: {type(entry)}")
                continue
                
            # Formato moderno: dicionário completo
            page_number = entry.get('page_number', 0)
            page_text = entry.get('page_text', '')
            choice_made = entry.get('choice_made', {})

            # Truncamento inteligente dos últimos 50 caracteres preservando palavras
            truncated_text = self._smart_truncate_text(page_text, 50)

            # Construir resultado da ação
            action_result = {}
            
            # Adicionar outcome executado
            if 'executed_outcome' in choice_made:
                action_result['executed_outcome'] = choice_made['executed_outcome']
            
            # Adicionar resultados de roll
            if 'roll_result' in choice_made:
                action_result['roll_result'] = choice_made['roll_result']
                action_result['skill_used'] = choice_made.get('skill_used', '')
                action_result['target_value'] = choice_made.get('target_value', 0)
                action_result['success'] = choice_made.get('success', False)
            
            # Adicionar resultados de opposite roll
            if 'opposite_roll' in choice_made:
                action_result['opposite_roll'] = choice_made['opposite_roll']
            
            # Adicionar efeitos aplicados
            if 'effects_applied' in choice_made and choice_made['effects_applied']:
                action_result['effects_applied'] = choice_made['effects_applied']
            
            # Adicionar goto executado
            if 'goto_executed' in choice_made:
                action_result['goto_executed'] = choice_made['goto_executed']
            
            # Limpar choice_made dos campos de resultado para separar decisão de execução
            clean_choice = {k: v for k, v in choice_made.items() 
                           if k not in ['executed_outcome', 'roll_result', 'skill_used', 
                                       'target_value', 'success', 'opposite_roll', 
                                       'effects_applied', 'goto_executed']}
            
            # Construir entrada formatada (SIMPLIFICADA - sem original_choices e choice_index)
            formatted_entry = {
                "step": i,
                "page_number": page_number,
                "page_text": truncated_text,
                "choice_made": clean_choice if clean_choice else {"empty_choice": True}
            }
            
            # Adicionar resultado da ação apenas se não estiver vazio
            if action_result:
                formatted_entry["action_result"] = action_result
            
            formatted_entries.append(formatted_entry)
        
        # Construir objeto final
        history_json = {
            "history_summary": f"Últimas {len(formatted_entries)} decisões do agente",
            "total_decisions": len(history),
            "entries": formatted_entries
        }
        
        return json.dumps(history_json, indent=2, ensure_ascii=False)
    
    def _format_character_status_for_prompt(self) -> str:
        """
        Formata o status do personagem como string para uso em prompts.
        Mantém compatibilidade com generate_prompt().
        
        Returns:
            String formatada com o status do personagem
        """
        status_data = self.render_character_status()
        
        # Informações básicas
        char_info = status_data["character_info"]
        info_section = f"""
📋 CHARACTER INFO
├─ Name: {char_info["name"]}
├─ Occupation: {char_info["occupation"]}
└─ Age: {char_info["age"]}
"""
        
        # Status de saúde
        health = status_data["health_status"]
        health_section = f"""
❤️  HEALTH STATUS
└─ {health["icon"]} {health["current_level"]} (Damage: {health["damage_taken"]})
"""
        
        # Recursos
        resources = status_data["resources"]
        resources_section = f"""
⚡ RESOURCES
├─ Luck: {resources["luck"]["current"]}/{resources["luck"]["starting"]}
├─ Magic Points: {resources["magic"]["current"]}/{resources["magic"]["starting"]}
└─ Movement: {resources["movement"]}
"""
        
        # Características
        characteristics = status_data["characteristics"]
        char_section = "📊 CHARACTERISTICS\n"
        for char_name, char_data in characteristics.items():
            char_section += f"├─ {char_name}: {char_data['full']} (Half: {char_data['half']})\n"
        char_section = char_section.rstrip('\n')
        
        # Habilidades
        skills = status_data["skills"]
        skills_section = "🎯 KEY SKILLS\n"
        
        # Habilidades comuns
        for skill_name, skill_data in skills["common"].items():
            skills_section += f"├─ {skill_name}: {skill_data['full']}% (Half: {skill_data['half']}%)\n"
        
        # Habilidades de combate
        for skill_name, skill_data in skills["combat"].items():
            skills_section += f"├─ {skill_name}: {skill_data['full']}% (Half: {skill_data['half']}%)\n"
        
        skills_section = skills_section.rstrip('\n')
        
        # Inventário
        inventory = status_data["inventory"]
        inventory_section = "🎒 INVENTORY\n"
        if inventory['equipment']:
            inventory_section += "├─ Equipment: " + ", ".join(inventory['equipment']) + "\n"
        if inventory['weapons']:
            inventory_section += "├─ Weapons: " + ", ".join(inventory['weapons']) + "\n"
        if not inventory['equipment'] and not inventory['weapons']:
            inventory_section += "└─ Empty\n"
        inventory_section = inventory_section.rstrip('\n')
        
        # Modificadores
        modifiers = status_data["modifiers"]
        modifiers_section = ""
        if modifiers:
            modifiers_section = "⚠️  ACTIVE MODIFIERS\n"
            for mod in modifiers:
                modifiers_section += f"├─ {mod.get('skill', 'General')}: {mod.get('type', 'Unknown')} ({mod.get('duration', 'Unknown')})\n"
            modifiers_section = modifiers_section.rstrip('\n')
        
        return f"{info_section}{health_section}{resources_section}{char_section}\n{skills_section}\n{inventory_section}\n{modifiers_section}".strip()

    def add_to_history(self, page_number: int, page_text: str, choice_made: Dict[str, Any], choice_index: int = None):
        """
        Adiciona uma entrada ao histórico de decisões.
        
        Args:
            page_number: Numero da página onde a decisão foi tomada
            page_text: Texto da página onde a decisão foi tomada
            choice_made: Objeto choice completo que foi escolhido
            choice_index: Índice da escolha (opcional)
        """
        self.character.add_to_history(page_number, page_text, choice_made, choice_index)

        # Manter apenas as últimas 30 entradas para evitar overflow
        history = self.character.get_history()
        if len(history) > 30:
            # Manter apenas as últimas 30 entradas
            self.character.clear_history()
            for entry in history[-30:]:
                self.character.add_to_history(
                    entry['page_number'],
                    entry['page_text'],
                    entry['choice_made'],
                    entry.get('choice_index')
                )
    
    def generate_prompt(self) -> str:
        """
        Gera o prompt completo para o LLM.
        
        Returns:
            String formatada com todo o cockpit/dashboard
        """
        sections = [
            self.render_header(),
            "",
            self._format_character_status_for_prompt(),
            "",
            self.render_current_situation(),
            "",
            self.render_history(),
            "",
            "═══════════════════════════════════════════════════════════════════════════════",
            "🤖 YOUR DECISION:",
            "Choose your action by responding with the complete choice object from the list above.",
            "Example: {'text': 'Ask about the bruise', 'goto': 14}",
            "Or: {'roll': 'DEX', 'results': {'5': {'goto': 34}, '4': {'goto': 78}}}",
            "═══════════════════════════════════════════════════════════════════════════════"
        ]
        
        return "\n".join(sections)
    
    def update_character_from_effects(self, effects: List[Dict[str, Any]]):
        """
        Aplica efeitos à ficha do personagem usando os métodos da classe Character.
        
        Args:
            effects: Lista de efeitos a aplicar
        """
        result = self.character.apply_effects(effects)
        return result
    
    def get_choice_summary(self) -> str:
        """
        Retorna um resumo das escolhas disponíveis para debug.
        
        Returns:
            String com resumo das escolhas
        """
        if not self.current_page_data:
            return "No current page data"
            
        choices = self.current_page_data.get('choices', [])
        if not choices:
            return "No choices available (end state)"
            
        summary = f"Page {self.current_page_number} has {len(choices)} choices:\n"
        for i, choice in enumerate(choices, 1):
            if isinstance(choice, dict):
                # Exibir o objeto choice completo para debug
                summary += f"  [{i}] {choice}\n"
            else:
                summary += f"  [{i}] {choice}\n"
                
        return summary.strip()


# Exemplo de uso
if __name__ == "__main__":
    # Demonstração básica da classe GamePage
    from pages import PAGES
    
    # Criar personagem usando a classe Character
    character = Character()
    character.setup("Detective Smith", "Police Officer", 35, "Experienced detective")
    
    # Criar cockpit do jogo
    cockpit = Cockpit(character, PAGES)
    cockpit.set_current_page(1)
    
    # Renderizar a tela do jogo
    cockpit.render_game_screen()

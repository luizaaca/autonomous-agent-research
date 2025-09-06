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


class GamePage:
    """
    Representa uma página/tela do jogo formatada como cockpit para o agente.
    
    Esta classe encapsula toda a informação necessária para um LLM tomar decisões
    no contexto do jogo, incluindo instruções, estado do personagem, situação atual
    e histórico de ações.
    """
    
    def __init__(self, character: Character, pages_data: Dict[int, Dict]):
        """
        Inicializa a página do jogo.
        
        Args:
            character: Instância da classe Character
            pages_data: Dicionário com todas as páginas do jogo
        """
        self.character = character
        self.pages_data = pages_data
        self.current_page_id = None
        self.current_page_data = None
        
    def set_current_page(self, page_id: int):
        """Define a página atual do jogo."""
        self.current_page_id = page_id
        self.current_page_data = self.pages_data.get(page_id, {})
        
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
    
    def render_character_status(self) -> str:
        """
        Renderiza o status atual do personagem de forma visual.
        
        Returns:
            String formatada com toda a ficha do personagem
        """
        # Informações básicas usando métodos da Character
        info_section = f"""
📋 CHARACTER INFO
├─ Name: {self.character.name}
├─ Occupation: {self.character.occupation}
└─ Age: {self.character.age}
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
        
        health_section = f"""
❤️  HEALTH STATUS
└─ {health_icons.get(current_health, '❓')} {current_health} (Damage: {damage_taken})
"""
        
        # Recursos usando métodos da Character
        luck_data = self.character.get_luck()
        magic_data = self.character.get_magic_points()
        resources_section = f"""
⚡ RESOURCES
├─ Luck: {luck_data['current']}/{luck_data['starting']}
├─ Magic Points: {magic_data['current']}/{magic_data['starting']}
└─ Movement: 8
"""
        
        # Características principais usando métodos da Character
        char_section = "📊 CHARACTERISTICS\n"
        characteristics = ["STR", "CON", "DEX", "INT", "POW"]
        for char_name in characteristics:
            try:
                char_data = self.character.get_characteristic(char_name)
                char_section += f"├─ {char_name}: {char_data['full']} (Half: {char_data['half']})\n"
            except KeyError:
                continue
        char_section = char_section.rstrip('\n')
        
        # Habilidades principais usando métodos da Character
        skills_section = "🎯 KEY SKILLS\n"
        
        # Habilidades comuns (primeiras 6)
        common_skill_names = ["Athletics", "Drive", "Navigate", "Observation", "Read Person", "Research"]
        for skill_name in common_skill_names:
            try:
                skill_data = self.character.get_skill(skill_name, "common")
                skills_section += f"├─ {skill_name}: {skill_data['full']}% (Half: {skill_data['half']}%)\n"
            except KeyError:
                continue
        
        # Habilidades de combate
        combat_skill_names = ["Fighting", "Firearms"]
        for skill_name in combat_skill_names:
            try:
                skill_data = self.character.get_skill(skill_name, "combat")
                skills_section += f"├─ {skill_name}: {skill_data['full']}% (Half: {skill_data['half']}%)\n"
            except KeyError:
                continue
            
        skills_section = skills_section.rstrip('\n')
        
        # Inventário usando métodos da Character
        inventory = self.character.get_inventory()
        inventory_section = "🎒 INVENTORY\n"
        if inventory['equipment']:
            inventory_section += "├─ Equipment: " + ", ".join(inventory['equipment']) + "\n"
        if inventory['weapons']:
            inventory_section += "├─ Weapons: " + ", ".join(inventory['weapons']) + "\n"
        if not inventory['equipment'] and not inventory['weapons']:
            inventory_section += "└─ Empty\n"
        inventory_section = inventory_section.rstrip('\n')
        
        # Modificadores ativos usando métodos da Character
        modifiers_section = ""
        modifiers = self.character.get_modifiers()
        if modifiers:
            modifiers_section = "⚠️  ACTIVE MODIFIERS\n"
            for mod in modifiers:
                modifiers_section += f"├─ {mod.get('skill', 'General')}: {mod.get('type', 'Unknown')} ({mod.get('duration', 'Unknown')})\n"
            modifiers_section = modifiers_section.rstrip('\n')
        
        return f"{info_section}{health_section}{resources_section}{char_section}\n{skills_section}\n{inventory_section}\n{modifiers_section}".strip()
    
    def render_current_situation(self) -> str:
        """
        Renderiza a situação atual (página atual e opções disponíveis).
        
        Returns:
            String formatada com a situação atual do jogo
        """
        if not self.current_page_data:
            return "📍 CURRENT SITUATION\n└─ No current page data available"
            
        situation = f"""
📍 CURRENT SITUATION - PAGE {self.current_page_id}
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
    
    def render_history(self, max_entries: int = 5) -> str:
        """
        Renderiza o histórico de decisões anteriores.
        
        Args:
            max_entries: Número máximo de entradas a mostrar
            
        Returns:
            String formatada com o histórico
        """
        history = self.character.get_history()
        
        if not history:
            return "📚 DECISION HISTORY\n└─ No previous decisions"
            
        history_section = "📚 DECISION HISTORY\n"
        recent_history = history[-max_entries:] if len(history) > max_entries else history
        
        for i, entry in enumerate(recent_history, 1):
            if isinstance(entry, dict):
                page_id = entry.get('page_id', 'Unknown')
                choice = entry.get('choice_made', 'Unknown choice')
                # Exibir o objeto choice completo
                history_section += f"├─ Step {i}: Page {page_id} → {choice}\n"
            else:
                history_section += f"├─ Step {i}: {entry}\n"
                
        history_section = history_section.rstrip('\n')
        return history_section

    def add_to_history(self, page_id: int, page_text: str, choice_made: Dict[str, Any], choice_index: int = None):
        """
        Adiciona uma entrada ao histórico de decisões.
        
        Args:
            page_id: ID da página onde a decisão foi tomada
            page_text: Texto da página onde a decisão foi tomada
            choice_made: Objeto choice completo que foi escolhido
            choice_index: Índice da escolha (opcional)
        """
        self.character.add_to_history(page_id, page_text, choice_made, choice_index)

        # Manter apenas as últimas 30 entradas para evitar overflow
        history = self.character.get_history()
        if len(history) > 20:
            # Manter apenas as últimas 30 entradas
            self.character.clear_history()
            for entry in history[-30:]:
                self.character.add_to_history(
                    entry['page_id'],
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
            self.render_character_status(),
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
            
        summary = f"Page {self.current_page_id} has {len(choices)} choices:\n"
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
    
    # Criar página do jogo
    game_page = GamePage(character, PAGES)
    game_page.set_current_page(1)
    
    # Gerar e exibir o prompt
    prompt = game_page.generate_prompt()
    print(prompt)
    print("\n" + "="*80)
    print("CHOICE SUMMARY:")
    print(game_page.get_choice_summary())

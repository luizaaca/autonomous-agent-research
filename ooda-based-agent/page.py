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


class GamePage:
    """
    Representa uma página/tela do jogo formatada como cockpit para o agente.
    
    Esta classe encapsula toda a informação necessária para um LLM tomar decisões
    no contexto do jogo, incluindo instruções, estado do personagem, situação atual
    e histórico de ações.
    """
    
    def __init__(self, character_sheet: Dict[str, Any], pages_data: Dict[int, Dict]):
        """
        Inicializa a página do jogo.
        
        Args:
            character_sheet: Ficha completa do personagem
            pages_data: Dicionário com todas as páginas do jogo
        """
        self.character_sheet = character_sheet
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
        sheet = self.character_sheet
        
        # Informações básicas
        info_section = f"""
📋 CHARACTER INFO
├─ Name: {sheet['info']['name']}
├─ Occupation: {sheet['info']['occupation']}
└─ Age: {sheet['info']['age']}
"""
        
        # Status de saúde visual
        damage_level = sheet['status']['damage_taken']
        damage_labels = sheet['status']['damage_levels']
        current_health = damage_labels[min(damage_level, len(damage_labels)-1)]
        
        health_icons = {
            "Healthy": "💚",
            "Hurt": "💛", 
            "Bloodied": "🧡",
            "Down": "❤️",
            "Impaired": "💜"
        }
        
        health_section = f"""
❤️  HEALTH STATUS
└─ {health_icons.get(current_health, '❓')} {current_health} (Damage: {damage_level})
"""
        
        # Recursos
        resources = sheet['resources']
        resources_section = f"""
⚡ RESOURCES
├─ Luck: {resources['luck']['current']}/{resources['luck']['starting']}
├─ Magic Points: {resources['magic_pts']['current']}/{resources['magic_pts']['starting']}
└─ Movement: {resources['mov']}
"""
        
        # Características principais (atributos)
        characteristics = sheet['characteristics']
        char_section = "📊 CHARACTERISTICS\n"
        for char_name, char_data in characteristics.items():
            char_section += f"├─ {char_name}: {char_data['full']} (Half: {char_data['half']})\n"
        char_section = char_section.rstrip('\n')
        
        # Habilidades principais
        skills_section = "🎯 KEY SKILLS\n"
        common_skills = sheet['skills']['common']
        for skill_name, skill_data in list(common_skills.items())[:6]:  # Top 6 skills
            skills_section += f"├─ {skill_name}: {skill_data['full']}% (Half: {skill_data['half']}%)\n"
        
        # Habilidades de combate
        combat_skills = sheet['skills']['combat']
        for skill_name, skill_data in combat_skills.items():
            skills_section += f"├─ {skill_name}: {skill_data['full']}% (Half: {skill_data['half']}%)\n"
            
        skills_section = skills_section.rstrip('\n')
        
        # Inventário
        inventory = sheet['inventory']
        inventory_section = "🎒 INVENTORY\n"
        if inventory['equipment']:
            inventory_section += "├─ Equipment: " + ", ".join(inventory['equipment']) + "\n"
        if inventory['weapons']:
            inventory_section += "├─ Weapons: " + ", ".join(inventory['weapons']) + "\n"
        if not inventory['equipment'] and not inventory['weapons']:
            inventory_section += "└─ Empty\n"
        inventory_section = inventory_section.rstrip('\n')
        
        # Modificadores ativos
        modifiers_section = ""
        if sheet['status']['modifiers']:
            modifiers_section = "⚠️  ACTIVE MODIFIERS\n"
            for mod in sheet['status']['modifiers']:
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
        history = self.character_sheet.get('page_history', [])
        
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
    
    def add_to_history(self, page_id: int, choice_made: Dict[str, Any], choice_index: int = None):
        """
        Adiciona uma entrada ao histórico de decisões.
        
        Args:
            page_id: ID da página onde a decisão foi tomada
            choice_made: Objeto choice completo que foi escolhido
            choice_index: Índice da escolha (opcional)
        """
        if 'page_history' not in self.character_sheet:
            self.character_sheet['page_history'] = []
            
        history_entry = {
            'page_id': page_id,
            'choice_made': choice_made,
            'choice_index': choice_index
        }
        
        self.character_sheet['page_history'].append(history_entry)
        
        # Manter apenas as últimas 20 entradas para evitar overflow
        if len(self.character_sheet['page_history']) > 20:
            self.character_sheet['page_history'] = self.character_sheet['page_history'][-20:]
    
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
        Aplica efeitos à ficha do personagem.
        
        Args:
            effects: Lista de efeitos a aplicar
        """
        for effect in effects:
            action = effect.get('action')
            amount = effect.get('amount', 0)
            
            if action == 'take_damage':
                self.character_sheet['status']['damage_taken'] += amount
            elif action == 'heal_damage':
                self.character_sheet['status']['damage_taken'] = max(0, 
                    self.character_sheet['status']['damage_taken'] - amount)
            elif action == 'spend_magic':
                current_magic = self.character_sheet['resources']['magic_pts']['current']
                self.character_sheet['resources']['magic_pts']['current'] = max(0, current_magic - amount)
            elif action == 'spend_luck':
                current_luck = self.character_sheet['resources']['luck']['current']
                self.character_sheet['resources']['luck']['current'] = max(0, current_luck - amount)
            elif action == 'gain_skill':
                skill_name = effect.get('skill')
                if skill_name and 'skills' in self.character_sheet:
                    # Adicionar lógica para melhorar habilidades
                    pass
            elif action == 'apply_penalty':
                # Adicionar modificador de penalidade
                modifier = {
                    'skill': effect.get('skill', 'General'),
                    'type': 'penalty_dice',
                    'duration': effect.get('duration', 'scene'),
                    'amount': amount
                }
                self.character_sheet['status']['modifiers'].append(modifier)
    
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


def create_character_sheet():
    """
    Cria um template para a ficha de personagem.
    
    Esta função mantém compatibilidade com o notebook avançado.
    """
    return {
        "info": {
            "name": "Agent",
            "occupation": None,
            "age": 30,
            "backstory": ""
        },
        "contacts": {},
        "case_files": [],
        "magic": {"spells": [], "signare": []},
        "characteristics": {
            "STR": {"full": 0, "half": 0}, "CON": {"full": 0, "half": 0},
            "DEX": {"full": 0, "half": 0}, "INT": {"full": 0, "half": 0},
            "POW": {"full": 0, "half": 0}
        },
        "resources": {
            "luck": {"starting": 0, "current": 0},
            "magic_pts": {"starting": 0, "current": 0},
            "mov": 8
        },
        "skills": {
            "common": {
                "Athletics": {"full": 30, "half": 15}, "Drive": {"full": 30, "half": 15},
                "Navigate": {"full": 30, "half": 15}, "Observation": {"full": 30, "half": 15},
                "Read Person": {"full": 30, "half": 15}, "Research": {"full": 30, "half": 15},
                "Social": {"full": 30, "half": 15}, "Stealth": {"full": 30, "half": 15},
            },
            "combat": {
                "Fighting": {"full": 30, "half": 15}, "Firearms": {"full": 30, "half": 15}
            },
            "expert": {}
        },
        "status": {
            "damage_levels": ["Healthy", "Hurt", "Bloodied", "Down", "Impaired"],
            "damage_taken": 0,
            "modifiers": []
        },
        "inventory": {"equipment": [], "weapons": []},
        "page_history": []
    }


# Exemplo de uso
if __name__ == "__main__":
    # Demonstração básica da classe GamePage
    from pages import PAGES
    
    # Criar ficha de personagem
    character = create_character_sheet()
    character["info"]["name"] = "Detective Smith"
    character["info"]["occupation"] = "Police Officer"
    character["resources"]["luck"]["starting"] = 65
    character["resources"]["luck"]["current"] = 65
    character["resources"]["magic_pts"]["starting"] = 10
    character["resources"]["magic_pts"]["current"] = 10
    
    # Adicionar valores às características
    character["characteristics"]["STR"] = {"full": 50, "half": 25}
    character["characteristics"]["CON"] = {"full": 60, "half": 30}
    character["characteristics"]["DEX"] = {"full": 70, "half": 35}
    character["characteristics"]["INT"] = {"full": 80, "half": 40}
    character["characteristics"]["POW"] = {"full": 55, "half": 27}
    
    # Criar página do jogo
    game_page = GamePage(character, PAGES)
    game_page.set_current_page(1)
    
    # Gerar e exibir o prompt
    prompt = game_page.generate_prompt()
    print(prompt)
    print("\n" + "="*80)
    print("CHOICE SUMMARY:")
    print(game_page.get_choice_summary())

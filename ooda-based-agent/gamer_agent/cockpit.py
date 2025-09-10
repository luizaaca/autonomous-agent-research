"""
Page Module - Cockpit/Dashboard para Agente Autônomo

Este módulo implementa a classe GamePage que serve como interface cockpit/dashboard
para o agente autônomo, fornecendo uma visão completa do estado do jogo formatada
como prompt para LLMs.

A estrutura é dividida em:
- Header: Instruções fixas do jogo
- Body: Estado atual do personagem (ficha, status, inventário, histórico)
"""

from typing import Dict, Any
import json
from character import Character


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
        
    def set_current_page(self, page_number: int):
        """Define a página atual do jogo."""
        self.current_page_number = page_number
        
        # Compatibilidade com objetos GameData que têm método .get()
        if hasattr(self.pages_data, 'get'):
            self.current_page_data = self.pages_data.get(page_number, {})
        else:
            # Fallback para dicionários diretos
            self.current_page_data = self.pages_data.get(page_number, {})
    
    
    
    
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
        print(f"Luck data: {luck_data}")
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
        skills = self.character.get_all_skills()
        
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
                }
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
        
    def add_to_history(self, page_number: int, page_text: str, choice_made: Dict[str, Any], choice_index: int = None, reason: str = None):
        """
        Adiciona uma entrada ao histórico de decisões.
        
        Args:
            page_number: Numero da página onde a decisão foi tomada
            page_text: Texto da página onde a decisão foi tomada
            choice_made: Objeto choice completo que foi escolhido
            choice_index: Índice da escolha (opcional)
        """
        self.character.add_to_history(page_number, page_text, choice_made, choice_index, reason)

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
                    entry.get('choice_index'),
                    entry.get('reason')
                )

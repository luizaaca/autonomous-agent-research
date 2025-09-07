"""
Player Adapters Module - Implementações concretas dos adaptadores de entrada

Este módulo contém as implementações concretas da interface PlayerInputAdapter
para diferentes modos de jogo: demonstração, humano e IA.
"""

from player_input_adapter import PlayerInputAdapter
from typing import List, Dict, Any
import os
import random


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
        self._last_decision_reason = ""
    
    def get_decision(self, available_choices: List[Dict[str, Any]], character_data: Dict[str, Any]) -> int:
        """
        Toma decisão automática baseada na lógica internalizada do DefaultDecisionController.
        
        Args:
            available_choices: Lista de choices disponíveis
            character_data: Dados estruturados do personagem (não usado no modo demo)
            
        Returns:
            Índice (base 1) da escolha selecionada
        """
        if self.debug:
            print(f"[DemoPlayerAdapter] Processando {len(available_choices)} choices")
        
        # Validação básica
        if not available_choices:
            raise Exception("Lista de choices vazia - não é possível tomar decisão")
        
        # Processar choices válidas (lógica simplificada)
        valid_choice_indices = []
        
        for i, choice in enumerate(available_choices):
            # Para o modo demo, consideramos todas as choices básicas como válidas
            # Choices condicionais requerem validação específica no Agent
            if self._is_basic_choice(choice):
                valid_choice_indices.append(i)
        
        # Se não encontrou choices válidas, usar a primeira como fallback
        if not valid_choice_indices:
            if self.debug:
                print("[DemoPlayerAdapter] Nenhuma choice básica encontrada - usando primeira como fallback")
            return 1  # Primeira choice (base 1)
        
        # Selecionar primeira choice válida
        selected_index = valid_choice_indices[0]
        
        if self.debug:
            choice_text = available_choices[selected_index].get('text', str(available_choices[selected_index])[:50])
            print(f"[DemoPlayerAdapter] Selecionada choice {selected_index + 1}: {choice_text}")
        
        return selected_index + 1  # Converter para base 1
    
    def _is_basic_choice(self, choice: Dict[str, Any]) -> bool:
        """
        Verifica se uma choice é básica (não requer validação especial).
        
        Args:
            choice: Choice a ser verificada
            
        Returns:
            True se for uma choice básica
        """
        # Choice básica: tem 'goto' e não tem condicionais complexas
        if 'goto' in choice and 'conditional_on' not in choice:
            return True
        
        # Choice com roll também é considerada básica para demo
        if any(key in choice for key in ['roll', 'luck_roll', 'opposed_roll']):
            return True
            
        return False
    
    def _format_compact_cockpit(self, character_data: Dict[str, Any]) -> str:
        """
        Formata dados do personagem em formato compacto para telas 480p.
        
        Args:
            character_data: Dados estruturados do personagem do cockpit
            
        Returns:
            String formatada de forma compacta e tabular
        """
        lines = []
        
        # Linha 1: Info básica | Status de saúde | Recursos
        char_info = character_data.get('character_info', {})
        health = character_data.get('health_status', {})
        resources = character_data.get('resources', {})
        
        line1_parts = [
            f"{char_info.get('name', 'Unknown')} ({char_info.get('occupation', 'N/A')}, {char_info.get('age', 0)})",
            f"{health.get('icon', '❓')} {health.get('current_level', 'Unknown')} (DMG:{health.get('damage_taken', 0)})",
            f"Luck:{resources.get('luck', {}).get('current', 0)}/{resources.get('luck', {}).get('starting', 0)} Magic:{resources.get('magic', {}).get('current', 0)}/{resources.get('magic', {}).get('starting', 0)} Mov:{resources.get('movement', 8)}"
        ]
        lines.append("📋 " + " | ".join(line1_parts))
        
        # Linha 2: Características principais
        characteristics = character_data.get('characteristics', {})
        char_parts = []
        for char_name in ["STR", "CON", "DEX", "INT", "POW"]:
            char_data = characteristics.get(char_name, {})
            if char_data:
                char_parts.append(f"{char_name}:{char_data.get('full', 0)}")
        lines.append("📊 " + " ".join(char_parts))
        
        # Linha 3: Habilidades principais (compactas)
        skills = character_data.get('skills', {})
        skill_parts = []
        
        # Habilidades comuns mais importantes
        common_skills = skills.get('common', {})
        for skill in ['Athletics', 'Observation', 'Navigate']:
            if skill in common_skills:
                skill_parts.append(f"{skill}:{common_skills[skill].get('full', 0)}%")
        
        # Habilidades de combate
        combat_skills = skills.get('combat', {})
        for skill in ['Fighting', 'Firearms']:
            if skill in combat_skills:
                skill_parts.append(f"{skill}:{combat_skills[skill].get('full', 0)}%")
        
        lines.append("🎯 " + " ".join(skill_parts))
        
        # Linha 4: Inventário e modificadores (se houver)
        inventory = character_data.get('inventory', {})
        modifiers = character_data.get('modifiers', [])
        
        line4_parts = []
        
        # Inventário resumido
        items = []
        if inventory.get('equipment'):
            items.extend(inventory['equipment'][:2])  # Primeiros 2 items
        if inventory.get('weapons'):
            items.extend(inventory['weapons'][:2])    # Primeiras 2 armas
        
        if items:
            line4_parts.append(f"Items: {', '.join(items)}")
        else:
            line4_parts.append("Items: Empty")
        
        # Modificadores ativos (resumidos)
        if modifiers:
            mod_count = len(modifiers)
            line4_parts.append(f"Modifiers: {mod_count} active")
        
        if line4_parts:
            lines.append("🎒 " + " | ".join(line4_parts))
        
        return "\n".join(lines)


class HumanPlayerAdapter(PlayerInputAdapter):
    """
    Adapter para jogador humano via console.
    Implementa input loop com validação para capturar escolhas do usuário.
    """
    
    def get_decision(self, available_choices: List[Dict[str, Any]], character_data: Dict[str, Any]) -> int:
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
    
    def get_decision(self, available_choices: List[Dict[str, Any]], character_data: Dict[str, Any]) -> int:
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

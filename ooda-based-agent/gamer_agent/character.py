"""
Character Module - Classe centralizada para gerenciamento de personagem

Este módulo implementa a classe Character que centraliza toda a lógica relacionada
à ficha do personagem, incluindo características, habilidades, recursos, saúde,
dano e aplicação de efeitos.

A classe Character substitui as funções dispersas de create_character_sheet() e
setup_character(), oferecendo uma interface orientada a objetos para todas as
operações relacionadas ao personagem.
"""

import random
from typing import Dict, List, Any, Optional, Union


class Character:
    """
    Classe centralizada para gerenciamento completo de personagem.
    
    Esta classe encapsula toda a lógica relacionada à ficha do personagem,
    incluindo criação, configuração, características, habilidades, recursos,
    saúde, dano e histórico de ações.
    """
    
    def __init__(self, name: str = "Character Name", occupation: Optional[str] = None, 
                 age: int = 30, backstory: str = ""):
        """
        Inicializa um novo personagem.
        
        Args:
            name: Nome do personagem
            occupation: Ocupação do personagem (Police Officer, Social Worker, Nurse)
            age: Idade do personagem
            backstory: História de fundo do personagem
        """
        self._sheet = self._create_base_sheet()
        self.setup(name, occupation, age, backstory)
    
    def _create_base_sheet(self) -> Dict[str, Any]:
        """
        Cria a estrutura base da ficha de personagem.
        
        Returns:
            Dicionário com a estrutura completa da ficha
        """
        return {
            "info": {
                "name": "Character Name",
                "occupation": None,
                "age": 30,
                "backstory": ""
            },
            "contacts": {},
            "case_files": [],
            "magic": {"spells": [], "signare": []},
            "characteristics": {
                "STR": {"full": 0, "half": 0}, 
                "CON": {"full": 0, "half": 0},
                "DEX": {"full": 0, "half": 0}, 
                "INT": {"full": 0, "half": 0},
                "POW": {"full": 0, "half": 0}
            },
            "resources": {
                "luck": {"starting": 0, "current": 0},
                "magic_pts": {"starting": 0, "current": 0},
                "mov": 8
            },
            "skills": {
                "common": {
                    "Athletics": {"full": 30, "half": 15}, 
                    "Drive": {"full": 30, "half": 15},
                    "Navigate": {"full": 30, "half": 15}, 
                    "Observation": {"full": 30, "half": 15},
                    "Read Person": {"full": 30, "half": 15}, 
                    "Research": {"full": 30, "half": 15},
                    "Social": {"full": 30, "half": 15}, 
                    "Stealth": {"full": 30, "half": 15},
                },
                "combat": {
                    "Fighting": {"full": 30, "half": 15}, 
                    "Firearms": {"full": 30, "half": 15}
                },
                "expert": {}
            },
            "status": {
                "damage_levels": ["Healthy", "Hurt", "Bloodied", "Down", "Impaired"],
                "damage_taken": 0,
                "modifiers": []  # e.g., {"skill": "Fighting", "type": "penalty_dice", "duration": "scene"}
            },
            "inventory": {"equipment": [], "weapons": []},
            "page_history": []
        }
    
    def setup(self, name: str, occupation: str, age: int = 30, backstory: str = ""):
        """
        Configura o personagem com informações básicas e ajusta atributos baseados na ocupação.
        
        Args:
            name: Nome do personagem
            occupation: Ocupação/profissão do personagem
            age: Idade do personagem (padrão: 30)
            backstory: História de fundo do personagem
        """
        # Configurações básicas
        self.sheet["info"]["name"] = name
        self.sheet["info"]["occupation"] = occupation
        self.sheet["info"]["age"] = age
        self.sheet["info"]["backstory"] = backstory
        
        # Calcular e definir recursos iniciais
        import random
        
        # Sorte inicial (2d10 + 50)
        luck_roll = random.randint(1, 10) + random.randint(1, 10) + 50
        self.sheet["resources"]["luck"]["starting"] = luck_roll
        self.sheet["resources"]["luck"]["current"] = luck_roll
        
        # Magic Points iniciais baseados em POW (assumindo POW padrão de 60 para agentes)
        default_pow = 60
        magic_points = default_pow
        self.sheet["resources"]["magic_pts"]["starting"] = magic_points
        self.sheet["resources"]["magic_pts"]["current"] = magic_points
        
        # Configurar características baseadas na ocupação
        if occupation == "Police Officer":
            # Características melhoradas para policial
            self.sheet["characteristics"]["STR"] = {"full": 65, "half": 32}
            self.sheet["characteristics"]["CON"] = {"full": 60, "half": 30}
            self.sheet["characteristics"]["DEX"] = {"full": 55, "half": 27}
            self.sheet["characteristics"]["INT"] = {"full": 55, "half": 27}
            self.sheet["characteristics"]["POW"] = {"full": 60, "half": 30}
            
            # Ajustar magic points baseado no POW real
            actual_pow = self.sheet["characteristics"]["POW"]["full"]
            self.sheet["resources"]["magic_pts"]["starting"] = actual_pow
            self.sheet["resources"]["magic_pts"]["current"] = actual_pow
            
            # Perícias aprimoradas para policial
            self.sheet["skills"]["common"]["Athletics"] = {"full": 60, "half": 30}
            self.sheet["skills"]["common"]["Drive"] = {"full": 60, "half": 30}
            self.sheet["skills"]["common"]["Social"] = {"full": 60, "half": 30}
            self.sheet["skills"]["combat"]["Fighting"] = {"full": 60, "half": 30}
            self.sheet["skills"]["combat"]["Firearms"] = {"full": 60, "half": 30}
            
            # Perícias especializadas
            self.sheet["skills"]["expert"]["Law"] = {"full": 60, "half": 30}
            self.sheet["skills"]["expert"]["Magic"] = {"full": 60, "half": 30}
            
        elif occupation == "Social Worker":
            # Características para assistente social
            self.sheet["characteristics"]["STR"] = {"full": 50, "half": 25}
            self.sheet["characteristics"]["CON"] = {"full": 55, "half": 27}
            self.sheet["characteristics"]["DEX"] = {"full": 50, "half": 25}
            self.sheet["characteristics"]["INT"] = {"full": 70, "half": 35}
            self.sheet["characteristics"]["POW"] = {"full": 65, "half": 32}
            
            # Ajustar magic points baseado no POW
            actual_pow = self.sheet["characteristics"]["POW"]["full"]
            self.sheet["resources"]["magic_pts"]["starting"] = actual_pow
            self.sheet["resources"]["magic_pts"]["current"] = actual_pow
            
            # Perícias aprimoradas
            self.sheet["skills"]["common"]["Observation"] = {"full": 60, "half": 30}
            self.sheet["skills"]["common"]["Research"] = {"full": 60, "half": 30}
            self.sheet["skills"]["common"]["Social"] = {"full": 70, "half": 35}
            self.sheet["skills"]["expert"]["Magic"] = {"full": 60, "half": 30}
            
        elif occupation == "Nurse":
            # Características para enfermeiro/a
            self.sheet["characteristics"]["STR"] = {"full": 50, "half": 25}
            self.sheet["characteristics"]["CON"] = {"full": 60, "half": 30}
            self.sheet["characteristics"]["DEX"] = {"full": 60, "half": 30}
            self.sheet["characteristics"]["INT"] = {"full": 65, "half": 32}
            self.sheet["characteristics"]["POW"] = {"full": 60, "half": 30}
            
            # Ajustar magic points baseado no POW
            actual_pow = self.sheet["characteristics"]["POW"]["full"]
            self.sheet["resources"]["magic_pts"]["starting"] = actual_pow
            self.sheet["resources"]["magic_pts"]["current"] = actual_pow
            
            # Perícias aprimoradas
            self.sheet["skills"]["common"]["Observation"] = {"full": 70, "half": 35}
            self.sheet["skills"]["common"]["Read Person"] = {"full": 60, "half": 30}
            self.sheet["skills"]["common"]["Social"] = {"full": 60, "half": 30}
            self.sheet["skills"]["expert"]["Medicine"] = {"full": 70, "half": 35}
            self.sheet["skills"]["expert"]["Magic"] = {"full": 60, "half": 30}
        
        else:
            # Ocupação genérica - valores padrão
            self.sheet["characteristics"]["STR"] = {"full": 55, "half": 27}
            self.sheet["characteristics"]["CON"] = {"full": 55, "half": 27}
            self.sheet["characteristics"]["DEX"] = {"full": 55, "half": 27}
            self.sheet["characteristics"]["INT"] = {"full": 55, "half": 27}
            self.sheet["characteristics"]["POW"] = {"full": 55, "half": 27}
            
            # Magic points baseado no POW padrão
            self.sheet["resources"]["magic_pts"]["starting"] = 55
            self.sheet["resources"]["magic_pts"]["current"] = 55
        
        print(f"Character {name} ({occupation}) initialized successfully.")
        print(f"Luck: {self.sheet['resources']['luck']['current']}")
        print(f"Magic Points: {self.sheet['resources']['magic_pts']['current']}")
        return True
    
    # Propriedades para acesso fácil aos dados principais
    @property
    def name(self) -> str:
        """Nome do personagem."""
        return self._sheet["info"]["name"]
    
    @property
    def occupation(self) -> Optional[str]:
        """Ocupação do personagem."""
        return self._sheet["info"]["occupation"]
    
    @property
    def age(self) -> int:
        """Idade do personagem."""
        return self._sheet["info"]["age"]
    
    @property
    def backstory(self) -> str:
        """História de fundo do personagem."""
        return self._sheet["info"]["backstory"]
    
    @property
    def sheet(self) -> Dict[str, Any]:
        """
        Acesso direto à ficha completa (para compatibilidade).
        
        Returns:
            Dicionário completo da ficha do personagem
        """
        return self._sheet
    
    def get_game_backstory(self) -> str:
        """
        Gera backstory contextualizado para o jogo baseado na ocupação.
        
        Substitui a lógica de GameInstructions.get_backstory() centralizando
        a responsabilidade de backstory na classe Character, que é quem
        deve conhecer seu contexto de jogo.
        
        Returns:
            String com backstory completo incluindo contexto do jogo e ocupação
        """
        base_context = "Você é um agente OODA baseado em IA navegando por um livro-jogo de investigação policial."
        
        occupation_context = {
            "Police Officer": "Como policial experiente, você tem autoridade e conhecimento sobre procedimentos legais.",
            "Social Worker": "Como assistente social, você entende comportamento humano e tem habilidades de comunicação.",
            "Nurse": "Como enfermeiro, você tem conhecimento médico e experiência em situações de crise."
        }
        
        occupation_specific = occupation_context.get(self.occupation, "Você deve usar suas habilidades únicas")
        
        game_objective = "Seu objetivo é resolver o mistério, tomar decisões estratégicas e manter seu personagem vivo. Use suas habilidades de raciocínio, análise e tomada de decisão para progredir na história."
        
        return f"{base_context} {occupation_specific} {game_objective}"
    
    def get_characteristic(self, char_name: str) -> Dict[str, int]:
        """
        Obtém os valores de uma característica específica.
        
        Args:
            char_name: Nome da característica (STR, CON, DEX, INT, POW)
            
        Returns:
            Dicionário com valores 'full' e 'half' da característica
            
        Raises:
            KeyError: Se a característica não existir
        """
        if char_name not in self._sheet["characteristics"]:
            raise KeyError(f"Característica '{char_name}' não encontrada")
        return self._sheet["characteristics"][char_name].copy()
    
    def get_skill(self, skill_name: str, skill_type: str = "common") -> Dict[str, int]:
        """
        Obtém os valores de uma habilidade específica.
        
        Args:
            skill_name: Nome da habilidade
            skill_type: Tipo da habilidade ("common", "combat", "expert")
            
        Returns:
            Dicionário com valores 'full' e 'half' da habilidade
            
        Raises:
            KeyError: Se a habilidade não existir
        """
        if skill_type not in self._sheet["skills"]:
            raise KeyError(f"Tipo de habilidade '{skill_type}' não encontrado")
        
        if skill_name not in self._sheet["skills"][skill_type]:
            raise KeyError(f"Habilidade '{skill_name}' não encontrada em '{skill_type}'")
        
        return self._sheet["skills"][skill_type][skill_name].copy()
    
    def get_luck(self) -> Dict[str, int]:
        """
        Obtém os valores atuais e iniciais de sorte.
        
        Returns:
            Dicionário com 'current' e 'starting' luck
        """
        return self._sheet["resources"]["luck"].copy()
    
    def get_magic_points(self) -> Dict[str, int]:
        """
        Obtém os valores atuais e iniciais de pontos de magia.
        
        Returns:
            Dicionário com 'current' e 'starting' magic points
        """
        return self._sheet["resources"]["magic_pts"].copy()
    
    def get_health_status(self) -> str:
        """
        Obtém o status atual de saúde do personagem.
        
        Returns:
            String com o status de saúde atual
        """
        damage = self._sheet["status"]["damage_taken"]
        damage_levels = self._sheet["status"]["damage_levels"]
        
        if damage >= len(damage_levels):
            return "Impaired"
        return damage_levels[damage]
    
    def is_alive(self) -> bool:
        """
        Verifica se o personagem ainda está vivo/ativo.
        
        Returns:
            True se o personagem não estiver Impaired, False caso contrário
        """
        return self.get_health_status() != "Impaired"
    
    # Métodos de gerenciamento de recursos
    def can_spend_luck(self, amount: int) -> bool:
        """
        Verifica se o personagem tem sorte suficiente para gastar.
        
        Args:
            amount: Quantidade de sorte a verificar
            
        Returns:
            True se tiver sorte suficiente, False caso contrário
        """
        current_luck = self._sheet["resources"]["luck"]["current"]
        return current_luck >= amount and amount > 0
    
    def can_spend_magic(self, amount: int) -> bool:
        """
        Verifica se o personagem tem pontos de magia suficientes para gastar.
        
        Args:
            amount: Quantidade de pontos de magia a verificar
            
        Returns:
            True se tiver pontos suficientes, False caso contrário
        """
        current_magic = self._sheet["resources"]["magic_pts"]["current"]
        return current_magic >= amount and amount > 0
    
    def spend_luck(self, amount: int) -> Dict[str, Any]:
        """
        Gasta pontos de sorte do personagem.
        
        Args:
            amount: Quantidade de sorte a gastar
            
        Returns:
            Dicionário com resultado da operação
        """
        if not isinstance(amount, (int, float)) or amount < 0:
            return {
                "success": False,
                "error": "Quantidade deve ser um número não negativo",
                "spent": 0,
                "remaining": self._sheet["resources"]["luck"]["current"]
            }
        
        if not self.can_spend_luck(amount):
            return {
                "success": False,
                "error": f"Luck insuficiente. Atual: {self._sheet['resources']['luck']['current']}, Necessário: {amount}",
                "spent": 0,
                "remaining": self._sheet["resources"]["luck"]["current"]
            }
        
        old_value = self._sheet["resources"]["luck"]["current"]
        self._sheet["resources"]["luck"]["current"] -= amount
        
        return {
            "success": True,
            "spent": amount,
            "remaining": self._sheet["resources"]["luck"]["current"],
            "previous": old_value
        }
    
    def spend_magic(self, amount: int) -> Dict[str, Any]:
        """
        Gasta pontos de magia do personagem.
        
        Args:
            amount: Quantidade de pontos de magia a gastar
            
        Returns:
            Dicionário com resultado da operação
        """
        if not isinstance(amount, (int, float)) or amount < 0:
            return {
                "success": False,
                "error": "Quantidade deve ser um número não negativo",
                "spent": 0,
                "remaining": self._sheet["resources"]["magic_pts"]["current"]
            }
        
        if not self.can_spend_magic(amount):
            return {
                "success": False,
                "error": f"Magic insuficiente. Atual: {self._sheet['resources']['magic_pts']['current']}, Necessário: {amount}",
                "spent": 0,
                "remaining": self._sheet["resources"]["magic_pts"]["current"]
            }
        
        old_value = self._sheet["resources"]["magic_pts"]["current"]
        self._sheet["resources"]["magic_pts"]["current"] -= amount
        
        return {
            "success": True,
            "spent": amount,
            "remaining": self._sheet["resources"]["magic_pts"]["current"],
            "previous": old_value
        }
    
    def restore_luck(self, amount: int) -> None:
        """
        Restaura pontos de sorte do personagem.
        
        Args:
            amount: Quantidade de sorte a restaurar
        """
        if amount <= 0:
            return
        
        current = self._sheet["resources"]["luck"]["current"]
        starting = self._sheet["resources"]["luck"]["starting"]
        
        # Não pode exceder o valor inicial
        self._sheet["resources"]["luck"]["current"] = min(current + amount, starting)
    
    def restore_magic(self, amount: int) -> None:
        """
        Restaura pontos de magia do personagem.
        
        Args:
            amount: Quantidade de pontos de magia a restaurar
        """
        if amount <= 0:
            return
        
        current = self._sheet["resources"]["magic_pts"]["current"]
        starting = self._sheet["resources"]["magic_pts"]["starting"]
        
        # Não pode exceder o valor inicial
        self._sheet["resources"]["magic_pts"]["current"] = min(current + amount, starting)
    
    def set_magic_points(self, starting_value: int) -> None:
        """
        Define os pontos de magia iniciais e atuais do personagem.
        
        Args:
            starting_value: Valor inicial de pontos de magia
        """
        if starting_value < 0:
            starting_value = 0
        
        self._sheet["resources"]["magic_pts"]["starting"] = starting_value
        self._sheet["resources"]["magic_pts"]["current"] = starting_value
    
    # Métodos melhorados de validação
    def validate_characteristic_value(self, value: int) -> int:
        """
        Valida e corrige um valor de característica.
        
        Args:
            value: Valor a validar
            
        Returns:
            Valor validado (entre 1 e 100)
        """
        return max(1, min(100, value))
    
    def validate_skill_value(self, value: int) -> int:
        """
        Valida e corrige um valor de habilidade.
        
        Args:
            value: Valor a validar
            
        Returns:
            Valor validado (entre 0 e 100)
        """
        return max(0, min(100, value))
    
    def set_characteristic(self, char_name: str, value: int) -> Dict[str, Any]:
        """
        Define o valor de uma característica específica.
        
        Args:
            char_name: Nome da característica (STR, CON, DEX, INT, POW)
            value: Novo valor da característica
            
        Returns:
            Dicionário com resultado da operação
        """
        if char_name not in self._sheet["characteristics"]:
            return {
                "success": False,
                "error": f"Característica '{char_name}' não encontrada"
            }
        
        try:
            validated_value = self.validate_characteristic_value(value)
        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }
        
        old_value = self._sheet["characteristics"][char_name]["full"]
        half_value = validated_value // 2
        
        self._sheet["characteristics"][char_name] = {
            "full": validated_value,
            "half": half_value
        }
        
        return {
            "success": True,
            "characteristic": char_name,
            "old_value": old_value,
            "new_value": validated_value,
            "half_value": half_value
        }
    
    def set_skill(self, skill_name: str, value: int, skill_type: str = "common") -> Dict[str, Any]:
        """
        Define o valor de uma habilidade específica.
        
        Args:
            skill_name: Nome da habilidade
            value: Novo valor da habilidade
            skill_type: Tipo da habilidade ("common", "combat", "expert")
            
        Returns:
            Dicionário com resultado da operação
        """
        if skill_type not in self._sheet["skills"]:
            return {
                "success": False,
                "error": f"Tipo de habilidade '{skill_type}' não encontrado"
            }
        
        try:
            validated_value = self.validate_skill_value(value)
        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }
        
        # Valor anterior (se existir)
        old_value = None
        if skill_name in self._sheet["skills"][skill_type]:
            old_value = self._sheet["skills"][skill_type][skill_name]["full"]
        
        half_value = validated_value // 2
        
        self._sheet["skills"][skill_type][skill_name] = {
            "full": validated_value,
            "half": half_value
        }
        
        return {
            "success": True,
            "skill": skill_name,
            "skill_type": skill_type,
            "old_value": old_value,
            "new_value": validated_value,
            "half_value": half_value
        }
    
    # Sistema de rolagens
    def _make_d100_roll(self, bonus_dice: bool = False, penalty_dice: bool = False) -> int:
        """
        Executa uma rolagem D100 com suporte para bonus/penalty dice.
        
        Args:
            bonus_dice: Se True, usa o menor dos dois dados de dezena
            penalty_dice: Se True, usa o maior dos dois dados de dezena
            
        Returns:
            Resultado da rolagem (1-100)
        """
        tens_roll_1 = random.randint(0, 9) * 10
        tens_roll_2 = random.randint(0, 9) * 10
        units_roll = random.randint(1, 10)
        
        # Bonus e penalty dice se anulam
        if bonus_dice and penalty_dice:
            bonus_dice = False
            penalty_dice = False
        
        if bonus_dice:
            final_tens = min(tens_roll_1, tens_roll_2)
        elif penalty_dice:
            final_tens = max(tens_roll_1, tens_roll_2)
        else:
            final_tens = tens_roll_1
        
        # Calcula resultado final
        if final_tens == 0 and units_roll == 10:
            return 100
        elif final_tens == 0:
            return units_roll
        else:
            return final_tens + (units_roll % 10)
    
    def _evaluate_roll_result(self, roll: int, target_value: int, half_value: int) -> tuple[int, str]:
        """
        Avalia o resultado de uma rolagem D100.
        
        Args:
            roll: Resultado da rolagem
            target_value: Valor alvo (skill full)
            half_value: Valor de meio (skill half)
            
        Returns:
            Tupla (nível_sucesso, descrição)
            5 = Critical Success, 4 = Hard Success, 3 = Success, 2 = Failure, 1 = Fumble
        """
        if roll == 1:
            return (5, "Critical Success")
        if roll == 100:
            return (1, "Fumble")
        if roll <= half_value:
            return (4, "Hard Success")
        if roll <= target_value:
            return (3, "Success")
        
        return (2, "Failure")
    
    def roll_skill(self, skill_name: str, skill_type: str = "common", 
                   bonus_dice: bool = False, penalty_dice: bool = False, 
                   difficulty: str = "regular", auto_apply_modifiers: bool = True) -> Dict[str, Any]:
        """
        Executa uma rolagem de habilidade.
        
        Args:
            skill_name: Nome da habilidade
            skill_type: Tipo da habilidade ("common", "combat", "expert")
            bonus_dice: Se True, aplica bonus dice
            penalty_dice: Se True, aplica penalty dice
            difficulty: Dificuldade do teste ("regular", "hard")
            auto_apply_modifiers: Se True, aplica modificadores automaticamente
            
        Returns:
            Dicionário com resultado da rolagem
        """
        try:
            skill_data = self.get_skill(skill_name, skill_type)
        except KeyError as e:
            return {
                "success": False,
                "error": str(e),
                "roll": 0,
                "target": 0,
                "level": 0,
                "description": "Skill not found"
            }
        
        # Verificar modificadores se habilitado
        final_bonus_dice = bonus_dice
        final_penalty_dice = penalty_dice
        
        if auto_apply_modifiers:
            modifiers = self.check_skill_modifiers(skill_name, skill_type)
            
            # Aplicar modificadores (bonus e penalty se cancelam)
            if modifiers["has_bonus"] and not modifiers["has_penalty"]:
                final_bonus_dice = True
            elif modifiers["has_penalty"] and not modifiers["has_bonus"]:
                final_penalty_dice = True
            # Se ambos existem, se cancelam (mantém valores originais)
        
        # Determinar valores alvo baseado na dificuldade
        if difficulty == "hard":
            target_value = skill_data["half"]
            half_value = target_value // 2
        else:  # regular
            target_value = skill_data["full"]
            half_value = skill_data["half"]
        
        # Executar rolagem
        roll = self._make_d100_roll(final_bonus_dice, final_penalty_dice)
        level, description = self._evaluate_roll_result(roll, target_value, half_value)
        
        return {
            "success": True,
            "skill": skill_name,
            "skill_type": skill_type,
            "difficulty": difficulty,
            "roll": roll,
            "target": target_value,
            "half_target": half_value,
            "level": level,
            "description": description,
            "bonus_dice": final_bonus_dice,
            "penalty_dice": final_penalty_dice,
            "modifiers_applied": auto_apply_modifiers
        }
    
    def roll_characteristic(self, char_name: str, bonus_dice: bool = False, 
                           penalty_dice: bool = False, difficulty: str = "regular") -> Dict[str, Any]:
        """
        Executa uma rolagem de característica.
        
        Args:
            char_name: Nome da característica (STR, CON, DEX, INT, POW)
            bonus_dice: Se True, aplica bonus dice
            penalty_dice: Se True, aplica penalty dice
            difficulty: Dificuldade do teste ("regular", "hard")
            
        Returns:
            Dicionário com resultado da rolagem
        """
        try:
            char_data = self.get_characteristic(char_name)
        except KeyError as e:
            return {
                "success": False,
                "error": str(e),
                "roll": 0,
                "target": 0,
                "level": 0,
                "description": "Characteristic not found"
            }
        
        # Determinar valores alvo baseado na dificuldade
        if difficulty == "hard":
            target_value = char_data["half"]
            half_value = target_value // 2
        else:  # regular
            target_value = char_data["full"]
            half_value = char_data["half"]
        
        # Executar rolagem
        roll = self._make_d100_roll(bonus_dice, penalty_dice)
        level, description = self._evaluate_roll_result(roll, target_value, half_value)
        
        return {
            "success": True,
            "characteristic": char_name,
            "difficulty": difficulty,
            "roll": roll,
            "target": target_value,
            "half_target": half_value,
            "level": level,
            "description": description,
            "bonus_dice": bonus_dice,
            "penalty_dice": penalty_dice
        }
    
    def roll_luck(self, bonus_dice: bool = False, penalty_dice: bool = False) -> Dict[str, Any]:
        """
        Executa uma rolagem de sorte.
        
        Args:
            bonus_dice: Se True, aplica bonus dice
            penalty_dice: Se True, aplica penalty dice
            
        Returns:
            Dicionário com resultado da rolagem
        """
        luck_data = self.get_luck()
        target_value = luck_data["current"]
        half_value = target_value // 2
        
        # Executar rolagem
        roll = self._make_d100_roll(bonus_dice, penalty_dice)
        level, description = self._evaluate_roll_result(roll, target_value, half_value)
        
        return {
            "success": True,
            "type": "luck",
            "roll": roll,
            "target": target_value,
            "half_target": half_value,
            "level": level,
            "description": description,
            "bonus_dice": bonus_dice,
            "penalty_dice": penalty_dice
        }
    
    def opposed_roll(self, my_skill: str, my_skill_type: str = "common",
                    opponent_skill_full: int = 30, opponent_skill_half: int = 15,
                    my_bonus_dice: bool = False, my_penalty_dice: bool = False) -> Dict[str, Any]:
        """
        Executa um teste oposto entre duas habilidades.
        
        Args:
            my_skill: Nome da minha habilidade
            my_skill_type: Tipo da minha habilidade
            opponent_skill_full: Valor full da habilidade do oponente
            opponent_skill_half: Valor half da habilidade do oponente
            my_bonus_dice: Se True, aplica bonus dice para mim
            my_penalty_dice: Se True, aplica penalty dice para mim
            
        Returns:
            Dicionário com resultado do teste oposto
        """
        # Minha rolagem
        my_result = self.roll_skill(my_skill, my_skill_type, my_bonus_dice, my_penalty_dice)
        
        if not my_result["success"]:
            return my_result
        
        # Rolagem do oponente
        opponent_roll = self._make_d100_roll()
        opponent_level, opponent_desc = self._evaluate_roll_result(
            opponent_roll, opponent_skill_full, opponent_skill_half
        )
        
        # Determinar vencedor
        my_level = my_result["level"]
        
        if my_level > opponent_level:
            outcome = "win"
        elif my_level < opponent_level:
            outcome = "lose"
        else:
            # Mesmo nível de sucesso, comparar rolagens (menor vence)
            if my_result["roll"] < opponent_roll:
                outcome = "win"
            elif my_result["roll"] > opponent_roll:
                outcome = "lose"
            else:
                outcome = "draw"
        
        return {
            "success": True,
            "outcome": outcome,
            "my_roll": {
                "skill": my_skill,
                "roll": my_result["roll"],
                "target": my_result["target"],
                "level": my_level,
                "description": my_result["description"]
            },
            "opponent_roll": {
                "roll": opponent_roll,
                "target": opponent_skill_full,
                "level": opponent_level,
                "description": opponent_desc
            }
        }
    
    # Sistema de saúde e dano
    def get_health_status(self) -> Dict[str, Any]:
        """
        Retorna informações completas sobre o estado de saúde do personagem.
        
        Returns:
            Dicionário com informações de saúde
        """
        damage_taken = self._sheet["status"]["damage_taken"]
        damage_levels = self._sheet["status"]["damage_levels"]
        
        # Determinar nível de dano atual
        if damage_taken >= len(damage_levels):
            current_level = "Impaired"
            level_index = len(damage_levels) - 1
        else:
            current_level = damage_levels[damage_taken]
            level_index = damage_taken
        
        return {
            "damage_taken": damage_taken,
            "current_level": current_level,
            "level_index": level_index,
            "damage_levels": damage_levels.copy(),
            "is_alive": current_level != "Impaired",
            "is_healthy": damage_taken == 0,
            "max_damage": len(damage_levels) - 1
        }
    
    def is_alive(self) -> bool:
        """
        Verifica se o personagem está vivo (não Impaired).
        
        Returns:
            True se vivo, False se Impaired
        """
        return self.get_health_status()["is_alive"]
    
    def take_damage(self, amount: int) -> Dict[str, Any]:
        """
        Aplica dano ao personagem e atualiza seu status.
        
        Args:
            amount: Quantidade de dano a ser aplicada
            
        Returns:
            Dicionário com resultado da aplicação de dano
        """
        if not isinstance(amount, int) or amount < 0:
            return {
                "success": False,
                "error": "Quantidade de dano deve ser um inteiro não negativo",
                "damage_applied": 0
            }
        
        # Estado anterior
        old_status = self.get_health_status()
        
        # Aplicar dano
        self._sheet["status"]["damage_taken"] += amount
        
        # Estado atual
        new_status = self.get_health_status()
        
        # Verificar se morreu
        died = old_status["is_alive"] and not new_status["is_alive"]
        
        return {
            "success": True,
            "damage_applied": amount,
            "old_level": old_status["current_level"],
            "new_level": new_status["current_level"],
            "total_damage": new_status["damage_taken"],
            "died": died,
            "is_alive": new_status["is_alive"]
        }
    
    def heal_damage(self, amount: int) -> Dict[str, Any]:
        """
        Cura dano do personagem.
        
        Args:
            amount: Quantidade de dano a ser curada
            
        Returns:
            Dicionário com resultado da cura
        """
        if not isinstance(amount, int) or amount < 0:
            return {
                "success": False,
                "error": "Quantidade de cura deve ser um inteiro não negativo",
                "damage_healed": 0
            }
        
        # Estado anterior
        old_status = self.get_health_status()
        
        # Aplicar cura (não pode ficar negativo)
        old_damage = self._sheet["status"]["damage_taken"]
        actual_heal = min(amount, old_damage)
        self._sheet["status"]["damage_taken"] = max(0, old_damage - amount)
        
        # Estado atual
        new_status = self.get_health_status()
        
        return {
            "success": True,
            "damage_healed": actual_heal,
            "old_level": old_status["current_level"],
            "new_level": new_status["current_level"],
            "total_damage": new_status["damage_taken"],
            "fully_healed": new_status["is_healthy"]
        }
    
    # Sistema de modificadores temporários
    def get_modifiers(self) -> List[Dict[str, Any]]:
        """
        Retorna lista de modificadores ativos.
        
        Returns:
            Lista de modificadores
        """
        return self._sheet["status"]["modifiers"].copy()
    
    def add_modifier(self, skill: str, modifier_type: str, duration: int) -> Dict[str, Any]:
        """
        Adiciona um modificador temporário a uma habilidade.
        
        Args:
            skill: Nome da habilidade
            modifier_type: Tipo do modificador ("bonus_dice" ou "penalty_dice")
            duration: Duração em número de usos
            
        Returns:
            Dicionário com resultado da operação
        """
        if modifier_type not in ["bonus_dice", "penalty_dice"]:
            return {
                "success": False,
                "error": "Tipo de modificador deve ser 'bonus_dice' ou 'penalty_dice'"
            }
        
        if not isinstance(duration, int) or duration <= 0:
            return {
                "success": False,
                "error": "Duração deve ser um inteiro positivo"
            }
        
        # Adicionar modificador
        modifier = {
            "skill": skill,
            "type": modifier_type,
            "duration": duration
        }
        
        self._sheet["status"]["modifiers"].append(modifier)
        
        return {
            "success": True,
            "modifier": modifier,
            "total_modifiers": len(self._sheet["status"]["modifiers"])
        }
    
    def check_skill_modifiers(self, skill_name: str, skill_type: str = "common") -> Dict[str, bool]:
        """
        Verifica se uma habilidade tem modificadores ativos.
        
        Args:
            skill_name: Nome da habilidade
            skill_type: Tipo da habilidade
            
        Returns:
            Dicionário com status dos modificadores
        """
        modifiers = self._sheet["status"]["modifiers"]
        
        has_bonus = any(
            mod.get("skill") == skill_name and mod.get("type") == "bonus_dice"
            for mod in modifiers if isinstance(mod, dict)
        )
        
        has_penalty = any(
            mod.get("skill") == skill_name and mod.get("type") == "penalty_dice"
            for mod in modifiers if isinstance(mod, dict)
        )
        
        return {
            "has_bonus": has_bonus,
            "has_penalty": has_penalty,
            "net_bonus": has_bonus and not has_penalty,
            "net_penalty": has_penalty and not has_bonus,
            "cancelled": has_bonus and has_penalty
        }
    
    def reduce_modifier_duration(self, skill_name: str, modifier_type: str) -> Dict[str, Any]:
        """
        Reduz a duração de um modificador específico.
        
        Args:
            skill_name: Nome da habilidade
            modifier_type: Tipo do modificador
            
        Returns:
            Dicionário com resultado da operação
        """
        modifiers = self._sheet["status"]["modifiers"]
        found = False
        
        for i, mod in enumerate(modifiers):
            if (isinstance(mod, dict) and 
                mod.get("skill") == skill_name and 
                mod.get("type") == modifier_type):
                
                mod["duration"] -= 1
                found = True
                
                # Remove se duração chegou a 0
                if mod["duration"] <= 0:
                    modifiers.pop(i)
                    return {
                        "success": True,
                        "modifier_removed": True,
                        "remaining_duration": 0
                    }
                else:
                    return {
                        "success": True,
                        "modifier_removed": False,
                        "remaining_duration": mod["duration"]
                    }
        
        return {
            "success": False,
            "error": f"Modificador {modifier_type} para {skill_name} não encontrado"
        }
    
    def clear_modifiers(self, skill_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Remove modificadores. Se skill_name for None, remove todos.
        
        Args:
            skill_name: Nome da habilidade (opcional)
            
        Returns:
            Dicionário com resultado da operação
        """
        if skill_name is None:
            # Remove todos os modificadores
            count = len(self._sheet["status"]["modifiers"])
            self._sheet["status"]["modifiers"] = []
            return {
                "success": True,
                "modifiers_removed": count,
                "skill": "all"
            }
        else:
            # Remove modificadores de uma habilidade específica
            modifiers = self._sheet["status"]["modifiers"]
            original_count = len(modifiers)
            
            self._sheet["status"]["modifiers"] = [
                mod for mod in modifiers 
                if not (isinstance(mod, dict) and mod.get("skill") == skill_name)
            ]
            
            removed_count = original_count - len(self._sheet["status"]["modifiers"])
            
            return {
                "success": True,
                "modifiers_removed": removed_count,
                "skill": skill_name
            }
    
    # Sistema de efeitos
    def apply_effect(self, effect: Dict[str, Any]) -> Dict[str, Any]:
        """
        Aplica um único efeito ao personagem.
        
        Args:
            effect: Dicionário com o efeito a ser aplicado
            
        Returns:
            Dicionário com resultado da aplicação do efeito
        """
        if not isinstance(effect, dict):
            return {
                "success": False,
                "error": f"Efeito deve ser um dicionário, recebido: {type(effect)}"
            }
        
        action = effect.get("action")
        if not action:
            return {
                "success": False,
                "error": f"Efeito sem campo 'action': {effect}"
            }
        
        # Processar cada tipo de ação
        if action == "take_damage":
            amount = effect.get("amount", 0)
            return self.take_damage(amount)
            
        elif action == "heal_damage":
            amount = effect.get("amount", 0)
            return self.heal_damage(amount)
            
        elif action == "spend_luck":
            amount = effect.get("amount", 0)
            return self.spend_luck(amount)
            
        elif action == "spend_magic":
            amount = effect.get("amount", 0)
            return self.spend_magic(amount)
            
        elif action == "gain_skill":
            skill_name = effect.get("skill")
            if not skill_name or not isinstance(skill_name, str):
                return {
                    "success": False,
                    "error": f"Nome de skill inválido: {skill_name}"
                }
            
            # Adicionar skill se não existir (valor padrão 60/30)
            skill_type = effect.get("skill_type", "common")
            if skill_type not in self._sheet["skills"]:
                skill_type = "common"  # fallback
                
            if skill_name not in self._sheet["skills"][skill_type]:
                self._sheet["skills"][skill_type][skill_name] = {
                    "full": 60,
                    "half": 30
                }
                
                return {
                    "success": True,
                    "action": action,
                    "skill": skill_name,
                    "skill_type": skill_type,
                    "value": 60,
                    "message": f"Gained skill {skill_name} at 60%"
                }
            else:
                return {
                    "success": True,
                    "action": action,
                    "skill": skill_name,
                    "message": f"Skill {skill_name} already exists"
                }
                
        elif action == "apply_penalty":
            skill_name = effect.get("skill", "General")
            duration = effect.get("duration", 1)
            return self.add_modifier(skill_name, "penalty_dice", duration)
            
        elif action == "apply_bonus":
            skill_name = effect.get("skill", "General")
            duration = effect.get("duration", 1)
            return self.add_modifier(skill_name, "bonus_dice", duration)
            
        elif action == "restore_luck":
            amount = effect.get("amount", 0)
            return self.restore_luck(amount)
            
        elif action == "restore_magic":
            amount = effect.get("amount", 0)
            return self.restore_magic(amount)
            
        elif action == "set_characteristic":
            char_name = effect.get("characteristic")
            value = effect.get("value")
            if not char_name or value is None:
                return {
                    "success": False,
                    "error": "set_characteristic requer 'characteristic' e 'value'"
                }
            return self.set_characteristic(char_name, value)
            
        elif action == "set_skill":
            skill_name = effect.get("skill")
            value = effect.get("value")
            skill_type = effect.get("skill_type", "common")
            if not skill_name or value is None:
                return {
                    "success": False,
                    "error": "set_skill requer 'skill' e 'value'"
                }
            return self.set_skill(skill_name, value, skill_type)
            
        elif action == "add_inventory":
            item = effect.get("item")
            if not item:
                return {
                    "success": False,
                    "error": "add_inventory requer 'item'"
                }
            
            # Garantir que o inventário existe e tem a estrutura correta
            if "inventory" not in self._sheet:
                self._sheet["inventory"] = {"equipment": [], "weapons": []}
            elif isinstance(self._sheet["inventory"], list):
                # Converter lista antiga para nova estrutura
                old_items = self._sheet["inventory"]
                self._sheet["inventory"] = {"equipment": old_items, "weapons": []}
            
            # Determinar categoria (default equipment)
            category = effect.get("category", "equipment")
            if category not in ["equipment", "weapons"]:
                category = "equipment"
            
            self._sheet["inventory"][category].append(item)
            return {
                "success": True,
                "action": action,
                "item": item,
                "category": category,
                "message": f"Added {item} to {category}"
            }
            
        elif action == "remove_inventory":
            item = effect.get("item")
            if not item:
                return {
                    "success": False,
                    "error": "remove_inventory requer 'item'"
                }
            
            inventory = self._sheet.get("inventory", {"equipment": [], "weapons": []})
            
            # Procurar em ambas as categorias
            for category in ["equipment", "weapons"]:
                if category in inventory and item in inventory[category]:
                    inventory[category].remove(item)
                    return {
                        "success": True,
                        "action": action,
                        "item": item,
                        "category": category,
                        "message": f"Removed {item} from {category}"
                    }
            
            return {
                "success": False,
                "error": f"Item {item} not found in inventory"
            }
        
        else:
            return {
                "success": False,
                "error": f"Ação desconhecida '{action}' em efeito: {effect}"
            }
    
    def apply_effects(self, effects: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aplica uma lista de efeitos ao personagem.
        
        Args:
            effects: Lista de efeitos a serem aplicados
            
        Returns:
            Dicionário com resultado da aplicação dos efeitos
        """
        if not isinstance(effects, list):
            return {
                "success": False,
                "error": f"'effects' deve ser uma lista, recebido: {type(effects)}",
                "effects_applied": 0
            }
        
        results = []
        success_count = 0
        error_count = 0
        
        for i, effect in enumerate(effects):
            result = self.apply_effect(effect)
            results.append({
                "effect_index": i,
                "effect": effect,
                "result": result
            })
            
            if result.get("success", False):
                success_count += 1
            else:
                error_count += 1
        
        return {
            "success": error_count == 0,
            "effects_processed": len(effects),
            "effects_applied": success_count,
            "effects_failed": error_count,
            "results": results
        }
    
    def validate_effect(self, effect: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida um efeito sem aplicá-lo.
        
        Args:
            effect: Dicionário com o efeito a ser validado
            
        Returns:
            Dicionário com resultado da validação
        """
        if not isinstance(effect, dict):
            return {
                "valid": False,
                "error": f"Efeito deve ser um dicionário, recebido: {type(effect)}"
            }
        
        action = effect.get("action")
        if not action:
            return {
                "valid": False,
                "error": f"Efeito sem campo 'action': {effect}"
            }
        
        # Lista de ações válidas
        valid_actions = [
            "take_damage", "heal_damage", "spend_luck", "spend_magic",
            "gain_skill", "apply_penalty", "apply_bonus", "restore_luck",
            "restore_magic", "set_characteristic", "set_skill",
            "add_inventory", "remove_inventory"
        ]
        
        if action not in valid_actions:
            return {
                "valid": False,
                "error": f"Ação '{action}' não é válida. Ações válidas: {valid_actions}"
            }
        
        # Validações específicas por ação
        if action in ["take_damage", "heal_damage", "spend_luck", "spend_magic", "restore_luck", "restore_magic"]:
            amount = effect.get("amount")
            if amount is not None and (not isinstance(amount, (int, float)) or amount < 0):
                return {
                    "valid": False,
                    "error": f"Campo 'amount' deve ser um número não negativo, recebido: {amount}"
                }
        
        if action in ["gain_skill", "apply_penalty", "apply_bonus", "set_skill"]:
            skill = effect.get("skill")
            if not skill or not isinstance(skill, str):
                return {
                    "valid": False,
                    "error": f"Campo 'skill' deve ser uma string não vazia, recebido: {skill}"
                }
        
        if action == "set_characteristic":
            char = effect.get("characteristic")
            value = effect.get("value")
            if not char or not isinstance(char, str):
                return {
                    "valid": False,
                    "error": f"Campo 'characteristic' deve ser uma string não vazia"
                }
            if value is None or not isinstance(value, (int, float)):
                return {
                    "valid": False,
                    "error": f"Campo 'value' deve ser um número"
                }
        
        if action in ["add_inventory", "remove_inventory"]:
            item = effect.get("item")
            if not item or not isinstance(item, str):
                return {
                    "valid": False,
                    "error": f"Campo 'item' deve ser uma string não vazia"
                }
        
        return {
            "valid": True,
            "action": action,
            "message": f"Efeito '{action}' é válido"
        }
    
    # Sistema de inventário
    def get_inventory(self) -> Dict[str, List[str]]:
        """
        Retorna o inventário do personagem.
        
        Returns:
            Dicionário com listas de equipamentos e armas
        """
        inventory = self._sheet.get("inventory", {"equipment": [], "weapons": []})
        
        # Garantir compatibilidade com formato antigo
        if isinstance(inventory, list):
            return {"equipment": inventory.copy(), "weapons": []}
        
        return {
            "equipment": inventory.get("equipment", []).copy(),
            "weapons": inventory.get("weapons", []).copy()
        }
    
    def add_item(self, item: str, category: str = "equipment") -> Dict[str, Any]:
        """
        Adiciona um item ao inventário.
        
        Args:
            item: Nome do item a ser adicionado
            category: Categoria do item ("equipment" ou "weapons")
            
        Returns:
            Dicionário com resultado da operação
        """
        if not isinstance(item, str) or not item.strip():
            return {
                "success": False,
                "error": "Item deve ser uma string não vazia"
            }
        
        if category not in ["equipment", "weapons"]:
            category = "equipment"
        
        # Garantir que o inventário existe
        if "inventory" not in self._sheet:
            self._sheet["inventory"] = {"equipment": [], "weapons": []}
        elif isinstance(self._sheet["inventory"], list):
            # Converter lista antiga para nova estrutura
            old_items = self._sheet["inventory"]
            self._sheet["inventory"] = {"equipment": old_items, "weapons": []}
        
        if category not in self._sheet["inventory"]:
            self._sheet["inventory"][category] = []
        
        self._sheet["inventory"][category].append(item)
        
        return {
            "success": True,
            "item": item,
            "category": category,
            "inventory_size": len(self._sheet["inventory"][category])
        }
    
    def remove_item(self, item: str, category: Optional[str] = None) -> Dict[str, Any]:
        """
        Remove um item do inventário.
        
        Args:
            item: Nome do item a ser removido
            category: Categoria específica ou None para buscar em todas
            
        Returns:
            Dicionário com resultado da operação
        """
        if not isinstance(item, str) or not item.strip():
            return {
                "success": False,
                "error": "Item deve ser uma string não vazia"
            }
        
        inventory = self._sheet.get("inventory", {"equipment": [], "weapons": []})
        
        if isinstance(inventory, list):
            # Compatibilidade com formato antigo
            if item in inventory:
                inventory.remove(item)
                return {
                    "success": True,
                    "item": item,
                    "category": "equipment",
                    "inventory_size": len(inventory)
                }
        else:
            # Buscar na categoria específica ou em todas
            categories = [category] if category else ["equipment", "weapons"]
            
            for cat in categories:
                if cat in inventory and item in inventory[cat]:
                    inventory[cat].remove(item)
                    return {
                        "success": True,
                        "item": item,
                        "category": cat,
                        "inventory_size": len(inventory[cat])
                    }
        
        return {
            "success": False,
            "error": f"Item '{item}' não encontrado no inventário"
        }
    
    def has_item(self, item: str, category: Optional[str] = None) -> bool:
        """
        Verifica se o personagem possui um item.
        
        Args:
            item: Nome do item a ser verificado
            category: Categoria específica ou None para buscar em todas
            
        Returns:
            True se possui o item, False caso contrário
        """
        inventory = self._sheet.get("inventory", {"equipment": [], "weapons": []})
        
        if isinstance(inventory, list):
            # Compatibilidade com formato antigo
            return item in inventory
        
        # Buscar na categoria específica ou em todas
        categories = [category] if category else ["equipment", "weapons"]
        
        for cat in categories:
            if cat in inventory and item in inventory[cat]:
                return True
        
        return False
    
    def __repr__(self) -> str:
        """Representação string do personagem."""
        return f"Character(name='{self.name}', occupation='{self.occupation}', health='{self.get_health_status()}')"
    
    def __str__(self) -> str:
        """String amigável do personagem."""
        luck = self.get_luck()
        magic = self.get_magic_points()
        return (f"{self.name} ({self.occupation})\n"
                f"Health: {self.get_health_status()}\n"
                f"Luck: {luck['current']}/{luck['starting']}\n"
                f"Magic: {magic['current']}/{magic['starting']}")
    
    # Métodos de gerenciamento de histórico
    def add_to_history(self, page_number: int, page_text: str, choice_made: Dict[str, Any], choice_index: int = None):
        """
        Adiciona uma entrada ao histórico de decisões.
        
        Args:
            page_number: Número da página onde a decisão foi tomada
            page_text: Texto da página onde a decisão foi tomada
            choice_made: Objeto choice completo que foi escolhido
            choice_index: Índice da escolha (opcional)
        """
        history_entry = {
            'page_number': page_number,
            'page_text': page_text,
            'choice_made': choice_made,
            'choice_index': choice_index
        }
        
        self._sheet['page_history'].append(history_entry)
    
    def get_history(self) -> List[Dict[str, Any]]:
        """
        Retorna o histórico de decisões.
        
        Returns:
            Lista com entradas do histórico
        """
        return self._sheet.get('page_history', [])
    
    def clear_history(self):
        """Limpa o histórico de decisões."""
        self._sheet['page_history'] = []


# Função de compatibilidade com código existente
def create_character_sheet():
    """
    Função de compatibilidade que cria uma ficha base.
    
    DEPRECATED: Use Character() diretamente.
    
    Returns:
        Dicionário com estrutura de ficha de personagem
    """
    temp_char = Character()
    return temp_char.sheet


# Função de compatibilidade com código existente
def setup_character(sheet, name, occupation, backstory):
    """
    Função de compatibilidade para setup de personagem.
    
    DEPRECATED: Use Character(name, occupation, backstory) diretamente.
    
    Args:
        sheet: Ficha de personagem (será modificada in-place)
        name: Nome do personagem
        occupation: Ocupação
        backstory: História de fundo
        
    Returns:
        Ficha modificada
    """
    # Criar Character temporário para aplicar setup
    temp_char = Character(name, occupation, 30, backstory)
    
    # Copiar dados para a sheet existente
    sheet.update(temp_char.sheet)
    return sheet


# Exemplo de uso e teste
if __name__ == "__main__":
    print("=== TESTE DA CLASSE CHARACTER ===\n")
    
    # Criar personagem policial
    detective = Character("Detective Smith", "Police Officer", 35, 
                         "Um veterano da força policial especializado em casos paranormais.")
    
    print("1. Personagem criado:")
    print(detective)
    print()
    
    # Testar acesso às características
    print("2. Características:")
    for char_name in ["STR", "DEX", "INT", "POW"]:
        char_data = detective.get_characteristic(char_name)
        print(f"   {char_name}: {char_data['full']} (Half: {char_data['half']})")
    print()
    
    # Testar acesso às habilidades
    print("3. Algumas habilidades:")
    skills_to_test = [
        ("Social", "common"),
        ("Observation", "common"), 
        ("Fighting", "combat")
    ]
    for skill, skill_type in skills_to_test:
        try:
            skill_data = detective.get_skill(skill, skill_type)
            print(f"   {skill}: {skill_data['full']}% (Half: {skill_data['half']}%)")
        except KeyError:
            print(f"   {skill}: Não encontrada em {skill_type} skills")
    print()
    
    # Testar habilidades expert
    print("4. Habilidades Expert:")
    for expert_skill, skill_data in detective.sheet["skills"]["expert"].items():
        print(f"   {expert_skill}: {skill_data['full']}% (Half: {skill_data['half']}%)")
    print()
    
    # Testar sistema de recursos
    print("5. Sistema de Recursos:")
    luck = detective.get_luck()
    magic = detective.get_magic_points()
    print(f"   Luck inicial: {luck['current']}/{luck['starting']}")
    print(f"   Magic inicial: {magic['current']}/{magic['starting']}")
    
    # Definir pontos de magia para o teste
    detective.set_magic_points(10)
    magic_after = detective.get_magic_points()
    print(f"   Magic após set_magic_points(10): {magic_after['current']}/{magic_after['starting']}")
    
    # Testar gastos de recursos
    print(f"   Pode gastar 3 luck? {detective.can_spend_luck(3)}")
    print(f"   Pode gastar 50 luck? {detective.can_spend_luck(50)}")
    
    if detective.spend_luck(5):
        luck_after = detective.get_luck()
        print(f"   Após gastar 5 luck: {luck_after['current']}/{luck_after['starting']}")
    
    if detective.spend_magic(3):
        magic_after = detective.get_magic_points()
        print(f"   Após gastar 3 magic: {magic_after['current']}/{magic_after['starting']}")
    
    # Testar restauração
    detective.restore_luck(2)
    detective.restore_magic(1)
    luck_restored = detective.get_luck()
    magic_restored = detective.get_magic_points()
    print(f"   Após restaurar (2 luck, 1 magic): Luck {luck_restored['current']}, Magic {magic_restored['current']}")
    print()
    
    # Testar modificação de características e habilidades
    print("6. Modificação de valores:")
    original_str = detective.get_characteristic("STR")
    print(f"   STR original: {original_str['full']}")
    
    detective.set_characteristic("STR", 75)
    new_str = detective.get_characteristic("STR")
    print(f"   STR após set_characteristic(75): {new_str['full']} (Half: {new_str['half']})")
    
    detective.set_skill("Athletics", 80, "common")
    athletics = detective.get_skill("Athletics", "common")
    print(f"   Athletics após set_skill(80): {athletics['full']}% (Half: {athletics['half']}%)")
    print()
    
    # Testar compatibilidade com funções antigas
    print("7. Teste de compatibilidade:")
    old_sheet = create_character_sheet()
    old_sheet = setup_character(old_sheet, "Agent Test", "Nurse", "Enfermeiro experiente")
    print(f"   Nome via função antiga: {old_sheet['info']['name']}")
    print(f"   Ocupação via função antiga: {old_sheet['info']['occupation']}")
    print()
    
    print("=== TESTE CONCLUÍDO ===")

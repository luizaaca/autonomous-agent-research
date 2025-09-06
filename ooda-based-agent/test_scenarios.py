import random
import pages

# Functions from the notebook

def create_character_sheet():
    """Cria um template para a ficha de personagem."""
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
            "damage_levels": ["Healthy", "Hurt", "Bloodied", "Down", "Impaired"], #0 for healthy, 1 for Hurt, 2 for Bloodied, 3 for Down, 4 for Impaired
            "damage_taken": 0,
            "modifiers": []  # e.g., {"skill": "Fighting", "type": "penalty_dice", "duration": "scene"}
        },
        "inventory": {"equipment": [], "weapons": []},
        "page_history": []
    }

def setup_character(sheet, name, occupation, backstory):
    """Configura a ficha de personagem com base na ocupação e história."""
    sheet["info"]["name"] = name
    sheet["info"]["occupation"] = occupation
    sheet["info"]["backstory"] = backstory

    # Define a sorte inicial do personagem
    luck_roll = random.randint(1, 10) + random.randint(1, 10) + 50
    sheet["resources"]["luck"]["starting"] = luck_roll
    sheet["resources"]["luck"]["current"] = luck_roll

    # Define os pontos full e half das características como DEX, INT, POW
    sheet["characteristics"]["DEX"]["full"] = random.randint(1, 10) + 50
    sheet["characteristics"]["DEX"]["half"] = sheet["characteristics"]["DEX"]["full"] // 2
    sheet["characteristics"]["INT"]["full"] = random.randint(1, 10) + 50
    sheet["characteristics"]["INT"]["half"] = sheet["characteristics"]["INT"]["full"] // 2
    sheet["characteristics"]["POW"]["full"] = random.randint(1, 10) + 50
    sheet["characteristics"]["POW"]["half"] = sheet["characteristics"]["POW"]["full"] // 2

    # Ajusta as perícias com base na ocupação
    if occupation == "Police Officer":
        for skill in ["Law", "Social", "Athletics", "Fighting"]:
            if skill in sheet["skills"]["common"]:
                sheet["skills"]["common"][skill] = {"full": 60, "half": 30}
        sheet["skills"]["expert"]["Magic"] = {"full": 60, "half": 30}
        sheet["skills"]["expert"]["Law"] = {"full": 60, "half": 30}
    elif occupation == "Social Worker":
        for skill in ["Observation", "Research", "Social"]:
            if skill in sheet["skills"]["common"]:
                sheet["skills"]["common"][skill] = {"full": 60, "half": 30}
        sheet["skills"]["expert"]["Magic"] = {"full": 60, "half": 30}
    elif occupation == "Nurse":
        for skill in ["Observation", "Read Person", "Social"]:
            if skill in sheet["skills"]["common"]:
                sheet["skills"]["common"][skill] = {"full": 60, "half": 30}
        sheet["skills"]["expert"]["Medicine"] = {"full": 60, "half": 30}
        sheet["skills"]["expert"]["Magic"] = {"full": 60, "half": 30}

    return sheet

def make_check(target_value, half_value, bonus_dice=False, penalty_dice=False):
    """Realiza um teste de perícia D100 e retorna o nível de sucesso numérico."""
    tens_roll_1 = random.randint(0, 9) * 10
    tens_roll_2 = random.randint(0, 9) * 10
    units_roll = random.randint(1, 10)

    # Um dado de bônus e um dado de penalidade se anulam.
    if bonus_dice and penalty_dice:
        bonus_dice = False
        penalty_dice = False

    if bonus_dice:
        final_tens = min(tens_roll_1, tens_roll_2)
        print("Applied bonus die.")
    elif penalty_dice:
        final_tens = max(tens_roll_1, tens_roll_2)
        print("Applied penalty die.")
    else:
        final_tens = tens_roll_1

    # Calcula o resultado final da rolagem
    if final_tens == 0 and units_roll == 10:
        final_roll = 100
    elif final_tens == 0:
        final_roll = units_roll
    else:
        final_roll = final_tens + (units_roll % 10)

    # Determina o nível de sucesso
    if final_roll == 1:
        return (5, final_roll)  # Critical Success
    if final_roll == 100:
        return (1, final_roll)  # Fumble
    if final_roll <= half_value:
        return (4, final_roll)  # Hard Success
    if final_roll <= target_value:
        return (3, final_roll)  # Success
    
    return (2, final_roll)  # Failure

# Agent Class from the notebook

class Agent:
    def __init__(self, name, occupation, game_instructions, game_data):
        base_sheet = create_character_sheet()
        self.sheet = setup_character(base_sheet, name, occupation, game_instructions.get_backstory())
        self.game_data = game_data
        self.current_page = 1
        self.combat_status = {}

    def __repr__(self):
        return f"Agent(Name: {self.sheet['info']['name']}, Occupation: {self.sheet['info']['occupation']})"

    def _validate_choices(self, choices):
        """Valida se a lista de choices está em formato correto."""
        if not isinstance(choices, list):
            print(f"ERRO CRÍTICO: 'choices' deve ser uma lista, recebido: {type(choices)}")
            return False
        
        if len(choices) == 0:
            print("ERRO: Lista de choices está vazia.")
            return False
        
        for i, choice in enumerate(choices):
            if not isinstance(choice, dict):
                print(f"ERRO: Choice {i} deve ser um dicionário, recebido: {type(choice)}")
                return False
        
        return True

    def _llm_decide(self, choices):
        """
        Decide qual ação tomar com base nas opções e no estado do agente.
        Esta versão usa uma lógica puramente declarativa baseada no campo 'requires'
        e também trata escolhas condicionais baseadas na ocupação.
        Inclui validações robustas para prevenir problemas com dados corrompidos.
        """
        # VALIDAÇÃO CRÍTICA: Verificar se choices está em formato válido
        if not self._validate_choices(choices):
            print("ERRO CRÍTICO: Lista de choices inválida. Usando ação de fallback.")
            raise Exception("Invalid choices format")
        
        choosen_choice = None
        
        try:
            for choice in choices:
                # Validação individual da choice
                if not isinstance(choice, dict):
                    print(f"AVISO: Choice inválida (não é dicionário): {choice}. Pulando.")
                    continue
                
                # Trata escolhas condicionais (estrutura especial com conditional_on)
                if "conditional_on" in choice:
                    if choice["conditional_on"] == "occupation":
                        paths = choice.get("paths")
                        occupation = self.sheet["info"]["occupation"] or "default"

                        print(f"Conditions Applied: Path choices based on occupation: {paths} for occupation {occupation}")
                        if not isinstance(paths, dict):
                            print(f"ERRO: 'paths' deve ser um dicionário: {paths}.")
                            raise Exception("Invalid paths format")
                
                        # Verifica se há um caminho específico para a ocupação atual
                        if occupation in paths:
                            selected_path = paths[occupation]
                            print(f"Agente decidiu com base na ocupação ({occupation}): {selected_path}")
                            choosen_choice = selected_path
                        # Usa o caminho padrão se não houver específico
                        elif "default" in paths:
                            selected_path = paths["default"]
                            print(f"Agente decidiu pelo caminho padrão da ocupação: {selected_path}")
                            choosen_choice = selected_path
                        else:
                            print(f"AVISO: Nenhum caminho válido para ocupação '{occupation}' e sem caminho padrão.")
                            raise Exception("No valid path for occupation and no default path")
                if choosen_choice:
                    return choosen_choice
                
                # Validar se a choice padrão tem campos mínimos necessários
                if not any(field in choice for field in ["goto", "roll", "opposed_roll", "luck_roll"]):
                    raise Exception("Choice inválida: campos obrigatórios ausentes.")

                # Há opção de definir ocupação, definir com base na ficha. Alterar futuramente para apenas validar escolha do llm, ou seja, se escolha está na lista fornecida.
                if "set-occupation" in choice:
                    if choice["set-occupation"] == self.sheet["info"]["occupation"]:
                        print(f"Agente decidiu pela opção de definir ocupação já existente: {choice}")
                        return choice
                    else:
                        print(f"AVISO: Opção de definir ocupação não corresponde à ocupação atual. Pulando choice: {choice}")
                        continue

                if "requires" in choice:
                    # Avalia as condições em 'requires'
                    requires = choice.get("requires")
                    if not isinstance(requires, dict):
                        print(f"AVISO: 'requires' deve ser um dicionário: {requires}. Pulando choice.")
                        continue
            
                    conditions_met = True
                    for key, value in requires.items():
                        try:
                            # Condição de ocupação
                            if key == "occupation":
                                if not isinstance(value, str):
                                    print(f"AVISO: Valor de ocupação deve ser string: {value}")
                                    conditions_met = False
                                    break
                                if self.sheet["info"]["occupation"] != value:
                                    conditions_met = False
                                    break
                            # Condição de dano
                            elif key == "damage_taken":
                                if not isinstance(value, dict):
                                    print(f"AVISO: Condição damage_taken deve ser dicionário: {value}")
                                    conditions_met = False
                                    break
                                min_damage = value.get("min", 0)
                                max_damage = value.get("max", float('inf'))
                                if not isinstance(min_damage, (int, float)) or not isinstance(max_damage, (int, float)):
                                    print(f"AVISO: Valores min/max de damage_taken devem ser numéricos")
                                    conditions_met = False
                                    break
                                current_damage = self.sheet["status"]["damage_taken"]
                                if not (min_damage <= current_damage <= max_damage):
                                    conditions_met = False
                                    break
                            # Adicionar outras verificações de condição aqui, se necessário
                            else:
                                print(f"AVISO: Condição desconhecida '{key}' em requires. Ignorando.")
                        except Exception as e:
                            print(f"ERRO ao avaliar condição '{key}': {e}")
                            conditions_met = False
                            break
            
                    # Se todas as condições forem atendidas, escolhe esta opção
                    if conditions_met:
                        # Validar se a choice tem campos necessários antes de retornar
                        if any(field in choice for field in ["goto", "roll", "opposed_roll", "luck_roll"]):
                            print(f"Agente decidiu com base em pré-requisitos: {choice}")
                            return choice
                        else:
                            print(f"AVISO: Choice com pré-requisitos atendidos não tem ação válida: {choice}")
                
                if "goto" in choice and isinstance(choice["goto"], int) and choice["goto"] > 0:
                    # Marca como possível escolha padrão
                    if not choosen_choice:
                        choosen_choice = choice

                # Se nenhuma escolha com pré-requisitos foi satisfeita, usa a padrão
                if choosen_choice:
                    print(f"Agente decidiu pela opção: {choosen_choice}")
                    return choosen_choice
                
                # Se não há escolha padrão válida, pega a primeira choice da lista que tenha ação válida
                for choice in choices:
                    if isinstance(choice, dict) and any(field in choice for field in ["goto", "roll", "opposed_roll", "luck_roll"]):
                        print(f"Agente usando primeira choice válida como fallback: {choice}")
                        return choice
        except Exception as e:
            print(f"ERRO CRÍTICO durante decisão: {e}")
    
        # Fallback de segurança final
        print("ERRO: Nenhuma choice válida encontrada. Usando fallback de segurança.")
        return self._create_fallback_choice()

    def _process_effects(self, effects):
        """Processa uma lista de efeitos no estado do agente."""
        if not isinstance(effects, list):
            print(f"AVISO: 'effects' deve ser uma lista, recebido: {type(effects)}. Ignorando efeitos.")
            return
            
        for effect in effects:
            if not isinstance(effect, dict):
                print(f"AVISO: Efeito deve ser um dicionário, recebido: {type(effect)}. Pulando efeito.")
                continue
                
            action = effect.get("action")
            if not action:
                print(f"AVISO: Efeito sem campo 'action': {effect}. Pulando efeito.")
                continue
                
            if action == "spend_luck":
                amount = effect.get("amount", 0)
                if not isinstance(amount, (int, float)) or amount < 0:
                    print(f"AVISO: Quantidade de sorte inválida: {amount}. Usando 0.")
                    amount = 0
                luck_amount = self.sheet["resources"]["luck"]["current"]
                luck_amount = max(0, luck_amount - amount)
                self.sheet["resources"]["luck"]["current"] = luck_amount
                print(f"Spent {amount} luck. Current luck: {self.sheet['resources']['luck']['current']}")
            elif action == "gain_skill":
                skill = effect.get("skill")
                if not skill or not isinstance(skill, str):
                    print(f"AVISO: Nome de perícia inválido: {skill}. Pulando efeito.")
                    continue
                if skill not in self.sheet["skills"]["common"]:
                    self.sheet["skills"]["common"][skill] = {"full": 60, "half": 30}
                    print(f"Gained skill {skill}. Current level: {self.sheet['skills']['common'][skill]}")
            elif action == "spend_magic":
                amount = effect.get("amount", 0)
                if not isinstance(amount, (int, float)) or amount < 0:
                    print(f"AVISO: Quantidade de magia inválida: {amount}. Usando 0.")
                    amount = 0
                magic_amount = self.sheet["resources"]["magic_pts"]["current"]
                magic_amount = max(0, magic_amount - amount)
                self.sheet["resources"]["magic_pts"]["current"] = magic_amount
                print(f"Spent {amount} magic points. Current magic points: {self.sheet['resources']['magic_pts']['current']}")
            elif action == "apply_penalty":
                self.apply_penalty(effect)
            elif action == "heal_damage":
                self.heal_status(effect)
            elif action == "take_damage":
                self.take_damage(effect)
            else:
                print(f"AVISO: Ação desconhecida '{action}' em efeito: {effect}. Pulando efeito.")

    def _validate_choice(self, choice):
        """Valida se a choice retornada pelo LLM está em formato correto."""
        if not isinstance(choice, dict):
            print(f"ERRO CRÍTICO: Choice deve ser um dicionário, recebido: {type(choice)}")
            return False
        
        # Verifica se tem pelo menos um campo válido para ação
        valid_action_fields = ["goto", "roll", "opposed_roll", "luck_roll", "effects"]
        has_valid_action = any(field in choice for field in valid_action_fields)
        
        if not has_valid_action:
            print(f"ERRO: Choice não contém nenhum campo de ação válido: {choice}")
            return False
        
        # Validações específicas por tipo de ação
        if "goto" in choice:
            goto_value = choice["goto"]
            if not isinstance(goto_value, int) or goto_value < 0:
                print(f"ERRO: 'goto' deve ser um número inteiro positivo, recebido: {goto_value}")
                return False
        
        if "roll" in choice:
            roll_value = choice["roll"]
            if not isinstance(roll_value, (str, dict)):
                print(f"ERRO: 'roll' deve ser string ou dicionário, recebido: {type(roll_value)}")
                return False
            
            if isinstance(roll_value, dict) and "skill" not in roll_value:
                print(f"ERRO: 'roll' como dicionário deve ter campo 'skill': {roll_value}")
                return False
        
        if "results" in choice:
            results = choice["results"]
            if not isinstance(results, dict):
                print(f"ERRO: 'results' deve ser um dicionário, recebido: {type(results)}")
                return False
        
        return True

    def verify_conditions(self, choice, available_choices):
        """
        Verifica se a choice selecionada pelo LLM está de acordo com as condições
        de ocupação disponíveis na página atual.
        
        Args:
            choice: A choice selecionada pelo LLM
            available_choices: Lista de choices disponíveis na página atual
            
        Returns:
            bool: True se válida, False se inválida
        """
        # Verifica se há choices condicionais baseadas em ocupação
        conditional_choice = None
        for available_choice in available_choices:
            if isinstance(available_choice, dict) and available_choice.get("conditional_on") == "occupation":
                conditional_choice = available_choice
                break
        
        # Se não há choice condicional, a validação passa
        if not conditional_choice:
            return True
        
        # Obtém a ocupação atual do agente
        current_occupation = self.sheet["info"]["occupation"] or "default"
        
        # Obtém os paths disponíveis
        paths = conditional_choice.get("paths", {})
        if not isinstance(paths, dict):
            print(f"ERRO CRÍTICO: 'paths' deve ser um dicionário: {paths}")
            return False
        
        # Determina qual path deveria ser usado para esta ocupação
        expected_path = None
        if current_occupation in paths:
            expected_path = paths[current_occupation]
        elif "default" in paths:
            expected_path = paths["default"]
        else:
            print(f"ERRO CRÍTICO: Nenhum path válido para ocupação '{current_occupation}' e sem path padrão")
            return False

        # Valida se o expected_path é um dicionário        
        if not isinstance(expected_path, dict):
            print(f"ERRO CRÍTICO: Path esperado deve ser um dicionário: {expected_path}")
            return False

        # Verifica se ao menos um campo padrao esta presente no expected_path
        for field in ["goto", "roll", "opposed_roll", "luck_roll"]:
            if field in expected_path:
                print(f"Campo padrão encontrado em expected_path: {field}")
                break
        else:
            print(f"ERRO CRÍTICO: Nenhum campo padrão encontrado em expected_path: {expected_path}")
            return False

        # Compara os campos relevantes entre expected_path e choice, verificar goto dentro de results:
        #   'default': {'text': 'Tentar usar sua força de vontade (não-policial)', 'roll': 'POW', 'results': {'2': {'goto': 27}, '3': {'goto': 22}}}
        expected_has_goto = expected_path.get("goto") or any(i.get('goto') is not None for i in expected_path.get("results", {}).values())
        choice_has_goto = choice.get("goto") or any(i.get('goto') is not None for i in choice.get("results", {}).values())

        if not expected_has_goto or not choice_has_goto:
            print(f"ERRO CRÍTICO: 'goto' ausente em expected_path ou choice.")
            return False
            
        
        # Verifica outros campos relevantes se necessário
        for field in ["roll", "opposed_roll", "luck_roll"]:
            if field in expected_path and field in choice:
                if expected_path[field] != choice[field]:
                    print(f"ERRO DE VALIDAÇÃO: LLM seguiu path incorreto para ocupação '{current_occupation}'. "
                          f"Campo '{field}' esperado: {expected_path[field]}, Recebido: {choice[field]}")
                    return False
        
        return True

    def perform_action(self, choice):
        """
        Executa a ação decidida, aplicando efeitos e rolagens de dados.
        Inclui validações para prevenir problemas com respostas incorretas do LLM.
        """
        # VALIDAÇÃO CRÍTICA: Verificar se choice está em formato válido
        if not self._validate_choice(choice):
            print("ERRO CRÍTICO: Choice inválida recebida do LLM. Usando ação padrão de segurança.")
            # Ação de segurança: tentar navegar para página 1 ou manter página atual
            self.sheet["info"]["backstory"].append(f"\nViolação de escolha detectada: {choice}. Escolha opção válida!")
            return "Ação de segurança executada devido a choice inválida."
        
        # VALIDAÇÃO DE CONDIÇÕES: Verificar se o LLM seguiu o path correto para sua ocupação
        page_data = self.game_data.get(self.current_page, {})
        available_choices = page_data.get("choices", [])
        
        if not self.verify_conditions(choice, available_choices):
            print("ERRO: LLM violou condições de ocupação. Usando ação padrão de segurança.")
            # Adicionar mensagem no backstory do agente para registrar a violação
            self.sheet["info"]["backstory"].append(f"\nViolação de condições de ocupação detectada: {choice}")
            return "Ação de segurança executada devido a violação de condições de ocupação."
        
        outcome = choice.get("outcome", "")
        
        try:
            # 1. Aplicar efeitos imediatos da escolha
            if "effects" in choice:
                self._process_effects(choice["effects"])

            # 2. Executar rolagens de dados, se necessário
            if "roll" in choice:
                
                roll_data = choice["roll"]
                
                # Detectar se roll é uma string (formato simples) ou dicionário (formato complexo)
                if isinstance(roll_data, str):
                    # Formato simples: "roll": "Fighting"
                    skill_name = roll_data
                    difficulty = choice.get("difficulty", "normal")
                    bonus_dice = choice.get("bonus_dice", False)
                    penalty_dice = choice.get("penalty_dice", False)
                    results = choice.get("results", {})
                elif isinstance(roll_data, dict):
                    # Formato complexo: "roll": {"skill": "INT", "difficulty": "hard", ...}
                    skill_name = roll_data.get("skill")
                    difficulty = roll_data.get("difficulty", "normal")
                    bonus_dice = roll_data.get("bonus_dice", False)
                    penalty_dice = roll_data.get("penalty_dice", False)
                    results = roll_data.get("results", {})
                else:
                    print(f"ERRO: Formato de 'roll' inválido: {roll_data}. Usando valores padrão.")
                    self.sheet["info"]["backstory"].append(f"\nViolação de formato de roll detectada: {roll_data}. Use valores fornecidos.")
                    return "Ação de segurança executada devido a formato inválido de roll."

                # Validar skill_name
                if not skill_name or not isinstance(skill_name, str):
                    print(f"ERRO: Nome de perícia inválido: {skill_name}. Escolha uma perícia válida.'.")
                    self.sheet["info"]["backstory"].append(f"\nViolação de nome de perícia detectada: {skill_name}. Use perícia válida.")
                    return "Ação de segurança executada devido a perícia inválida."

                # Encontra a perícia na ficha do personagem
                skill_values = None
                if skill_name in self.sheet["skills"]["common"]:
                    skill_values = self.sheet["skills"]["common"][skill_name]
                elif skill_name in self.sheet["skills"]["combat"]:
                    skill_values = self.sheet["skills"]["combat"][skill_name]
                elif skill_name in self.sheet["skills"]["expert"]:
                    skill_values = self.sheet["skills"]["expert"][skill_name]
                else:
                    # Para características como INT, DEX, etc.
                    if skill_name in self.sheet["characteristics"]:
                        char_value = self.sheet["characteristics"][skill_name]["full"]
                        skill_values = {"full": char_value, "half": char_value // 2}
                    else:
                        print(f"Perícia '{skill_name}' não encontrada. Usando valores padrão.")
                        skill_values = {"full": 30, "half": 15}

                # Validar difficulty
                if difficulty not in ["normal", "hard"]:
                    print(f"AVISO: Dificuldade inválida '{difficulty}'. Usando 'normal'.")
                    difficulty = "normal"
                
                # valor padrão
                target_value = 33

                # Ajusta valores baseados na dificuldade
                if difficulty == "hard":
                    target_value = skill_values["half"]
                    half_value = target_value // 2
                else:  # normal
                    target_value = skill_values["full"]
                    half_value = skill_values["half"]

                print(f"Performing roll for skill '{skill_name}' with target {target_value} (difficulty: {difficulty})")
                
                # Validar bonus_dice e penalty_dice
                bonus_dice = bool(bonus_dice) if isinstance(bonus_dice, (bool, int)) else False
                penalty_dice = bool(penalty_dice) if isinstance(penalty_dice, (bool, int)) else False

                # Verifica se há penalidades ativas para esta perícia
                has_penalty = any(
                    mod.get("skill") == skill_name and mod.get("type") == "penalty_dice"
                    for mod in self.sheet["status"]["modifiers"] if isinstance(mod, dict)
                )

                has_bonus = any(
                    mod.get("skill") == skill_name and mod.get("type") == "bonus_dice"
                    for mod in self.sheet["status"]["modifiers"] if isinstance(mod, dict)
                )

                # Realiza o teste
                level, roll_value = make_check(target_value, half_value, bonus_dice=has_bonus, penalty_dice=has_penalty)
                print(f"Rolled {skill_name}: {roll_value} vs {target_value} -> Level {level}")

                # Processa os resultados baseados no nível de sucesso
                if not isinstance(results, dict):
                    print(f"ERRO: 'results' deve ser um dicionário: {results}")
                    results = {}
                
                result = results.get(str(level))
                
                if result:
                    # Para formato complexo, result pode ser um número (goto direto) ou dict com outcome/effects/goto
                    if isinstance(result, int):
                        # Resultado simples: apenas o número da página
                        if result > 0:  # Validar página válida
                            self.current_page = result
                            print(f"Navigating to page {result} based on roll result.")
                        else:
                            print(f"ERRO: Página inválida {result}. Mantendo página atual.")
                    elif isinstance(result, dict):
                        # Resultado complexo: contém outcome, effects, goto
                        outcome = result.get("outcome", outcome)
                        if "effects" in result:
                            self._process_effects(result["effects"])
                        if "goto" in result:
                            goto_page = result["goto"]
                            if isinstance(goto_page, int) and goto_page > 0:
                                self.current_page = goto_page
                                print(f"Navigating to page {goto_page} based on roll result.")
                            else:
                                print(f"ERRO: Página 'goto' inválida: {goto_page}. Mantendo página atual.")
                else:
                    print(f"AVISO: Nenhum resultado encontrado para nível {level}. Mantendo página atual.")
            
            # 2.5. Executar rolagens de sorte (luck_roll)
            elif "luck_roll" in choice and choice["luck_roll"]:
                # Usa o valor atual de sorte do personagem
                luck_value = self.sheet["resources"]["luck"]["current"]
                luck_half = luck_value // 2
                
                # Realiza o teste de sorte
                level, roll_value = make_check(luck_value, luck_half)
                
                # Processa o resultado da rolagem de sorte
                results = choice.get("results", {})
                if not isinstance(results, dict):
                    print(f"ERRO: 'results' para luck_roll deve ser um dicionário: {results}")
                    return outcome
                    
                result = results.get(str(level))
                if not result: # Fallback para o nível de sucesso mais próximo
                     for i in range(level - 1, 0, -1):
                        result = results.get(str(i))
                        if result:
                            break
                
                print(f"Rolled Luck: {roll_value} vs {luck_value} -> Level {level}")
                
                if result:
                    outcome = result.get("outcome", outcome)
                    if "effects" in result:
                        self._process_effects(result["effects"])
                    if "goto" in result:
                        goto_page = result["goto"]
                        if isinstance(goto_page, int) and goto_page > 0:
                            self.current_page = goto_page
                            print(f"Navigating to page {goto_page} based on luck roll.")
                        else:
                            print(f"ERRO: Página 'goto' inválida: {goto_page}. Mantendo página atual.")

            # 3. Opposed roll
            elif "opposed_roll" in choice:
                skill_to_roll = choice["opposed_roll"]
                if not isinstance(skill_to_roll, str):
                    print(f"ERRO: 'opposed_roll' deve ser uma string: {skill_to_roll}")
                    return outcome
                    
                opponent_skill = choice.get("opponent_skill", {"full": 30, "half": 15})
                if not isinstance(opponent_skill, dict):
                    print(f"ERRO: 'opponent_skill' deve ser um dicionário: {opponent_skill}")
                    opponent_skill = {"full": 30, "half": 15}
                    
                results = choice.get("outcomes", {})
                if not isinstance(results, dict):
                    print(f"ERRO: 'outcomes' deve ser um dicionário: {results}")
                    return outcome

                # Encontra a perícia na ficha do personagem
                skill_values = None
                if skill_to_roll in self.sheet["skills"]["common"]:
                    skill_values = self.sheet["skills"]["common"][skill_to_roll]
                elif skill_to_roll in self.sheet["skills"]["combat"]:
                    skill_values = self.sheet["skills"]["combat"][skill_to_roll]
                elif skill_to_roll in self.sheet["skills"]["expert"]:
                    skill_values = self.sheet["skills"]["expert"][skill_to_roll]
                else:
                    # Para características como INT, DEX, etc.
                    if skill_to_roll in self.sheet["characteristics"]:
                        char_value = self.sheet["characteristics"][skill_to_roll]["full"]
                        skill_values = {"full": char_value, "half": char_value // 2}
                    else:
                        print(f"Perícia '{skill_to_roll}' não encontrada. Usando valores padrão.")
                        skill_values = {"full": 30, "half": 15}

                target_value = skill_values["full"]
                half_value = skill_values["half"]

                # Verifica se há modificadores ativos para esta perícia
                has_penalty = any(
                    mod.get("skill") == skill_to_roll and mod.get("type") == "penalty_dice"
                    for mod in self.sheet["status"]["modifiers"] if isinstance(mod, dict)
                )

                has_bonus = any(
                    mod.get("skill") == skill_to_roll and mod.get("type") == "bonus_dice"
                    for mod in self.sheet["status"]["modifiers"] if isinstance(mod, dict)
                )

                # Realiza o teste do agente
                agent_level, agent_roll = make_check(target_value, half_value, bonus_dice=has_bonus, penalty_dice=has_penalty)
                print(f"Agente Rolled {skill_to_roll}: {agent_roll} vs {target_value} -> Level {agent_level}")

                # Realiza o teste do oponente
                opponent_level, opponent_roll = make_check(opponent_skill["full"], opponent_skill["half"])
                print(f"Oponente Rolled: {opponent_roll} vs {opponent_skill['full']} -> Level {opponent_level}")

                # Determina o resultado do confronto
                if agent_level > opponent_level:
                    result_key = "win"
                elif agent_level < opponent_level:
                    result_key = "lose"
                else:
                    result_key = "draw"
                
                if result_key in results:
                    result = results[result_key]
                    if isinstance(result, dict):
                        if "effects" in result:
                            self._process_effects(result["effects"])
                        if "goto" in result and isinstance(result["goto"], int) and result["goto"] > 0:
                            self.current_page = result["goto"]
                            print(f"{result_key.upper()}: Navigating to page {result['goto']}.")
                        outcome = result.get("outcome", outcome)
                    else:
                        print(f"ERRO: Resultado '{result_key}' deve ser um dicionário: {result}")

            # 4. Navegação direta (sem rolagem)
            elif "goto" in choice:
                goto_page = choice["goto"]
                if isinstance(goto_page, int) and goto_page > 0:
                    print(f"Navigating directly to page {goto_page}.")
                    self.current_page = goto_page
                else:
                    print(f"ERRO: Página 'goto' inválida: {goto_page}. Mantendo página atual.")
            
            else:
                print(f"AVISO: Nenhuma ação reconhecida na choice: {choice}")
                
        except Exception as e:
            print(f"ERRO CRÍTICO durante execução da ação: {e}")
            print(f"Choice problemática: {choice}")
            outcome = f"Erro durante execução: {str(e)}"
            
        return outcome

    def run(self):
        """
        Executa o ciclo OODA principal para navegar pelo livro-jogo.
        """
        while True:
            # 1. Observe
            page_text, choices = self._observe()
            if not choices:
                print("Fim da história (nenhuma escolha encontrada).")
                break
            
            # 2. Orient
            self._orient(page_text)
            
            # 3. Decide
            chosen_action = self._llm_decide(choices)
            print(f"Agente escolheu: {chosen_action}")        
            # 4. Act
            outcome = self.perform_action(chosen_action)
            print(f"Resultado: {outcome}\n---")
            # Condição de parada
            if self.current_page == 0:
                print("Fim da história (goto: 0).")
                break

    def _observe(self):
        """
        Observa o ambiente, lendo o texto e as opções da página atual.
        """
        page_data = self.game_data.get(self.current_page, {})
        page_text = page_data.get("text", "Página não encontrada.")
        choices = page_data.get("choices", [])
        
        damage = self.sheet["status"]["damage_taken"]
        if damage >= len(self.sheet["status"]["damage_levels"]):
            damage = len(self.sheet["status"]["damage_levels"]) - 1
        print(f"---" + f" Página: {self.current_page} --- Status: {self.sheet['status']['damage_levels'][damage]}\n")
        print(f"Page: {page_text}\n")
        print(f"Escolhas disponíveis: {choices}")
        return page_text, choices

    def _orient(self, page_text):
        """
        Orienta o agente, atualizando seu estado interno com base nas observações.
        """
        # Adiciona a página atual ao histórico
        if self.current_page not in self.sheet["page_history"]:
            self.sheet["page_history"].append((self.current_page, page_text))
        
        # Futuramente, poderia usar um LLM para extrair contexto do page_text
        pass

    def apply_penalty(self, effect):
        """Aplica uma penalidade a uma perícia."""
        skill = effect["skill"] # e.g., "Fighting"
        duration = effect["duration"] # e.g., 1 number of rolls    
        self.sheet["status"]["modifiers"].append((skill, "penalty_dice", duration))
        print(f"Applied penalty to {skill} for {duration}.")

    def heal_status(self, effect):
        """Cura um status ou dano."""
        status_to_heal = effect["amount"]
        self.sheet["status"]["damage_taken"] = max(0, self.sheet["status"]["damage_taken"] - status_to_heal)
        damage_level_map = self.sheet["status"]["damage_levels"]
        current_level = damage_level_map[self.sheet["status"]["damage_taken"]]
        print(f"Healed damage: {status_to_heal}. Total damage: {self.sheet['status']['damage_taken']}. Status: {current_level}")

    def take_damage(self, effect):
        """Aplica dano ao personagem e atualiza o status."""
        amount = effect.get("amount", 0)
        self.sheet["status"]["damage_taken"] += amount
        
        # Atualiza o nível de dano atual
        damage_level_map = self.sheet["status"]["damage_levels"]
        current_level_index = self.sheet["status"]["damage_taken"]

        if current_level_index >= len(damage_level_map):
            current_level = "Impaired"
            self.current_page = 999 # End game
        else:
            current_level = damage_level_map[current_level_index]

        print(f"Took {amount} damage. Total damage: {self.sheet['status']['damage_taken']}. Status: {current_level}")
        #se o level for Impaired, o jogo termina
        if current_level == "Impaired":
            print("Character is Impaired. Game Over.")
            self.current_page = 999


class GameInstructions:
    def get_backstory(self):
        return "Um oficial recém-formado na divisão de crimes especiais, conhecido por sua abordagem metódica."

class GameData:
    def __init__(self):
        self.pages = pages.PAGES
    
    def get(self, page_id, default=None):
        return self.pages.get(page_id, default)

if __name__ == "__main__":
    game_instructions = GameInstructions()
    game_data = GameData()

    input("Pressione Enter para iniciar o próximo cenário de teste...\n")
    # Scenario 1: Police Officer (default)
    print("---" + " Running Scenario 1: Police Officer " + "---")
    agent_police = Agent(
        name="Alex", 
        occupation="Police Officer", 
        game_instructions=game_instructions, 
        game_data=game_data
    )
    agent_police.run()
    print("---" + " Scenario 1 Finished " + "---\n")
    input("Pressione Enter para iniciar o próximo cenário de teste...\n")
    # Scenario 2: Social Worker
    print("---" + " Running Scenario 2: Social Worker " + "---")
    agent_social = Agent(
        name="Brenda", 
        occupation="Social Worker", 
        game_instructions=game_instructions, 
        game_data=game_data
    )
    agent_social.run()
    print("---" + " Scenario 2 Finished " + "---\n")

    input("Pressione Enter para iniciar o próximo cenário de teste...\n")
    # Scenario 3: Nurse
    print("---" + " Running Scenario 3: Nurse " + "---")
    agent_nurse = Agent(
        name="Charles", 
        occupation="Nurse", 
        game_instructions=game_instructions, 
        game_data=game_data
    )
    agent_nurse.run()
    print("---" + " Scenario 3 Finished " + "---\n")

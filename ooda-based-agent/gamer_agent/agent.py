from character import Character
from cockpit import GamePage
from decision_controller import DecisionController, DecisionContext
from default_decision_controller import DefaultDecisionController

class Agent:
    def __init__(self, name, occupation, game_instructions, game_data, decision_controller: DecisionController = None):
        # Refatorado para usar Character com backstory inteligente
        # game_instructions agora é opcional - Character tem get_game_backstory()
        if game_instructions and hasattr(game_instructions, 'get_backstory'):
            # Compatibilidade com código legado
            backstory = game_instructions.get_backstory()
        else:
            # Nova arquitetura - Character gerencia seu próprio backstory
            backstory = ""  # Será substituído por get_game_backstory()
        
        self.character = Character(name, occupation, 30, backstory)
        self.game_data = game_data
        self.current_page = 1
        self.combat_status = {}
        
        # Injeção de dependência para controlador de decisão
        self.decision_controller = decision_controller or DefaultDecisionController()
        
        # Criar instância da GamePage para visualização rica
        self.game_page = GamePage(self.character, game_data)

    @property
    def sheet(self):
        """Propriedade de compatibilidade para código que ainda acessa self.sheet"""
        return self.character.sheet

    def __repr__(self):
        return f"Agent(Name: {self.character.name}, Occupation: {self.character.occupation})"

    def _smart_truncate_text(self, text: str, max_chars: int = 200) -> str:
        """
        Trunca texto preservando palavras completas nos últimos N caracteres.
        
        Args:
            text: Texto a ser truncado
            max_chars: Número máximo de caracteres (padrão: 200)
            
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
        Refatorado para usar injeção de dependência com DecisionController.
        """
        # VALIDAÇÃO CRÍTICA: Verificar se choices está em formato válido
        if not self._validate_choices(choices):
            print("ERRO CRÍTICO: Lista de choices inválida. Usando ação de fallback.")
            raise Exception("Invalid choices format")
        
        # Criar contexto para o controller
        context = DecisionContext(self.character, self.game_data, self.current_page)
        
        # Delegar decisão para o controller injetado
        chosen_choice = self.decision_controller.decide(choices, context)
        
        # Exibir escolha formatada
        if chosen_choice:
            print("🎯 ESCOLHA DO MODELO (ESTRUTURADA):")
            print("=" * 50)
            for key, value in chosen_choice.items():
                print(f"  {key}: {value}")
            print("=" * 50)
        
        return chosen_choice
    #Não tem fallback deve ser reenviada para o agente decisorio novamente com historico atualizado
    def _create_fallback_choice(self):
        """Cria uma choice de segurança para situações de erro."""
        raise Exception("Fallback choice should not be used in this implementation.")

    def _process_effects(self, effects):
        """
        Processa uma lista de efeitos no estado do agente.
        Refatorado para usar character.apply_effects() ao invés de lógica manual.
        """
        if not isinstance(effects, list):
            print(f"AVISO: 'effects' deve ser uma lista, recebido: {type(effects)}. Ignorando efeitos.")
            return
        
        # Usar o método robusto da classe Character
        result = self.character.apply_effects(effects)
        
        # Log dos resultados para compatibilidade com comportamento anterior
        if result['success']:
            print(f"Aplicados {result['effects_applied']} efeitos com sucesso.")
            if result['effects_failed'] > 0:
                print(f"AVISO: {result['effects_failed']} efeitos falharam.")
        else:
            print(f"ERRO: Falha ao aplicar efeitos. {result['effects_failed']} efeitos falharam.")
        
        return result

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
        
        # Obtém a ocupação atual do agente (refatorado para usar Character)
        current_occupation = self.character.occupation or "default"
        
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
            print("ERRO CRÍTICO: Choice inválida recebida do LLM")
            raise ValueError(f"Choice inválida: {choice}")
        
        # VALIDAÇÃO DE CONDIÇÕES: Verificar se o LLM seguiu o path correto para sua ocupação
        page_data = self.game_data.get(self.current_page, {})
        available_choices = page_data.get("choices", [])
        
        if not self.verify_conditions(choice, available_choices):
            print("ERRO: LLM violou condições de ocupação")
            raise ValueError(f"Violação de condições de ocupação: {choice}")
        
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
                    print(f"ERRO: Formato de 'roll' inválido: {roll_data}")
                    raise ValueError(f"Formato de 'roll' inválido: {roll_data}. Deve ser string ou dicionário.")

                # Validar skill_name
                if not skill_name or not isinstance(skill_name, str):
                    print(f"ERRO: Nome de perícia inválido: {skill_name}")
                    raise ValueError(f"Nome de perícia inválido: {skill_name}. Deve ser uma string válida.")

                # Validar difficulty
                if difficulty not in ["normal", "hard"]:
                    print(f"AVISO: Dificuldade inválida '{difficulty}'. Usando 'normal'.")
                    difficulty = "normal"
                
                # Converter difficulty para formato da Character
                character_difficulty = "regular" if difficulty == "normal" else "hard"
                
                print(f"Performing roll for skill '{skill_name}' with difficulty: {difficulty}")
                
                # Validar bonus_dice e penalty_dice
                bonus_dice = bool(bonus_dice) if isinstance(bonus_dice, (bool, int)) else False
                penalty_dice = bool(penalty_dice) if isinstance(penalty_dice, (bool, int)) else False

                # Usar o método robusto da classe Character para rolagens
                roll_result = None
                try:
                    # Tentar como habilidade primeiro
                    for skill_type in ["common", "combat", "expert"]:
                        roll_result = self.character.roll_skill(
                            skill_name, skill_type, 
                            bonus_dice=bonus_dice, 
                            penalty_dice=penalty_dice,
                            difficulty=character_difficulty,
                            auto_apply_modifiers=True
                        )
                        if roll_result.get("success", False):
                            break
                    else:
                        # Se não encontrar como habilidade, tentar como característica
                        roll_result = self.character.roll_characteristic(
                            skill_name,
                            bonus_dice=bonus_dice,
                            penalty_dice=penalty_dice,
                            difficulty=character_difficulty
                        )
                        if not roll_result.get("success", False):
                            print(f"ERRO: '{skill_name}' não encontrado como habilidade ou característica.")
                            raise Exception(f"'{skill_name}' not found as skill or characteristic")
                    
                    # Verificar se roll_result foi bem-sucedido
                    if not roll_result.get("success", False):
                        print(f"ERRO: Failed to roll for '{skill_name}': {roll_result.get('error', 'Unknown error')}")
                        raise Exception(f"Failed to roll for '{skill_name}'")
                    
                    # Extrair informações do resultado
                    level = roll_result["level"]
                    roll_value = roll_result["roll"]
                    target_value = roll_result["target"]
                    
                    print(f"Rolled {skill_name}: {roll_value} vs {target_value} -> Level {level}")
                    
                except Exception as e:
                    print(f"ERRO na rolagem: {e}")
                    raise Exception(f"Erro na rolagem: {e}")

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
            
            # 2.5. Executar rolagens de sorte (luck_roll) - refatorado para usar Character
            elif "luck_roll" in choice and choice["luck_roll"]:
                try:
                    # Usar o método robusto da classe Character para rolagem de sorte
                    roll_result = self.character.roll_luck()
                    
                    # Extrair informações do resultado
                    level = roll_result["level"]
                    roll_value = roll_result["roll"]
                    luck_value = roll_result["target"]
                    
                    print(f"Rolled Luck: {roll_value} vs {luck_value} -> Level {level}")
                    
                except Exception as e:
                    print(f"ERRO na rolagem de sorte: {e}")
                    raise Exception(f"Erro na rolagem de sorte: {e}")
                
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

                # Usar o método robusto da classe Character para teste oposto
                roll_result = None
                try:
                    roll_result = self.character.opposed_roll(
                        skill_to_roll, 
                        "common",  # Tentar common primeiro
                        opponent_skill["full"],
                        opponent_skill["half"]
                    )
                    if not roll_result.get("success", False):
                        raise KeyError(f"Failed to roll {skill_to_roll} as common skill")
                except KeyError:
                    # Se não estiver em common, tentar combat
                    try:
                        roll_result = self.character.opposed_roll(
                            skill_to_roll, 
                            "combat",
                            opponent_skill["full"],
                            opponent_skill["half"]
                        )
                        if not roll_result.get("success", False):
                            raise KeyError(f"Failed to roll {skill_to_roll} as combat skill")
                    except KeyError:
                        # Se não estiver em combat, tentar expert
                        try:
                            roll_result = self.character.opposed_roll(
                                skill_to_roll, 
                                "expert",
                                opponent_skill["full"],
                                opponent_skill["half"]
                            )
                            if not roll_result.get("success", False):
                                raise KeyError(f"Failed to roll {skill_to_roll} as expert skill")
                        except KeyError:
                            print(f"ERRO: Perícia '{skill_to_roll}' não encontrada para teste oposto.")
                            raise KeyError(f"Perícia '{skill_to_roll}' não encontrada para teste oposto.")
                
                if not roll_result or not roll_result.get("success", False):
                    print(f"ERRO: Falha na rolagem oposta: {roll_result}")
                    raise Exception(f"Falha na rolagem oposta para {skill_to_roll}")
                
                # Extrair informações do resultado
                result_key = roll_result["outcome"]  # "win", "lose", "draw"
                agent_level = roll_result["my_roll"]["level"]
                agent_roll = roll_result["my_roll"]["roll"]
                opponent_level = roll_result["opponent_roll"]["level"]
                opponent_roll = roll_result["opponent_roll"]["roll"]
                
                print(f"Agente Rolled {skill_to_roll}: {agent_roll} -> Level {agent_level}")
                print(f"Oponente Rolled: {opponent_roll} -> Level {opponent_level}")
                print(f"Resultado: {result_key}")
                
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
            
            # 5. Record - Registrar escolha no histórico detalhado
            choice_index = None
            for i, choice in enumerate(choices):
                if choice == chosen_action:
                    choice_index = i
                    break
            
            self._record_choice_in_history(page_text, chosen_action, choice_index, outcome)
            
            # Condição de parada
            if self.current_page == 0:
                print("Fim da história (goto: 0).")
                break

    def _observe(self):
        """
        Observa o ambiente usando GamePage para visualização rica.
        Exibe o cockpit completo enviado ao modelo e retorna choices estruturadas.
        """
        # Configurar a página atual na GamePage
        self.game_page.set_current_page(self.current_page)
        
        # Gerar prompt rico usando GamePage
        prompt = self.game_page.generate_prompt()
        
        # Exibir visualização rica
        print("=" * 80)
        print("📱 COCKPIT ENVIADO AO MODELO:")
        print("=" * 80)
        print(prompt)
        print("=" * 80)
        
        # Obter dados da página atual
        page_data = self.game_data.get(self.current_page, {})
        page_text = page_data.get("text", "Página não encontrada.")
        choices = page_data.get("choices", [])
        
        # Exibir choices estruturadas
        print("🎯 CHOICES DISPONÍVEIS (ESTRUTURADAS):")
        for i, choice in enumerate(choices):
            print(f"  [{i+1}] {choice}")
        print("=" * 80)
        
        return page_text, choices

    def _orient(self, page_text):
        """
        Orienta o agente, atualizando seu estado interno com base nas observações.
        Integra com GamePage para histórico visual.
        """
        # Exibir progresso visual
        print("\n" + "=" * 80)
        print("📍 PROGRESSO DA NAVEGAÇÃO:")
        print(f"  Página atual: {self.current_page}")
        print(f"  Total de páginas visitadas: {len([entry for entry in self.sheet['page_history'] if isinstance(entry, tuple)])}")
        print("=" * 80 + "\n")
        # Futuramente, poderia usar um LLM para extrair contexto do page_text
        pass

    def _record_choice_in_history(self, page_text, chosen_choice, choice_index=None, outcome=None):
        """
        Registra a escolha feita no histórico detalhado usando Character.add_to_history().
        
        Args:
            page_text: Texto da página onde a escolha foi feita
            chosen_choice: Objeto choice escolhido
            choice_index: Índice da escolha (opcional)
            outcome: Resultado da ação executada (opcional)
        """
        # Criar choice expandida com resultado para o histórico
        choice_with_outcome = chosen_choice.copy()
        if outcome:
            choice_with_outcome['executed_outcome'] = outcome
        
        # Adicionar ao histórico detalhado via Character
        self.character.add_to_history(
            page_number=self.current_page,
            page_text=self._smart_truncate_text(page_text, 200),
            choice_made=choice_with_outcome,
            choice_index=choice_index
        )
        
        print("✅ ESCOLHA REGISTRADA NO HISTÓRICO DETALHADO")
        print(f"  Página: {self.current_page}")
        print(f"  Escolha: {chosen_choice.get('text', str(chosen_choice)[:50])}")
        if outcome:
            print(f"  Resultado: {outcome[:100]}...")

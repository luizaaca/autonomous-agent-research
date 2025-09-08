from character import Character
from cockpit import Cockpit
from player_input_adapter import PlayerInputAdapter
from typing import Dict, Any

class Agent:
    def __init__(self, character: Character, game_repository: Dict[int, Dict], player_input_adapter: PlayerInputAdapter):
        """
        Inicializa o Agent com arquitetura PlayerInputAdapter v1.2.
        
        Args:
            character: Instância da classe Character (pode ter occupation=None inicialmente)
            game_repository: Dicionário com todas as páginas do jogo
            player_input_adapter: Adapter para captura de entrada do jogador
        """
        self.character = character
        self.game_data = game_repository
        self.current_page = 1
        self.combat_status = {}
        
        # Nova arquitetura v1.2: PlayerInputAdapter
        self.player_input_adapter = player_input_adapter
        
        # Circuit Breaker Pattern - Previne loops infinitos
        self.failed_choices_count = 0
        self.max_choice_retries = 3
        
        # Criar instância do Cockpit para visualização rica
        self.cockpit = Cockpit(self.character, game_repository)

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

    def _decide(self, choices):
        """
        Decide qual ação tomar usando PlayerInputAdapter (Arquitetura v1.2).
        Implementa Circuit Breaker Pattern e validação de regras conforme seção 5.4.
        
        Args:
            choices: Lista de choices disponíveis na página atual
            
        Returns:
            choice dict selecionado e validado, ou None se circuit breaker ativado
        """
        # CIRCUIT BREAKER: Verificar se já excedeu máximo de falhas
        if self.failed_choices_count >= self.max_choice_retries:
            error_msg = f"[CIRCUIT BREAKER] Máximo de tentativas ({self.max_choice_retries}) excedido para escolhas falhadas consecutivas. Encerrando execução para evitar loop infinito."
            print(f"🚨 {error_msg}")
            
            # Adicionar ao histórico
            if hasattr(self.character, 'add_to_history'):
                self.character.add_to_history(
                    page_number=self.current_page,
                    page_text="[SYSTEM CIRCUIT BREAKER]",
                    choice_made={"system_error": error_msg},
                    choice_index=0
                )
            
            print("🛑 Execução interrompida para preservar estabilidade do sistema")
            return None  # Sinaliza para o run() encerrar
        
        # VALIDAÇÃO CRÍTICA: Verificar se choices está em formato válido
        if not self._validate_choices(choices):
            print("ERRO CRÍTICO: Lista de choices inválida. Usando ação de fallback.")
            raise Exception("Invalid choices format")
        
        # Loop de retry para validação de regras (máximo 3 tentativas)
        max_attempts = 3
        attempt = 0
        
        while attempt < max_attempts:
            attempt += 1
            
            # Obter dados estruturados do cockpit
            character_data = self.cockpit.render_character_status()
            
            # Usar PlayerInputAdapter para obter choice_index (base 1)
            choice_index = self.player_input_adapter.get_decision(choices, character_data)
            
            # Conversão para base 0 e obtenção do choice dict
            chosen_choice = choices[choice_index - 1]
            
            # VALIDAÇÃO DE REGRAS: Verificar se choice é válido para estado atual
            validation_result = self._validate_choice_against_rules(chosen_choice)
            
            if validation_result["valid"]:
                # SUCCESS: Reset circuit breaker counter
                self.failed_choices_count = 0
                
                # Exibir escolha formatada
                print("🎯 ESCOLHA SELECIONADA E VALIDADA:")
                print("=" * 50)
                for key, value in chosen_choice.items():
                    print(f"  {key}: {value}")
                print("=" * 50)
                
                # RESOLUÇÃO DE CONDITIONAL_ON: Se choice tem conditional_on, resolvê-lo
                if 'conditional_on' in chosen_choice:
                    resolved_choice = self._resolve_conditional_choice(chosen_choice)
                    print(f"🎯 CHOICE RESOLVIDO PARA OCUPAÇÃO:")
                    print("=" * 50)
                    for key, value in resolved_choice.items():
                        print(f"  {key}: {value}")
                    print("=" * 50)
                    return resolved_choice
                
                return chosen_choice
            else:
                # FAILURE: Increment circuit breaker counter
                self.failed_choices_count += 1
                
                # Choice inválido - adicionar feedback de erro ao histórico
                error_message = f"[SYSTEM ERROR] {validation_result['error_message']} (Falha {self.failed_choices_count}/{self.max_choice_retries})"
                print(f"❌ {error_message}")
                
                # Adicionar erro ao histórico do character para contexto futuro
                if hasattr(self.character, 'add_to_history'):
                    # Usar método moderno se disponível
                    self.character.add_to_history(
                        page_number=self.current_page,
                        page_text="[SYSTEM]",
                        choice_made={"error": error_message},
                        choice_index=choice_index
                    )
                
                # Verificar se atingiu limite do circuit breaker
                if self.failed_choices_count >= self.max_choice_retries:
                    print("🚨 Circuit Breaker será ativado na próxima tentativa")
                    print("🛑 Forçando fallback para evitar loop infinito...")
                    
                    # Fallback de emergência: retornar primeira choice básica
                    for choice in choices:
                        if self._is_basic_choice(choice):
                            print(f"🔄 Usando fallback choice: {choice.get('text', 'N/A')}")
                            return choice
                    
                    # Se nenhuma choice básica, retornar primeira disponível
                    print(f"🔄 Usando primeira choice disponível: {choices[0].get('text', 'N/A')}")
                    return choices[0]
                
                if attempt >= max_attempts:
                    print("⚠️  Máximo de tentativas excedido no loop atual.")
                    # Continue para próxima tentativa, circuit breaker decide se para
                    break
                
                print(f"🔄 Solicitando nova escolha... (Tentativa {attempt + 1}/{max_attempts})")
        
        # Nunca deveria chegar aqui, mas safety fallback
        return choices[0]
    
    def _resolve_conditional_choice(self, choice: Dict[str, Any]) -> Dict[str, Any]:
        """
        Resolve uma choice conditional_on para o path específico da ocupação atual.
        
        Args:
            choice: Choice com conditional_on a ser resolvido
            
        Returns:
            Choice resolvido para a ocupação atual
        """
        if choice.get('conditional_on') != 'occupation':
            # Se não é conditional_on occupation, retornar como está
            return choice
        
        current_occupation = self.character.occupation
        paths = choice.get('paths', {})
        
        # Determinar qual path usar
        if current_occupation in paths:
            resolved_choice = paths[current_occupation].copy()
            print(f"🎯 Usando path para ocupação '{current_occupation}'")
        elif 'default' in paths:
            resolved_choice = paths['default'].copy()
            print(f"🎯 Usando path 'default' (ocupação atual: {current_occupation or 'None'})")
        else:
            # Não deveria acontecer se validação passou, mas fallback de segurança
            print(f"⚠️  ERRO: Nenhum path encontrado para ocupação '{current_occupation}' e sem default")
            return choice
        
        # Preservar texto original se não houver no path resolvido
        if 'text' not in resolved_choice and 'text' in choice:
            resolved_choice['text'] = choice['text']
            
        return resolved_choice
    
    def _validate_choice_against_rules(self, choice: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida se uma choice é permitida pelas regras do jogo (v1.2).
        
        Args:
            choice: Choice a ser validado
            
        Returns:
            Dict com 'valid' (bool) e 'error_message' (str) se inválido
        """
        # Validação de conditional_on (ocupação)
        if 'conditional_on' in choice:
            if choice['conditional_on'] == 'occupation':
                current_occupation = self.character.occupation
                
                # Verificar se tem paths definidos
                paths = choice.get('paths', {})
                
                # Se ocupação atual não está nos paths e não há default
                if current_occupation not in paths and 'default' not in paths:
                    return {
                        "valid": False,
                        "error_message": f"Choice requer ocupação específica. Ocupação atual: {current_occupation or 'None'}"
                    }
                
                # Se ocupação atual não está nos paths mas há default, permitir
                # Se ocupação atual está nos paths, permitir
                
        # Validação de requires (pré-requisitos adicionais)
        if 'requires' in choice:
            for requirement in choice['requires']:
                # Implementar validação de requisitos específicos conforme necessário
                # Ex: knuckles_restrained, specific items, etc.
                pass
        
        # Choice é válido
        return {"valid": True, "error_message": ""}
    
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
        
        # Choice com roll também é considerada básica
        if any(key in choice for key in ['roll', 'luck_roll', 'opposed_roll']):
            return True
            
        return False
    #Não tem fallback deve ser reenviada para o agente decisorio novamente com historico atualizado
    def _create_fallback_choice(self):
        """Cria uma choice de segurança para situações de erro."""
        raise Exception("Fallback choice should not be used in this implementation.")

    def _process_effects(self, effects):
        """
        Processa uma lista de efeitos no estado do agente (v1.2).
        Refatorado para usar character.apply_effects() com tratamento de ocupação dinâmica.
        """
        if not isinstance(effects, list):
            print(f"AVISO: 'effects' deve ser uma lista, recebido: {type(effects)}. Ignorando efeitos.")
            return

        occupation_before = self.character.occupation
        
        # Usar o método robusto da classe Character
        result = self.character.apply_effects(effects)
        
        # Verificar se ocupação foi definida/alterada
        occupation_after = self.character.occupation
        if occupation_before != occupation_after:
            print(f"🎯 OCUPAÇÃO DEFINIDA: {occupation_before or 'None'} → {occupation_after}")
            print(f"📋 Personagem agora tem acesso a habilidades e choices específicas de {occupation_after}")
        
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
        Retorna uma tupla com o (outcome, next_page).
        """
        if not self._validate_choice(choice):
            raise ValueError(f"Choice inválida: {choice}")
        
        outcome = choice.get("outcome", "")
        next_page = self.current_page

        try:
            if "effects" in choice:
                self._process_effects(choice["effects"])

            if "roll" in choice:
                roll_data = choice["roll"]
                if isinstance(roll_data, str):
                    skill_name, difficulty, results = roll_data, choice.get("difficulty", "normal"), choice.get("results", {})
                elif isinstance(roll_data, dict):
                    skill_name, difficulty, results = roll_data.get("skill"), roll_data.get("difficulty", "normal"), roll_data.get("results", {})
                else:
                    raise ValueError(f"Formato de 'roll' inválido: {roll_data}")

                roll_result = self.character.roll_skill(skill_name, "common", difficulty=difficulty) or \
                              self.character.roll_skill(skill_name, "combat", difficulty=difficulty) or \
                              self.character.roll_skill(skill_name, "expert", difficulty=difficulty) or \
                              self.character.roll_characteristic(skill_name, difficulty=difficulty)

                if not roll_result or not roll_result.get("success"):
                    raise Exception(f"Falha na rolagem de '{skill_name}'")

                level = roll_result["level"]
                print(f"Rolled {skill_name}: {roll_result['roll']} vs {roll_result['target']} -> Level {level}")
                
                result = results.get(str(level))
                if result:
                    if isinstance(result, int):
                        if result >= 0: next_page = result
                    elif isinstance(result, dict):
                        if "effects" in result: self._process_effects(result["effects"])
                        if "goto" in result and isinstance(result["goto"], int) and result["goto"] >= 0:
                            next_page = result["goto"]

            elif "luck_roll" in choice and choice["luck_roll"]:
                roll_result = self.character.roll_luck()
                level = roll_result["level"]
                print(f"Rolled Luck: {roll_result['roll']} vs {roll_result['target']} -> Level {level}")
                
                results = choice.get("results", {})
                result = results.get(str(level)) or next((results.get(str(i)) for i in range(level - 1, 0, -1) if results.get(str(i))), None)
                if result:
                    if "effects" in result: self._process_effects(result["effects"])
                    if "goto" in result and isinstance(result["goto"], int) and result["goto"] >= 0:
                        next_page = result["goto"]

            elif "goto" in choice:
                goto_page = choice["goto"]
                if isinstance(goto_page, int) and goto_page >= 0:
                    next_page = goto_page
                else:
                    print(f"ERRO: Página 'goto' inválida: {goto_page}")

        except Exception as e:
            print(f"ERRO CRÍTICO durante execução da ação: {e}")
            outcome = f"Erro de Execução: {str(e)}"
            
        return outcome, next_page

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
            
            # 3. Decide (usando PlayerInputAdapter v1.2)
            chosen_action = self._decide(choices)
            
            # CIRCUIT BREAKER CHECK: Se _decide retornar None, encerrar execução
            if chosen_action is None:
                print("🚨 CIRCUIT BREAKER ATIVADO - Encerrando execução do agente")
                print("📊 Estatísticas da sessão:")
                print(f"   - Página atual: {self.current_page}")
                print(f"   - Falhas consecutivas: {self.failed_choices_count}")
                print(f"   - Limite máximo: {self.max_choice_retries}")
                break
            
            
            # 4. Act
            try:
                outcome, next_page = self.perform_action(chosen_action)
                
                # Se a ação foi bem-sucedida, reseta o contador de falhas.
                self.failed_choices_count = 0
                
                # LOG DA JOGADA: Exibir dados estruturados em JSON
                choice_index = None
                for i, choice in enumerate(choices, 1):
                    if choice == chosen_action:
                        choice_index = i
                        break
                self._log_turn_summary(chosen_action, choice_index or 1, outcome)
                self.cockpit.render_game_screen()
                print(f"Agente escolheu: {chosen_action}")
                
                # PAUSA MANUAL: Aguardar ENTER para continuar (todos os modos)
                try:
                    input("Pressione ENTER para continuar...")
                except KeyboardInterrupt:
                    print("\n🛑 Jogo interrompido pelo usuário")
                    break
                
            except Exception as e:
                print(f"🚨 ERRO DE EXECUÇÃO: A ação falhou. {e}")
                self.failed_choices_count += 1
                outcome = f"Erro de Execução: {e}"
                if self.failed_choices_count >= self.max_choice_retries:
                    print("🚨 CIRCUIT BREAKER ATIVADO DEVIDO A ERRO DE EXECUÇÃO - Encerrando.")
                    break
            
            # 5. Record - Registrar escolha no histórico detalhado
            choice_index = None
            for i, choice in enumerate(choices):
                if choice == chosen_action:
                    choice_index = i
                    break
            
            self._record_choice_in_history(page_text, chosen_action, choice_index, outcome)
            
            # Navegação para a próxima página
            self.current_page = next_page

            # Condição de parada
            if self.current_page == 0:
                print("Fim da história (goto: 0).")
                break

    def _observe(self):
        """
        Observa o ambiente usando Cockpit para visualização rica.
        Exibe a nova "tela de video-game" de forma limpa.
        """
        # Configurar a página atual no Cockpit
        self.cockpit.set_current_page(self.current_page)
        
        # Renderizar a tela de video-game (sem prints extras)
        self.cockpit.render_game_screen()
        
        # Obter dados da página atual
        page_data = self.game_data.get(self.current_page, {})
        page_text = page_data.get("text", "Página não encontrada.")
        choices = page_data.get("choices", [])
        
        return page_text, choices

    def _orient(self, page_text):
        """
        Orienta o agente, atualizando seu estado interno com base nas observações.
        Processamento interno sem output visual.
        """
        # Processamento interno silencioso
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
    
    def _log_turn_summary(self, chosen_choice: Dict[str, Any], choice_index: int, outcome: str):
        """
        Registra um resumo limpo da jogada como JSON estruturado.
        
        Este método implementa o sistema de logging separado solicitado,
        mostrando a escolha do jogador em formato JSON entre cada tela.
        
        Args:
            chosen_choice: Choice executada
            choice_index: Índice da choice selecionada (base 1)
            outcome: Resultado da execução da choice
        """
        import json
        
        # Estruturar dados da jogada (foco no código da choice)
        turn_data = {
            "page": self.current_page,
            "choice_selected": {
                "index": choice_index,
                "choice_data": chosen_choice  # Código completo da choice
            },
            "execution_result": outcome if outcome else "Executada com sucesso"
        }
        
        # Exibir log estruturado de forma mais limpa
        print("\n📋 LOG DA JOGADA:")
        print(json.dumps(turn_data, indent=2, ensure_ascii=False))
        print("")  # Linha em branco para separação

#!/usr/bin/env python3
"""
Autonomous Gaming Agent - The Domestic
Entry point for the gaming agent with PlayerInputAdapter architecture v1.2

Usage:
    python main.py --player demo   (modo demonstração automática)
    python main.py --player human  (modo console interativo)
    python main.py --player llm    (modo IA via API)
"""

import argparse
import os
import sys
from game_repository import GameRepository
from agent import Agent
from player_strategy import DemoPlayerAdapter, HumanPlayerAdapter, LLMPlayerAdapter


def main():
    """
    Ponto de entrada principal do agente de jogo.
    Configura e inicia o agente com o PlayerInputAdapter apropriado.
    """
    # Configuração argparse para seleção do tipo de jogador
    parser = argparse.ArgumentParser(
        description="Autonomous Gaming Agent - The Domestic",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Tipos de jogador disponíveis:
  demo    - Modo demonstração automática (DefaultDecisionController interno)
  human   - Modo console interativo (input manual via terminal)
  llm     - Modo IA via API (requer GEMINI_API_KEY)

Exemplos:
  python main.py --player demo
  python main.py --player human
  python main.py --player llm
        """
    )
    
    parser.add_argument(
        '--player', 
        choices=['demo', 'human', 'llm'], 
        default='demo',
        help='Tipo de interface do jogador (padrão: demo)'
    )

    parser.add_argument(
        '--lang',
        choices=['en', 'pt'],
        default='en',
        help='Idioma do jogo (padrão: en)'
    )

    parser.add_argument(
        '--debug',
        action='store_true',
        help='Ativa o modo de depuração com logs detalhados'
    )
    
    args = parser.parse_args()
    
    try:
        # Game Repository com cache das 112 páginas
        print("[INFO] Carregando repositório do jogo...")
        game_repo = GameRepository(lang=args.lang)
        
        # Seleção e configuração do PlayerInputAdapter baseado no argumento
        print(f"[INFO] Configurando {args.player} player adapter...")
        
        if args.player == 'human':
            player_adapter = HumanPlayerAdapter()
            print("[INFO] Modo humano: Use o console para interagir")
            
        elif args.player == 'llm':
            # api_key = os.getenv("GEMINI_API_KEY")
            # if not api_key:
            #     print("[ERROR] GEMINI_API_KEY não encontrada nas variáveis de ambiente")
            #     print("        Configure a chave da API antes de usar o modo LLM:")
            #     print("        export GEMINI_API_KEY='sua_chave_aqui'")
            #     sys.exit(1)
            api_key = "DUMMY_KEY_FOR_TESTING"  # Substitua pela sua chave real ou use variável de ambiente
            player_adapter = LLMPlayerAdapter()
            print("[INFO] Modo LLM: IA tomará decisões via API")
            
        else:  # default: demo
            player_adapter = DemoPlayerAdapter()
            print("[INFO] Modo demo: Execução automática para demonstração")
        
        # Instanciar Agent com dependency injection (arquitetura v1.2)
        print("[INFO] Inicializando Agent com nova arquitetura PlayerInputAdapter...")
        agent = Agent(
            game_repository=game_repo,
            player_input_adapter=player_adapter
        )
        
        # Iniciar o game loop (ciclo OODA)
        print("[INFO] Iniciando jogo...")
        print("=" * 60)
        agent.run()
        
    except KeyboardInterrupt:
        print("\n\n[INFO] Jogo interrompido pelo usuário")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n[ERROR] Erro durante execução: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

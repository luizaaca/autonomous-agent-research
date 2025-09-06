import pages
from agent import Agent

class GameInstructions:
    def get_backstory(self):
        return "Você é um agente OODA baseado em IA navegando por um livro-jogo de investigação policial. Seu objetivo é resolver o mistério, tomar decisões estratégicas e manter seu personagem vivo. Use suas habilidades de raciocínio, análise e tomada de decisão para progredir na história."

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

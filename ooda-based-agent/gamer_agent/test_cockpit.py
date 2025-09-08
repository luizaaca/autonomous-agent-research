from character import Character
from pages import PAGES
from cockpit import Cockpit

# Criar personagem
character = Character('Test Agent', 'Police Officer', 35, 'Test backstory')
cockpit = Cockpit(character, PAGES)
cockpit.set_current_page(1)

# Testar a renderização
print('Testando renderização do Cockpit com novo layout...')
cockpit.render_game_screen()
print('Renderização concluída com sucesso.')

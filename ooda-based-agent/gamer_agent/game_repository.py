"""
Game Repository Module - Gerenciamento centralizado de dados do jogo

Este módulo implementa o padrão Repository para acesso aos dados do jogo,
incluindo páginas, validação e cache. Separa as responsabilidades de
acesso a dados da lógica de negócio.
"""

from typing import Dict, Any, Optional
import pages


class GameRepository:
    """
    Repositório centralizado para dados do jogo.
    
    Implementa padrão Repository para encapsular acesso aos dados das páginas,
    proporcionando cache, validação e interface limpa para o resto do sistema.
    """
    
    def __init__(self):
        """Inicializa o repositório com dados das páginas."""
        self._pages_data = pages.PAGES
        self._cache = {}
        self._validate_data()
    
    def get_page(self, page_id: int, default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Obtém dados de uma página específica.
        
        Args:
            page_id: ID da página
            default: Valor padrão se página não existir
            
        Returns:
            Dicionário com dados da página
        """
        return self._pages_data.get(page_id, default)
    
    def get(self, page_id: int, default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Método de compatibilidade com interface GameData legacy.
        
        Args:
            page_id: ID da página
            default: Valor padrão se página não existir
            
        Returns:
            Dicionário com dados da página
        """
        return self.get_page(page_id, default)
    
    def get_page_text(self, page_id: int) -> str:
        """
        Obtém apenas o texto de uma página.
        
        Args:
            page_id: ID da página
            
        Returns:
            Texto da página ou mensagem de erro
        """
        page_data = self.get_page(page_id)
        if page_data:
            return page_data.get("text", "Texto não encontrado.")
        return f"Página {page_id} não encontrada."
    
    def get_page_choices(self, page_id: int) -> list:
        """
        Obtém choices de uma página.
        
        Args:
            page_id: ID da página
            
        Returns:
            Lista de choices da página
        """
        page_data = self.get_page(page_id)
        if page_data:
            return page_data.get("choices", [])
        return []
    
    def page_exists(self, page_id: int) -> bool:
        """
        Verifica se uma página existe.
        
        Args:
            page_id: ID da página
            
        Returns:
            True se página existe
        """
        return page_id in self._pages_data
    
    def get_all_page_ids(self) -> list:
        """
        Obtém lista de todos os IDs de páginas disponíveis.
        
        Returns:
            Lista com IDs das páginas
        """
        return list(self._pages_data.keys())
    
    def get_total_pages(self) -> int:
        """
        Obtém total de páginas no jogo.
        
        Returns:
            Número total de páginas
        """
        return len(self._pages_data)
    
    def _validate_data(self) -> None:
        """
        Valida estrutura dos dados das páginas.
        
        Raises:
            ValueError: Se dados estiverem malformados
        """
        if not isinstance(self._pages_data, dict):
            raise ValueError("Pages data deve ser um dicionário")
        
        for page_id, page_data in self._pages_data.items():
            if not isinstance(page_data, dict):
                raise ValueError(f"Página {page_id} deve ser um dicionário")
            
            if "text" not in page_data:
                raise ValueError(f"Página {page_id} deve ter campo 'text'")
            
            # Choices é opcional, mas se existir deve ser lista
            if "choices" in page_data and not isinstance(page_data["choices"], list):
                raise ValueError(f"Página {page_id}: 'choices' deve ser uma lista")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Obtém estatísticas sobre os dados do jogo.
        
        Returns:
            Dicionário com estatísticas
        """
        total_pages = self.get_total_pages()
        pages_with_choices = 0
        total_choices = 0
        
        for page_id in self.get_all_page_ids():
            choices = self.get_page_choices(page_id)
            if choices:
                pages_with_choices += 1
                total_choices += len(choices)
        
        return {
            "total_pages": total_pages,
            "pages_with_choices": pages_with_choices,
            "pages_without_choices": total_pages - pages_with_choices,
            "total_choices": total_choices,
            "avg_choices_per_page": total_choices / max(pages_with_choices, 1)
        }
    
    def __repr__(self) -> str:
        """Representação string do repositório."""
        stats = self.get_statistics()
        return f"GameRepository(pages={stats['total_pages']}, choices={stats['total_choices']})"


# Teste e validação
if __name__ == "__main__":
    print("=== TESTE DO GAME REPOSITORY ===\n")
    
    # Criar repositório
    repo = GameRepository()
    print(f"1. Repositório criado: {repo}")
    print()
    
    # Testar acesso a páginas
    print("2. Teste de acesso a páginas:")
    page_1 = repo.get_page(1)
    print(f"   Página 1 existe: {repo.page_exists(1)}")
    print(f"   Texto da página 1: {repo.get_page_text(1)[:50]}...")
    print(f"   Choices da página 1: {len(repo.get_page_choices(1))} choices")
    print()
    
    # Testar página inexistente
    print("3. Teste página inexistente:")
    print(f"   Página 999 existe: {repo.page_exists(999)}")
    print(f"   Texto da página 999: {repo.get_page_text(999)}")
    print()
    
    # Estatísticas
    print("4. Estatísticas do jogo:")
    stats = repo.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    print()
    
    print("=== TESTE CONCLUÍDO ===")

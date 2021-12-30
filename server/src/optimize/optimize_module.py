from dependency_injector import containers, providers
from src.optimize.adapter.project_adapter import ProjectAdapter
from src.optimize.infrastructure.project_repository import ProjectRepository
from src.optimize.usecase.optimize_path_service import OptimizePathService


class OptimizeModule(containers.DeclarativeContainer):
    project_repository=providers.Singleton(ProjectRepository)
    
    optimize_path_service = providers.Singleton(OptimizePathService, project_repository=project_repository)

    project_adapter = providers.Singleton(ProjectAdapter, project_repository=project_repository)
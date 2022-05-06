from pymitter import EventEmitter
from src.image.usecase.add_image_service import AddImageService
from src.image.infrastructure.image_repository import ImageRepository
from dependency_injector import containers, providers


class ImageModule(containers.DeclarativeContainer):


    # config = providers.Configuration(yaml_files=["config.yml"])

    # plotter_client = providers.Factory( 
    #     api_key=config.giphy.api_key,
    #     timeout=config.giphy.request_timeout,
    # )

    # search_service = providers.Factory(
    #     services.SearchService,
    #     giphy_client=giphy_client,
    # )

    image_repository=providers.Singleton(ImageRepository)
    add_image_service = providers.Singleton(
        AddImageService, 
        repository=image_repository
    )
    
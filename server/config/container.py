from dependency_injector import containers, providers
from dependency_injector.wiring import inject
from src.image.image_module import ImageModule

from src.plotter.module import PlotterModule  # noqa
from pymitter import EventEmitter


class Container(containers.DeclarativeContainer):
    #__self__ = providers.Self()
    #wiring_config = containers.WiringConfiguration(modules=["image_controller", "plotter_controller"])
    config = providers.Configuration()    
    
    print("Container init")
    plotter = providers.Container(PlotterModule)
    print("PlotterModule init")
    image = providers.Container(ImageModule)
    print("ImageModule init")

    events = providers.Singleton(EventEmitter)

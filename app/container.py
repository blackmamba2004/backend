from dishka import make_async_container, AsyncContainer

from app.providers import provider_list


def create_container() -> AsyncContainer:
    return make_async_container(
        *provider_list()
    )

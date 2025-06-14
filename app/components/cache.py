import json
import logging
from typing import Optional, Type, Callable, Coroutine, Any

from redis import Redis
from app.config import RedisConfig
from app.schemas import BaseSchema

logger = logging.getLogger(__name__)

type CacheData = BaseSchema | dict


class RedisCache:
    """
    Класс для упрощённой работы с кэшированием через Redis
    """

    def __init__(
        self, redis: Redis, config: RedisConfig
    ):
        self._redis = redis
        self._config = config

    async def get(
        self,
        key_tuple: tuple,
        response_dto: Optional[Type[BaseSchema]] = None
    ) -> Optional[CacheData]:
        """
        Получить данные из Redis по ключу
        :param key_tuple: Ключ-кортеж
        :param response_dto: Класс для преобразования полученных данных в DTO
        :return:
        """
        key = self.__format_key(key_tuple)
        return await self.get_by_key(key, response_dto)

    async def get_by_key(
        self,
        redis_key: str | bytes,
        response_dto: Optional[Type[BaseSchema]] = None
    ) -> Optional[CacheData]:
        """
        Получить данные из кэша по строчному или байтовому ключу
        :param redis_key: Готовый ключ
        :param response_dto: Класс для преобразования полученных данных в DTO
        :return:
        """
        if isinstance(redis_key, bytes):
            key_str = redis_key.decode()
        else:
            key_str = redis_key

        data = await self._redis.get(redis_key)
        if data is None:
            logger.debug(f"Not found data for key: {key_str}")
            return None

        caching_data = self.__decode_body(data)
        logger.debug(f"Found data in cache for key: {key_str}")
        if response_dto is None:
            return caching_data

        return response_dto(**caching_data)

    async def set(
        self, key_tuple: tuple, body: CacheData, ttl: Optional[int] = None
    ) -> None:
        """
        Установить значение в кэш
        :param key_tuple: Кортеж значений для ключа
        :param body: Данные для вставки в Redis
        :param ttl: Время жизни установленной записи
        :return:
        """
        redis_key = self.__format_key(key_tuple)
        serialized_body = self.__encode_body(body)
        await self._redis.set(
            name=redis_key,
            value=serialized_body,
            ex=self._config.cache_ttl if ttl is None else ttl
        )
        logger.debug(f"Set data in cache for key: {redis_key}")

    async def set_by_key(
            self,
            redis_key: str | bytes,
            body: CacheData,
            ttl: Optional[int] = None
    ) -> None:
        """
        Установить значение в кэш
        :param redis_key: Готовый ключ для Redis
        :param body: Данные для вставки в Redis
        :param ttl: Время жизни установленной записи
        :return:
        """
        serialized_body = self.__encode_body(body)
        await self._redis.set(
            name=redis_key,
            value=serialized_body,
            ex=self._config.cache_ttl if ttl is None else ttl
        )
        logger.debug(f"Set data in cache for key: {redis_key}")

    async def delete(self, key_tuple: tuple) -> None:
        """
        Удалить значение по ключу
        """
        key = self.__format_key(key_tuple)
        await self._redis.delete(key)
        logger.debug(f"Delete data in cache for key: {key_tuple}")

    async def delete_by_prefix(self, prefix: str) -> None:
        """
        Удалить все значения из кэша, которые начинаются на указанный префикс
        :param prefix:
        :return:
        """
        for key in await self._redis.keys(prefix + "*"):
            await self._redis.delete(key)
            logger.debug(f"Delete data in cache for key: {key}")

    async def behind_cache(
            self,
            key_tuple: tuple,
            func: Callable[[], Coroutine[Any, Any, CacheData]],
            ttl: Optional[int] = None
    ) -> tuple[CacheData, bool]:
        """
        Проверить наличие значения в кэше по ключу,
        если значение отсутствует, то сохранить результат
        выполнения переданной функции в кэш и вернуть его,
        иначе вернуть значение из кэша.
        :param key_tuple: Ключ
        :param func: Callback-функция
        :param ttl: Время жизни для установки кэша
        :return:
        """

        data = await self.get(key_tuple)
        if data is not None:
            return data, True

        data = await func()
        await self.set(key_tuple, data, ttl)
        return data, False

    async def get_keys_by_prefix(self, prefix: str) -> list:
        """
        Получить все ключи из redis, которые соответствуют определённому префиксу
        :param prefix:
        :return:
        """
        return await self._redis.keys(prefix)

    @staticmethod
    def __format_key(key_tuple: tuple) -> bytes:
        """
        Преобразовать значение кортежа в строку и представить её в виде байтов
        :param key_tuple: Ключ
        :return:
        """
        return (":".join(str(item) for item in key_tuple)).encode()

    @staticmethod
    def __encode_body(body: CacheData) -> bytes:
        """
        Закодировать в виде байтов словарь из DTO-объект
        :param body:
        :return:
        """
        if isinstance(body, BaseSchema):
            return body.model_dump_json().encode()
        return json.dumps(body).encode()

    @staticmethod
    def __decode_body(body: bytes) -> dict:
        """
        Выполнить декодирование данных из байтов в словарь
        :param body:
        :return:
        """
        return json.loads(body.decode())

    async def incr(
        self, key_tuple: tuple, amount: int = 1
    ) -> int:
        """
        Инкрементировать значение key на amount
        :param key_tuple: Ключ
        :param amount: Шаг инкремента
        :return:
        """
        key = self.__format_key(key_tuple)
        return await self._redis.incr(key, amount)

    async def exists(self, key_tuple: str) -> int:
        """
        Проверить существование ключа
        :param key_tuple: Ключ
        :return:
        """
        key = self.__format_key(key_tuple)
        return await self._redis.exists(key)

    async def init_counter_with_ttl(
        self, key_tuple: tuple, counter_ttl: int, amount: int = 1
    ) -> int:
        """
        Инициализировать и инкрементировать счетчик, если не существует,
        иначе инкрементировать
        :param key_tuple: Ключ
        :param counter_ttl: Время жизни счетчика
        :param amount: Шаг инкремента
        """
        exists = await self.exists(key_tuple)

        if not exists:
            await self.set(key_tuple, amount, counter_ttl)
            return amount

        return await self.incr(key_tuple, amount)

    async def get_raw(self, key_tuple: tuple) -> dict | None:
        """
        Получить данные из кэша в виде словаря по ключу
        :param key_tuple: Ключ
        :return: Значение из кэша в виде словаря или None
        """
        key = self.__format_key(key_tuple)
        data = await self._redis.get(key)
        if data is None:
            return None

        return self.__decode_body(data)
from dataclasses import dataclass
from abc import ABC, abstractmethod
import requests
from functools import cached_property
from inspect import signature
import warnings
from math import ceil

from typing import Any, Iterator, Optional
from typing_extensions import Self

APIResponse = dict[str, Any]

# Must match page size of requests to puzzgrid.com/api/grids?...
GRIDS_PER_PAGE = 10


class PuzzGridAPIRequest:
    """An API request with query parameters"""

    path: str
    parameters: Optional[dict[str, str]] = None
    base_url: str = "https://puzzgrid.com/api/"

    def __init__(self, path: str, headers: dict[str, str] = {}, **query_parameters):
        self.path = path
        self.headers = headers
        self.parameters = {
            k: ','.join([str(x) for x in v]) if isinstance(v, list) else str(v)
            for k, v in query_parameters.items()
        }

    @property
    def url(self) -> str:
        """The complete URL of the API request"""
        return self.base_url + self.path

    @cached_property
    def response(self) -> APIResponse:
        """Fetches from the API and converts to a JSON dict"""
        res = requests.get(self.url, params=self.parameters, headers=self.headers)
        res.status_code
        return res.json()


@dataclass(frozen=True)
class Model(ABC):
    """(Part of) a response from the API"""

    @classmethod
    @abstractmethod
    def parse_field(cls, key: str, value: Any) -> Any:
        """
        Decides how each field should be parsed from a provided JSON
        dictionary.
        """
        raise NotImplementedError()

    @classmethod
    def from_response(cls, res: APIResponse) -> Optional[Self]:
        # Make sure APIResponse has all the keys needed to initialise the model
        keys = list(signature(cls.__init__).parameters.keys())[1:]
        if not all(k in res for k in keys):
            warnings.warn(f"Invalid API response, cannot cast to {cls.__name__}")
            return None
        # If any of the fields couldn't be parsed, then return None
        fields = {k: cls.parse_field(k, res[k]) for k in keys}
        if any(v is None for v in fields.values()):
            return None
        # Create the model with the required keys
        return cls(**fields)


@dataclass(frozen=True)
class GridModel(Model):
    """A puzzgrid puzzle"""

    id: int
    creator: str
    difficulty: float
    quality: float
    country: str
    date: int
    user_id: str
    tags: list[str]

    @classmethod
    def parse_field(cls, key: str, value: Any) -> Any:
        return value

    @property
    def is_ladder(self) -> bool:
        return "ladder" in self.tags


@dataclass(frozen=True)
class SpecialGridModel(Model):
    """The puzzgrid puzzle of the day/week"""

    id: int
    name: str
    creation_time: int
    type: str

    @classmethod
    def parse_field(cls, key: str, value: Any) -> Any:
        return value

    @property
    def is_ladder(self) -> bool:
        return self.type == "ladder"


@dataclass(frozen=True)
class ListOfGridsModel(Model):
    """A list of puzzgrids returned by an API query to /api/grids"""

    rows: list[GridModel]
    """List of grids in date order (newest to oldest)"""

    @classmethod
    def parse_field(cls, key: str, value: Any) -> Any:
        rows = [GridModel.from_response(g) for g in value]

        # Filter out grids that couldn't be parsed
        rows = [g for g in rows if g is not None]

        # Sort by date
        return sorted(rows, key=lambda g: g.date, reverse=True)


@dataclass(frozen=True)
class GridOfTheXModel(Model):
    """The daily and weekly puzzgrids, as returned by /api/gridofthex"""

    week: SpecialGridModel
    """Grid of the week"""
    day: SpecialGridModel
    """Grid of the day"""

    @classmethod
    def parse_field(cls, key: str, value: Any) -> Any:
        return SpecialGridModel.from_response(value)


#####################################
# API endpoint wrappers

def get_grids(
    min_difficulty: float,
    min_quality: float,
    country: str = 'all',
    max_results: int = 30
) -> Iterator[GridModel]:

    total_grids = 0

    for page in range(1, 1 + ceil(max_results / GRIDS_PER_PAGE)):
        req = PuzzGridAPIRequest(
            '/grids',
            dif=min_difficulty,
            qual=min_quality,
            nat=country,
            page=page,
        )
        grids = ListOfGridsModel.from_response(req.response)
        if not grids:
            warnings.warn("Got bad/empty response from api/grids")
            raise StopIteration

        for grid in grids.rows:
            if total_grids >= max_results:
                raise StopIteration
            yield grid
            total_grids += 1

    print(total_grids, max_results)
    if total_grids < max_results:
        warnings.warn(f"Couldn't fetch {max_results} grids from api/grids")


def get_weekly() -> Optional[SpecialGridModel]:

    req = PuzzGridAPIRequest('/gridofthex')
    grids = GridOfTheXModel.from_response(req.response)
    if grids is None:
        warnings.warn("Failed to fetch grids")
        return None

    return grids.week


def get_daily() -> Optional[SpecialGridModel]:

    req = PuzzGridAPIRequest('/gridofthex')
    grids = GridOfTheXModel.from_response(req.response)
    if grids is None:
        warnings.warn("Failed to fetch grids")
        return None

    return grids.day

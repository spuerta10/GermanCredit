from abc import ABC, abstractmethod
from typing import Any


class BaseView(ABC):
    """Abstract base class for views in the MVC pattern.

    This class defines a standard interface for rendering views.
    """

    @abstractmethod
    def render(self) -> dict[str, Any]:
        """Renders the view and returns the data to be displayed.

        Returns:
            Dict[str, Any]: A dictionary containing the data
                that will be rendered in the view.
        """
        ...

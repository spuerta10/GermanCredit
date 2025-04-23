from abc import abstractmethod
from typing import Any

from src.view.base_view import BaseView


class BaseFormView(BaseView):
    # @override
    @abstractmethod
    def render(self) -> dict[str, Any]:
        """Renders the view and returns the data to be displayed.

        Returns:
            Dict[str, Any]: A dictionary containing the data
                that will be rendered in the view.
        """
        ...

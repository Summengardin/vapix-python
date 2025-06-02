"""vapix_python.OpticsControl
===========================
Axis VAPIX® *Optics Control* API (``opticscontrol.cgi``) wrapper
----------------------------------------------------------------

This class mirrors the style and API‑surface of ``PTZControl`` but targets
cameras that expose optical zoom & focus without mechanical pan/tilt.

Only a subset of the 1.2 Optics Control API is wrapped – more can be added
via the generic :py:meth:`~OpticsControl.call` helper.

* Author: OpenAI ChatGPT (generated)
* License: MIT (same as vapix_python)
"""
from __future__ import annotations

import json
import logging
import uuid
from typing import Any, Dict, List, Optional, Sequence, TYPE_CHECKING, Union

import requests

__all__ = ["OpticsControl", "OpticsControlError"]

_LOGGER = logging.getLogger(__name__)

# Import for type hints only
if TYPE_CHECKING:
    from .VapixAPI import VapixAPI


class OpticsControlError(RuntimeError):
    """Raised when the camera returns an *error* member in JSON‑RPC response."""

    def __init__(self, message: str, *, code: Optional[int] = None, details: Any = None) -> None:
        self.code = code
        self.details = details
        super().__init__(message)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<OpticsControlError {self.code}: {self.args[0]!r}>"


class OpticsControl:
    """
    A class that provides an interface to interact with Axis cameras using the Optics Control API.

    Attributes:
    -----------
    api : VapixAPI
        The VapixAPI instance used for making requests.
    """

    #: Mapping of shorthand relative step identifiers to Optics Control API
    #: accepted values. Exposed so that library users can share constants
    #: across projects.
    RELATIVE_STEP = {
        "BIG_IN": "+bigStep",
        "SMALL_IN": "+smallStep",
        "BIG_OUT": "-bigStep",
        "SMALL_OUT": "-smallStep",
    }

    def __init__(self, api: VapixAPI) -> None:
        """
        Initializes the OpticsControl with a VapixAPI instance.

        Parameters:
        -----------
        api : VapixAPI
            The VapixAPI instance to use for making requests.
        """
        self.api = api

    def is_available(self) -> bool:
        """
        Checks if the optics are available.
        """
        try:
            self.get_optics()
            return True
        except Exception as e:
            return False

    def get_optics(self) -> Dict[str, Any]:
        """
        Gets information about all available optics.

        Returns:
        --------
        Dict[str, Any]
            A dictionary containing information about the optics.
        """
        return self.api._send_request_vanilla('opticscontrol.cgi', method="POST", json_data={
            "apiVersion": "1.2",
            "method": "getOptics"
        })

    def get_capabilities(self) -> Dict[str, Any]:
        """
        Gets information about the optics capabilities.

        Returns:
        --------
        Dict[str, Any]
            A dictionary containing information about the optics capabilities.
        """
        return self.api._send_request_vanilla('opticscontrol.cgi', method="POST", json_data={
            "apiVersion": "1.2",
            "method": "getCapabilities"
        })

    def set_focus(self, optics_id: Union[str, int], position: float) -> None:
        """
        Sets the focus position for the specified optics.

        Parameters:
        -----------
        optics_id : Union[str, int]
            The ID of the optics to set focus for.
        position : float
            The focus position to set (0.0 to 1.0).
        """
        self.api._send_request_vanilla('opticscontrol.cgi', method="POST", json_data={
            "apiVersion": "1.2",
            "method": "setFocus",
            "params": {
                "optics": [{
                    "opticsId": str(optics_id),
                    "position": position
                }]
            }
        })

    def set_relative_focus(self, optics_id: Union[str, int], step: str) -> None:
        """
        Changes the focus relative to the current position.

        Parameters:
        -----------
        optics_id : Union[str, int]
            The ID of the optics to adjust focus for.
        step : str
            The relative step to take ("+bigStep", "+smallStep", "-bigStep", "-smallStep").
        """
        self.api._send_request_vanilla('opticscontrol.cgi', method="POST", json_data={
            "apiVersion": "1.2",
            "method": "setRelativeFocus",
            "params": {
                "optics": [{
                    "opticsId": str(optics_id),
                    "type": step
                }]
            }
        })

    def set_magnification(self, optics_id: Union[str, int], magnification: float) -> None:
        """
        Sets the magnification for the specified optics.

        Parameters:
        -----------
        optics_id : Union[str, int]
            The ID of the optics to set magnification for.
        magnification : float
            The magnification value to set.
        """
        self.api._send_request_vanilla('opticscontrol.cgi', method="POST", json_data={
            "apiVersion": "1.2",
            "method": "setMagnification",
            "params": {
                "optics": [{
                    "opticsId": str(optics_id),
                    "magnification": magnification
                }]
            }
        })

    def set_relative_magnification(self, optics_id: Union[str, int], step: str) -> None:
        """
        Changes the magnification relative to the current position.

        Parameters:
        -----------
        optics_id : Union[str, int]
            The ID of the optics to adjust magnification for.
        step : str
            The relative step to take ("+bigStep", "+smallStep", "-bigStep", "-smallStep").
        """
        self.api._send_request_vanilla('opticscontrol.cgi', method="POST", json_data={
            "apiVersion": "1.2",
            "method": "setRelativeMagnification",
            "params": {
                "optics": [{
                    "opticsId": str(optics_id),
                    "type": step
                }]
            }
        })

    def calibrate(self, optics_id: Union[str, int], zoom: bool = True, focus: bool = True) -> None:
        """
        Calibrates the optics.

        Parameters:
        -----------
        optics_id : Union[str, int]
            The ID of the optics to calibrate.
        zoom : bool, optional
            Whether to calibrate zoom. Defaults to True.
        focus : bool, optional
            Whether to calibrate focus. Defaults to True.
        """
        self.api._send_request_vanilla('opticscontrol.cgi', method="POST", json_data={
            "apiVersion": "1.2",
            "method": "calibrate",
            "params": {
                "optics": [{
                    "opticsId": str(optics_id),
                    "zoom": zoom,
                    "focus": focus
                }]
            }
        })

    def reset(self, optics_id: Union[str, int], zoom: bool = False, focus: bool = True) -> None:
        """
        Resets the optics to their default position.

        Parameters:
        -----------
        optics_id : Union[str, int]
            The ID of the optics to reset.
        zoom : bool, optional
            Whether to reset zoom. Defaults to False.
        focus : bool, optional
            Whether to reset focus. Defaults to True.
        """
        self.api._send_request_vanilla('opticscontrol.cgi', method="POST", json_data={
            "apiVersion": "1.2",
            "method": "reset",
            "params": {
                "optics": [{
                    "opticsId": str(optics_id),
                    "zoom": zoom,
                    "focus": focus
                }]
            }
        })

    def set_focus_window(self, optics_id: Union[str, int], x: float, y: float, width: float, height: float) -> None:
        """
        Sets the window in which autofocus will optimize the focus.

        Parameters:
        -----------
        optics_id : Union[str, int]
            The ID of the optics to set focus window for.
        x : float
            The x-coordinate of the window's upper-left corner (0.0 to 1.0).
        y : float
            The y-coordinate of the window's upper-left corner (0.0 to 1.0).
        width : float
            The width of the window (0.0 to 1.0).
        height : float
            The height of the window (0.0 to 1.0).
        """
        self.api._send_request_vanilla('opticscontrol.cgi', method="POST", json_data={
            "apiVersion": "1.2",
            "method": "setFocusWindow",
            "params": {
                "optics": [{
                    "opticsId": str(optics_id),
                    "focusWindowUpperLeftX": x,
                    "focusWindowUpperLeftY": y,
                    "focusWindowWidth": width,
                    "focusWindowHeight": height
                }]
            }
        })

    def perform_autofocus(self, optics_id: Union[str, int]) -> None:
        """
        Starts an automatic focus search.

        Parameters:
        -----------
        optics_id : Union[str, int]
            The ID of the optics to perform autofocus for.
        """
        self.api._send_request_vanilla('opticscontrol.cgi', method="POST", json_data={
            "apiVersion": "1.2",
            "method": "performAutofocus",
            "params": {
                "optics": [{
                    "opticsId": str(optics_id)
                }]
            }
        })

    def set_temperature_compensation(self, optics_id: Union[str, int], enabled: bool) -> None:
        """
        Sets the state for the active temperature compensation.

        Parameters:
        -----------
        optics_id : Union[str, int]
            The ID of the optics to set temperature compensation for.
        enabled : bool
            Whether to enable temperature compensation.
        """
        self.api._send_request_vanilla('opticscontrol.cgi', method="POST", json_data={
            "apiVersion": "1.2",
            "method": "setTemperatureCompensation",
            "params": {
                "optics": [{
                    "opticsId": str(optics_id),
                    "enable": enabled
                }]
            }
        })

    def set_ir_cut_filter_state(self, optics_id: Union[str, int], state: str) -> None:
        """
        Sets the state for the IRCut filter.

        Parameters:
        -----------
        optics_id : Union[str, int]
            The ID of the optics to set IR cut filter state for.
        state : str
            The state to set ("on", "off", or "auto").
        """
        self.api._send_request_vanilla('opticscontrol.cgi', method="POST", json_data={
            "apiVersion": "1.2",
            "method": "setIrCutFilterState",
            "params": {
                "optics": [{
                    "opticsId": str(optics_id),
                    "state": state
                }]
            }
        })

    def set_ir_compensation(self, optics_id: Union[str, int], enabled: bool) -> None:
        """
        Sets the state for the active IR compensation.

        Parameters:
        -----------
        optics_id : Union[str, int]
            The ID of the optics to set IR compensation for.
        enabled : bool
            Whether to enable IR compensation.
        """
        self.api._send_request_vanilla('opticscontrol.cgi', method="POST", json_data={
            "apiVersion": "1.2",
            "method": "setIrCompensation",
            "params": {
                "optics": [{
                    "opticsId": str(optics_id),
                    "enable": enabled
                }]
            }
        })

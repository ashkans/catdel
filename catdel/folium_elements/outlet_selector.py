from typing import Union

from branca.element import Element, Html, IFrame, MacroElement
from jinja2 import Template

from folium.utilities import (
    escape_backticks,
)
class OutletSelector(MacroElement):
    """
    When one clicks on a Map that contains an OutletSelector,
    a Marker is created at the pointer's position and all other markers are removed.

    Parameters
    ----------
    popup: str or IFrame or Html, default None
        Text to display in the marker's popup.
        This can also be an Element like IFrame or Html.
        If None, the popup will display the marker's latitude and longitude.
        You can include the latitude and longitude with ${lat} and ${lng}.


    Examples
    --------
    >>> OutletSelector("<b>Lat:</b> ${lat}<br /><b>Lon:</b> ${lng}")

    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            // Function to clear all existing markers and add a new one
            function newMarker(e) {
                // Clear all markers
                {{this._parent.get_name()}}.eachLayer(function (layer) {
                    if (layer instanceof L.Marker) {
                        {{this._parent.get_name()}}.removeLayer(layer);
                    }
                });
                
                // Add new marker
                var new_mark = L.marker({draggable: false}).setLatLng(e.latlng).addTo({{this._parent.get_name()}});
                new_mark.dragging.enable();
                new_mark.on('dblclick', function(e) {
                    {{this._parent.get_name()}}.removeLayer(e.target)
                });
                new_mark.dragging.disable();

                var lat = e.latlng.lat.toFixed(4),
                    lng = e.latlng.lng.toFixed(4);
                
                new_mark.bindPopup({{ this.popup }}).openPopup();
            };

            // Bind the function to the map click event
            {{this._parent.get_name()}}.on('click', newMarker);
        {% endmacro %}
        """
    )  # noqa

    def __init__(self, popup: Union[IFrame, Html, str, None] = None):
        super().__init__()
        self._name = "OutletSelector"
        if isinstance(popup, Element):
            popup = popup.render()
        if popup:
            self.popup = "`" + escape_backticks(popup) + "`"
        else:
            self.popup = (
                '"<div style=\'font-size: 14px;\'>📍 Outlet Location:<br><b>Latitude:</b> " + lat + "<br><b>Longitude:</b> " + lng + "</div>"'
            )

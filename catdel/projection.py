from pyproj import Proj, Transformer

class Projection:
    def __init__(self, config) -> None:
        """
        Initializes the Projection with the destination and geographic coordinate reference systems (CRS).

        Args:
            config: A configuration object containing the destination and geographic CRS.
        """
        self.dst_crs = config.dst_crs
        self.geographic_crs = config.geographic_crs
        self.transformer_to_geo = Transformer.from_crs(self.dst_crs, self.geographic_crs)
        self.transformer_from_geo = Transformer.from_crs(self.geographic_crs, self.dst_crs)

    @property
    def folium_proj(self) -> str:
        """
        Gets the destination CRS formatted for use with Folium.

        Returns:
            str: The destination CRS without colons.
        """
        return self.dst_crs.replace(':', '')

    @property
    def pyproj(self) -> Proj:
        """
        Gets the Proj object for the destination CRS.

        Returns:
            Proj: The Proj object initialized with the destination CRS.
        """
        return Proj(self.dst_crs)

    def to_geo(self, x: float, y: float) -> tuple[float, float]:
        """
        Transforms coordinates from the destination CRS to the geographic CRS.

        Args:
            x (float): The x-coordinate in the destination CRS.
            y (float): The y-coordinate in the destination CRS.

        Returns:
            tuple[float, float]: The transformed coordinates in the geographic CRS.
        """
        try:
            return self.transformer_to_geo.transform(x, y)
        except Exception as e:
            raise ValueError(f"Error transforming coordinates to geographic CRS: {e}")

    def from_geo(self, x: float, y: float) -> tuple[float, float]:
        """
        Transforms coordinates from the geographic CRS to the destination CRS.

        Args:
            x (float): The x-coordinate in the geographic CRS.
            y (float): The y-coordinate in the geographic CRS.

        Returns:
            tuple[float, float]: The transformed coordinates in the destination CRS.
        """
        try:
            return self.transformer_from_geo.transform(x, y)
        except Exception as e:
            raise ValueError(f"Error transforming coordinates from geographic CRS: {e}")

    def transform_array_to_geo(self, arr: list[tuple[float, float]]) -> list[tuple[float, float]]:
        """
        Transforms an array of coordinates from the destination CRS to the geographic CRS.

        Args:
            arr (list[tuple[float, float]]): An array of coordinates in the destination CRS.

        Returns:
            list[tuple[float, float]]: An array of transformed coordinates in the geographic CRS.
        """
        try:
            return [self.to_geo(x, y) for x, y in arr]
        except Exception as e:
            raise ValueError(f"Error transforming array of coordinates to geographic CRS: {e}")

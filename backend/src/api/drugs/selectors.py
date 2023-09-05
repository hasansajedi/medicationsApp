import pandas as pd
from typing import Dict, Union

from fastapi import Depends, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.paginator import paginate
from pandas import DataFrame, Series

from src.api.dependencies.configuration import app_settings
from src.api.drugs.schemas.medication import DrugModel
from src.utils.pagination import CustomParams


class LoadDrugDataHelper:
    """
    Helper class to retrieve drugs data from a JSON file.

    Attributes:
        _MAIM_NODE_NAME (str): The main node name in the JSON data.
    """

    _MAIM_NODE_NAME = "drugs"

    @classmethod
    async def load_data_from_json_file(
        cls,
        params: CustomParams = Depends(),
        search: str = None,
    ) -> Page[DrugModel]:
        """
        Load drug data from a JSON file and apply pagination.

        Args:
            params (CustomParams): CustomParams instance for pagination.
            search (str, optional): A keyword for filtering the data by name or diseases.

        Returns:
            Page[DrugModel]: A paginated page of DrugModel instances.

        Raises:
            HTTPException: If an error occurs while loading the dataset.
        """
        try:
            df: DataFrame = await cls._load_data(app_settings.DATA_PATH, search)
            data: DataFrame = df.apply(cls.row_to_pydantic_model)
            paginated_result = paginate(list(data.values), params)
            return paginated_result
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Error occurred on loading dataset.",
            )

    @classmethod
    def row_to_pydantic_model(cls, row: Union[Dict, Series]):
        """
        Convert a row to a Pydantic DrugModel instance.

        Args:
            row (Union[Dict, Series]): A row from the DataFrame.

        Returns:
            DrugModel: A Pydantic DrugModel instance.
        """
        return DrugModel(**row)

    @classmethod
    async def _load_data(cls, data_path: str, search_keyword: str = None):
        """
        Load data from a JSON file and optionally filter it by search keyword.

        Args:
            data_path (str): The path to the JSON data file.
            search_keyword (str, optional): A keyword for filtering the data.

        Returns:
            DataFrame: The loaded and filtered data as a DataFrame.
        """
        df = pd.read_json(data_path)[cls._MAIM_NODE_NAME]
        drugs_df = pd.DataFrame(df)

        if not search_keyword:
            return drugs_df[cls._MAIM_NODE_NAME]

        columns_to_search = ["name", "diseases"]

        # Expand the "drugs" dictionary to access the nested columns
        for column in columns_to_search:
            drugs_df[column] = drugs_df[cls._MAIM_NODE_NAME].apply(
                lambda x: x.get(column)
            )

        def custom_search(row):
            for col in columns_to_search:
                if isinstance(row[col], list):
                    for item in row[col]:
                        if search_keyword.lower() in item.lower():
                            return True
                elif isinstance(row[col], str):
                    if search_keyword.lower() in row[col].lower():
                        return True
            return False

        filter_mask = drugs_df.apply(custom_search, axis=1)

        # Use the boolean mask to filter the DataFrame to get the matching rows
        filtered_df: DataFrame = drugs_df[filter_mask]
        return filtered_df[cls._MAIM_NODE_NAME]

import os
import pandas as pd

from superagentx.handler.base import BaseHandler
from superagentx.handler.decorators import tool


class DataWriterHandler(BaseHandler):
    """
    Handler class to write structured tabular data to a CSV file.
    Inherits from BaseHandler in SuperAgentX.
    """

    def __init__(self):
        super().__init__()  # Call the base handler constructor

    @tool
    async def csv_writer(self, data: list):
        """
        Asynchronously writes tabular data to a CSV file.

        This method is decorated with @tool so it can be used as a tool in a SuperAgentX engine.

        Example input:
            data = [
                {"Name": "Alice", "Age": 30},
                {"Name": "Bob", "Age": 25}
            ]

        Args:
            data (list): A list of dictionaries. Each dictionary represents one row,
                         and keys are treated as column headers.

        Returns:
            str: Status message indicating success or failure.
        """

        print("Writing Data in CSV using CSV Handler")

        if data:

            # Convert the list of dictionaries to a pandas DataFrame
            df = pd.DataFrame(data)

            # Define the output directory and filename
            output_dir = "output/datafiles"
            output_file = "product.csv"
            output_path = os.path.join(output_dir, output_file)

            # Ensure the directory exists; if not, create it
            os.makedirs(output_dir, exist_ok=True)

            # Save the DataFrame to a CSV file (no index column, include headers)
            df.to_csv(output_path, index=False, header=True)

            return "Successfully generated CSV data"

        # Fallback message if no data was provided
        return "Failed to create CSV"

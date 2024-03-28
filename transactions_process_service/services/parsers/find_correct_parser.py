import logging
import re
from typing import Any, List
from fastapi import UploadFile
import tabula
from transactions_process_service.schemas.transaction import Transaction
from transactions_process_service.services.parsers.file_parser import FileParser
from .parsers_dict import all_parsers
from .parser_exceptions import CorrectParserNotFound


class FindCorrectParser:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def find_parser(self, file: UploadFile) -> FileParser:
        try:
            df = tabula.io.read_pdf(
                file.file,
                multiple_tables=True,
                pages="1",
                pandas_options={"header": None},
                guess=False,
            )
            file.file.seek(0)
            for table in df:
                table_data: List = table.values.tolist()  # type: ignore
                for row in table_data:
                    # self.logger.debug(row)
                    for item in row:
                        if isinstance(item, str):
                            # self.logger.debug(item)
                            formatted_item = "".join(self._format_string(item).split(" "))
                            formatted_all_parsers = {
                                perm_key: value
                                for key, value in all_parsers.items()
                                for perm_key in self._get_all_versions_of_key(key)
                            }
                            self.logger.debug(
                                f" \nFormattes Item : {formatted_item} \nFormatted all Parsers : {formatted_all_parsers.keys()}"
                            )
                            for parser_key in formatted_all_parsers:
                                if parser_key in formatted_item:
                                    self.logger.info(
                                        f"Found correct parser: {formatted_all_parsers[parser_key]}"
                                    )
                                    return formatted_all_parsers[parser_key]
            raise CorrectParserNotFound(file)
        except Exception as e:
            raise e(f"In Find Correct Parser for file {file.filename} got this error: \n{str(e)}")
        finally:
            file.file.seek(0)
        
    def _format_string(self, string: str) -> str:
        text = string.lower()
        text = re.sub(
            r"[_\-]+", " ", text
        )  # Replace underscores, hyphens, and other special characters with spaces
        text = re.sub(
            r"[^\w\s]", " ", text
        )  # Remove any non-alphanumeric characters except spaces
        text = re.sub(
            r"\s+", " ", text
        ).strip()  # Optional: Collapse multiple spaces into one
        return text

    def _get_all_versions_of_key(self, key: str) -> List[str]:
        from itertools import permutations

        key = self._format_string(key)
        return ["".join(list(p)) for p in permutations(key.split(" "))]

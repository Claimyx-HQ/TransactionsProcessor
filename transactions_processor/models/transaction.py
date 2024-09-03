from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Any, List, Union
import logging
import re
import hashlib
import uuid


logger = logging.getLogger(__name__)


class Transaction(BaseModel):
    date: datetime = Field(..., description="Transaction date")
    description: str = Field(..., description="Description of the transaction")
    amount: float = Field(..., description="Transaction amount")
    uuid: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for the transaction",
    )
    batch_number: int | None = Field(None, description="Optional batch number")
    origin: str | None = Field(None, description="Optional origin of the transaction")

    def __getitem__(self, item):
        return getattr(self, item)

    def to_dict(self):
        return {
            "uid": self.get_uid(),
            "date": self.date.strftime("%m-%d-%Y"),
            "description": self.description,
            "amount": self.amount,
            "batch_number": self.batch_number,
            "origin": self.origin,
        }

    @field_validator("date")
    def validate_date(cls, date: Union[str, datetime]) -> datetime:  # type: ignore
        date_pattern = re.compile(r"^\d{1,2}[-/.]\d{1,2}([-/.]\d{2,4})?$")

        if isinstance(date, str) and date_pattern.match(date):
            try:
                for fmt in (
                    "%m/%d/%y",
                    "%m-%d-%y",
                    "%m.%d.%y",
                    "%m/%d/%Y",
                    "%m-%d-%Y",
                    "%m.%d.%Y",
                ):
                    # logger.debug(f"trying date {date} with format {fmt}")
                    try:
                        return datetime.strptime(date, fmt)
                    except Exception as e:
                        # logger.exception(e)
                        pass
                for fmt in ("%m/%d", "%m-%d", "%m.%d"):
                    try:
                        parsed_date = datetime.strptime(date, fmt)
                        current_year = (
                            datetime.now().year
                        )  # Use the current year initially
                        parsed_date = parsed_date.replace(year=current_year)
                        # Check if the resulting date is in the future compared to today's date
                        if parsed_date > datetime.now():
                            # If the date is in the future, it means the transaction happened last year
                            parsed_date = parsed_date.replace(year=current_year - 1)
                        return parsed_date
                    except Exception as e:
                        # logger.exception(e)
                        pass
            except:
                raise ValueError("Date not found or incorrect format")
        elif isinstance(date, datetime):
            return date
        else:
            raise ValueError("Invalid date format")

    @field_validator("description")
    def validate_description(cls, description: Any) -> str:
        if isinstance(description, str):
            if not re.match(r"^\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4}$", description):
                return description.strip(" '")
            raise ValueError("Description not found")
        return str(description)

    @field_validator("amount")
    def validate_amount(cls, amount: Union[str, float, int]) -> float:
        if isinstance(amount, (float, int)):
            return float(amount)
        elif isinstance(amount, str):
            try:
                return float(amount.replace(",", ""))
            except ValueError:
                raise ValueError("Amount not found or is not a number")

    def get_uid(self) -> str:
        uid_data = (
            f"{self.date.strftime('%Y%m%d')}{self.description}{self.amount}{self.uuid}"
        )
        return hashlib.sha256(uid_data.encode()).hexdigest()[:8]

    @classmethod
    def from_raw_data(cls, raw_data: List[Union[str, float, int]]):
        date, description, amount, batch_number, origin = None, None, None, None, None

        for value in raw_data:
            if date is None:
                try:
                    # logger.debug(f"trying value {value} for date")
                    date = cls.validate_date(value)  # type: ignore
                    # logger.debug(f"value {value} accepted for date")
                    continue
                except ValueError:
                    # logger.exception(f"Invalid date: {value}")
                    pass

            if amount is None:
                try:
                    # logger.debug(f"trying value {value} for amount")
                    amount = cls.validate_amount(value)  # type: ignore
                    # logger.debug(f"value {value} accepted for amount")
                    continue
                except ValueError:
                    # logger.exception(f"Invalid amount: {value}")
                    pass

            if description is None:
                try:
                    # logger.debug(f"trying value {value} for description")
                    description = cls.validate_description(value)  # type: ignore
                    # logger.debug(f"value {value} accepted for description")
                    continue
                except ValueError:
                    # logger.exception(f"Invalid description: {value}")
                    pass
            if batch_number is None:
                try:
                    batch_number = int(value)  # Treat value as batch number
                    continue
                except (ValueError, TypeError):
                    pass
            if origin is None:
                try:
                    origin = str(value)  # Treat value as origin
                    continue
                except (ValueError, TypeError):
                    pass

        if date is None or description is None or amount is None:
            logger.error(
                f"Invalid input data: {raw_data} and date: {date} description: {description} amount: {amount}"
            )
            raise ValueError(f"Invalid input data: {raw_data} and date: {date} description: {description} amount: {amount}")

        return cls(
            date=date,
            description=description,
            amount=amount,
            batch_number=batch_number,
            origin=origin,
        )

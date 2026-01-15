
# aade-publicity-search

Python client for the **AADE Public AFM (VAT) lookup service**, using the official SOAP API.
It allows you to retrieve publicly available company / professional information by AFM
and returns the result as a Python dictionary (JSON-ready).

---

## Features

- 🔎 AFM (VAT) public lookup
- 🇬🇷 Official AADE SOAP service
- ⚡ Async / `httpx` based
- 🧼 Clean JSON output (dict)
- 🚫 No FastAPI dependency
- 🐍 Python 3.10+

---

## Installation

You can install the package via PyPI or directly from the GitHub repository using **pip** or **uv**.

### From pypi
```bash
# Using pip
pip install aade-publicity-search
# Using uv
uv pip install aade-publicity-search
```

### From Github
```bash
# Using pip
pip install git+https://github.com/gioiliop7/aade-publicity-search.git
# Using uv
uv pip install git+https://github.com/gioiliop7/aade-publicity-search.git
```

### Usage Example
```python
import asyncio
from aade_publicity_search import AadeClient

async def main():
    client = AadeClient(
        username="AADE_USERNAME",
        password="AADE_PASSWORD"
    )

    data = await client.get_vat_info("123456789")
    # Always check for error.
    if not data["success"]:
        print(f"Error: {data['error']}")
    else:
        print(data)

asyncio.run(main())
```

## Returned data structure

The client returns a dictionary similar to:

```json
{
    "success": true,
    "error": {
        "code": null,
        "description": null
    },
    "basic": {
        "afm": "123456789",
        "name": "COMPANY NAME",
        "doy": "ΔΟΥ ΑΘΗΝΩΝ",
        "legal_status": "ΑΤΟΜΙΚΗ ΕΠΙΧΕΙΡΗΣΗ"
    },
    "firm_activities": [
        {
            "activity_code": "62010000",
            "activity_descr": "Computer programming activities"
        }
    ]
}
```

----------

## AFM validation

AFM numbers are validated locally before calling the AADE service.
If the AFM is invalid, a `ValueError` is raised.

----------

## Error handling

-   HTTP errors raise `httpx.HTTPStatusError`

-   Invalid AFM raises `ValueError`

-   AADE service errors are returned in the `error` field of the response


----------

## Requirements

-   Python 3.10+

-   Valid AADE SOAP credentials

-   Internet access to AADE services
----------

## Disclaimer

This library uses the **official AADE public SOAP service**.
It is not affiliated with or endorsed by AADE.

Use responsibly and according to AADE terms of service.

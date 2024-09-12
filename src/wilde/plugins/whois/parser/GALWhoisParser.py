from typing import Optional

from wilde.plugins.whois.parser.WhoisParser import WhoisParser

_PREFIX: str = "Whois Refer#"  # Global prefix for all keys
_ORG_PREFIX: str = "Organisation"  # Prefix for organisation blocks
_CONTACT_PREFIX: str = "Contact"  # Prefix for contact blocks


class GALWhoisParser(WhoisParser):

    def parse_response(self, response: str) -> Optional[dict[str, str]]:
        # Split the response into lines
        lines = response.split('\n')

        # Initialize variables
        result_dict: dict[str, str] = {}
        last_key: Optional[str] = None
        key_counter: Optional[int] = None

        # Function to add a field to the resulting dictionary
        def add_field(field_key: str, field_value: str, field_key_counter: Optional[int]):
            if field_key_counter is None:
                block_key = f"{_PREFIX}{field_key}"
            else:
                block_key = f"{_PREFIX}{field_key}_{field_key_counter}"
            result_dict[block_key] = field_value

        # Process each line
        for line in lines:
            line = line.strip()

            # Skip blank lines
            if not line:
                continue
            
            if ":" in line and line.index(":") > 0:
                # Split key and value
                key, value = line.split(":", 1)

                if key == "Name Server":
                    key = "nserver"

                key = key.strip().lower()
                value = value.strip()

                # Handle cases of repeated values
                if last_key == key and key_counter is not None:
                    key_counter += 1

                elif last_key == key and key_counter is None:
                    key_counter = 1
                else:
                    key_counter = None

                last_key = key
                add_field(key, value, key_counter)

        return result_dict

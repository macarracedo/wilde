from wilde.plugins.whois.parser.WhoisParser import WhoisParser
from typing import Optional

_PREFIX: str = "Whois IANA#"    # Global prefix for all keys
_ORG_PREFIX: str = "Organisation"   # Prefix for organisation blocks
_CONTACT_PREFIX: str = "Contact"    # Prefix for contact blocks


class IANAWhoisParser(WhoisParser):

    def parse_response(self, response: str) -> Optional[dict[str, str]]:
        # Split the response into lines
        lines = response.split('\n')

        # Initialize variables
        result_dict: dict[str, str] = {}
        current_block: Optional[str] = None
        block_count: dict[str, int] = {}
        last_key: Optional[str] = None
        key_counter: Optional[int] = None

        # Function to add a field to the resulting dictionary
        def add_field(field_key: str, field_value: str, field_key_counter: Optional[int] = 0):
            if current_block and field_key_counter is None:
                block_key = f"{_PREFIX}{current_block} {block_count[current_block]}#{field_key}"
            elif current_block and field_key_counter is not None:
                block_key = f"{_PREFIX}{current_block} {block_count[current_block]}#{field_key}_{field_key_counter}"
            elif field_key_counter is None:
                block_key = f"{_PREFIX}{field_key}"
            else:
                block_key = f"{_PREFIX}{field_key}_{field_key_counter}"
            result_dict[block_key] = field_value

        # Process each line
        for line in lines:
            line = line.strip()

            # Skip blank lines and lines starting with '%'
            if not line or line.startswith('%'):
                continue

            # Identify organisation blocks
            if line.startswith("organisation:"):
                if current_block is _ORG_PREFIX:
                    block_count[current_block] += 1
                elif current_block is not _CONTACT_PREFIX:
                    current_block = _ORG_PREFIX

                if current_block not in block_count:
                    block_count[current_block] = 1

            # Identify contact blocks
            if line.startswith("contact:"):
                if current_block is _CONTACT_PREFIX:
                    block_count[current_block] += 1
                else:
                    current_block = _CONTACT_PREFIX

                if current_block not in block_count:
                    block_count[current_block] = 1

            # Close any block once nservers are found. No block should include nservers
            if line.startswith("nserver:"):
                if current_block is not None:
                    current_block = None

            # Split key and value
            key, value = line.split(":", 1)
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

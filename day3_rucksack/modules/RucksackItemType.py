import re


class RucksackItemType:
    _type_regex = re.compile('[A-Za-z]')

    def __init__(self, type_symbol):
        if not len(type_symbol) == 1:
            raise Exception("Invalid rucksack item type symbol, must be only 1 character")
        if not re.fullmatch('[A-Za-z]', type_symbol):
            raise Exception('Invalid rucksack item type symbol, must be upper or lower case alphabet letters only')
        self._type_symbol = type_symbol

    def __str__(self) -> str:
        return self.type_symbol()

    def __eq__(self, o: object) -> bool:
        return isinstance(o, RucksackItemType) and o.type_symbol() == self.type_symbol()

    def __hash__(self) -> int:
        return hash(self.type_symbol())

    def type_symbol(self):
        return self._type_symbol

    def priority(self):
        # in the type priority 'A' maps to 27 and in the ascii table ord('A') maps to 65
        upper_case_offset_from_ord = ord('A') - 27
        # in the type priority 'a' maps to 1 and in the ascii table ord('a') maps to 97
        lower_case_offset_from_ord = ord('a') - 1
        if self.type_symbol().isupper():
            return ord(self.type_symbol()) - upper_case_offset_from_ord
        else:
            return ord(self.type_symbol()) - lower_case_offset_from_ord

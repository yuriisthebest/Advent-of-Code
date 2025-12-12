from typing import Any


class Tags:
    def __init__(self):
        self.__tags = {}

    def get(self, tag_name: str) -> Any:
        """
        Get the value of a given tag.
        or None if the Cell does not have the tag.

        :param tag_name: The tag key
        :return: Value of the tag key or None if tag does not exist
        """
        return self.__tags[tag_name] if self.has_tag(tag_name) else None

    def get_all_tags(self) -> dict:
        """
        Get the full tag dictionary

        :return: Dictionary containing all key-values pairs of this object
        """
        return self.__tags

    def has_tag(self, tag_name: str) -> bool:
        """
        Checks if the cell has a given tag
        """
        return tag_name in self.__tags

    def update_tag(self, new_tags: dict) -> None:
        """
        Update multiple tags of the cell with the given key-values.
        Maintains all other current tags of the cell.

        Does nothing if no valid tags are given
        """
        if isinstance(new_tags, dict):
            self.__tags.update(new_tags)

class Typed:
    """
    Descriptor that enforces type checking for attributes.
    """

    def __init__(self, expected_type: type) -> None:
        if not isinstance(expected_type, type):
            raise TypeError("expected_type must be a type")

        self.expected_type = expected_type
        self.storage_name = None

    def __set_name__(self, owner, name: str) -> None:
        """
        Called automatically when the descriptor is assigned
        to a class attribute.
        """
        self.storage_name = f"_{type(self).__name__}__{name}"

    def __get__(self, instance, owner=None):
        """
        Retrieve the stored value.
        """
        if instance is None:
            return self

        if self.storage_name is None:
            raise AttributeError(
                "Descriptor has not been assigned to a class"
            )

        try:
            return instance.__dict__[self.storage_name]

        except KeyError as error:
            raise AttributeError(
                "Managed attribute has not been assigned"
            ) from error

    def __set__(self, instance, value) -> None:
        """
        Validate type before storing value.
        """
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"Expected {self.expected_type.__name__}, "
                f"got {type(value).__name__}"
            )

        instance.__dict__[self.storage_name] = value


# ---------------------------------
# Example Usage
# ---------------------------------

class Person:
    name = Typed(str)
    age = Typed(int)

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age


# Test Code
if __name__ == "__main__":

    person = Person("Stephen Sunguro", 35)

    print("Name:", person.name)
    print("Age:", person.age)

    print("\nUpdating age...")
    person.age = 36
    print("New Age:", person.age)

    print("\nTrying invalid assignment...")

    try:
        person.age = "Thirty Six"
    except TypeError as e:
        print("Error:", e)
``
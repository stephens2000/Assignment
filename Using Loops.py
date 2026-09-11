def product_of_multiples(factor: int, limit: int) -> int:
    """
    Returns the product of all multiples of 'factor'
    that are less than or equal to 'limit'.

    Example:
        product_of_multiples(3, 12)
        = 3 × 6 × 9 × 12
        = 1944
    """

    if not isinstance(factor, int) or isinstance(factor, bool):
        raise TypeError("factor must be an integer")

    if not isinstance(limit, int) or isinstance(limit, bool):
        raise TypeError("limit must be an integer")

    if factor <= 0:
        raise ValueError("factor must be greater than zero")

    if limit < factor:
        return 0

    product = 1

    for number in range(factor, limit + 1, factor):
        product *= number

    return product


# --------------------------
# Test Cases
# --------------------------

if __name__ == "__main__":

    print("Test 1:")
    print(product_of_multiples(3, 12))
    # 3 × 6 × 9 × 12 = 1944

    print("\nTest 2:")
    print(product_of_multiples(5, 20))
    # 5 × 10 × 15 × 20 = 15000

    print("\nTest 3:")
    print
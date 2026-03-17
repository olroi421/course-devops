"""
Тести для модуля розрахунку знижок.
Запуск: pytest tests/ -v
"""

from decimal import Decimal

import pytest
from src.discount import CustomerType, apply_discount, calculate_discount
# from src.discount_refactored_with_bug import calculate_discount, apply_discount, CustomerType


class TestCalculateDiscount:
    """Варіант 1 — покривають основну логіку."""

    def test_no_discount_for_regular_customer(self):
        # Arrange
        amount = Decimal("100.00")
        # Act
        result = calculate_discount(amount, CustomerType.REGULAR)
        # Assert
        assert result == Decimal("0.00")

    def test_ten_percent_for_premium(self):
        amount = Decimal("100.00")
        result = calculate_discount(amount, CustomerType.PREMIUM)
        assert result == Decimal("10.00")

    def test_twenty_percent_for_vip(self):
        amount = Decimal("100.00")
        result = calculate_discount(amount, CustomerType.VIP)
        assert result == Decimal("20.00")

    @pytest.mark.parametrize(
        "amount, customer_type, expected",
        [
            (Decimal("50.00"), CustomerType.REGULAR, Decimal("0.00")),
            (Decimal("50.00"), CustomerType.PREMIUM, Decimal("5.00")),
            (Decimal("50.00"), CustomerType.VIP, Decimal("10.00")),
            (Decimal("200.00"), CustomerType.PREMIUM, Decimal("20.00")),
            (Decimal("0.00"), CustomerType.VIP, Decimal("0.00")),
        ],
    )
    def test_various_scenarios(self, amount, customer_type, expected):
        assert calculate_discount(amount, customer_type) == expected

    def test_raises_for_negative_amount(self):
        with pytest.raises(ValueError, match="від'ємною"):
            calculate_discount(Decimal("-10.00"), CustomerType.REGULAR)


class TestApplyDiscount:
    """Варіант 1 — перевіряють фінальну суму після знижки."""

    def test_regular_pays_full_price(self):
        result = apply_discount(Decimal("100.00"), CustomerType.REGULAR)
        assert result == Decimal("100.00")

    def test_premium_pays_ninety(self):
        result = apply_discount(Decimal("100.00"), CustomerType.PREMIUM)
        assert result == Decimal("90.00")

    def test_vip_pays_eighty(self):
        result = apply_discount(Decimal("100.00"), CustomerType.VIP)
        assert result == Decimal("80.00")

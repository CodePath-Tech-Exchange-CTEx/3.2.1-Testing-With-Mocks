from src.example.expense_report import Expense, parse_expenses, summarize_by_category


def test_parse_expenses_creates_objects():
    rows = [
        {"category": "travel", "amount": 100},
        {"category": "food", "amount": 50.5},
    ]

    expenses = parse_expenses(rows)

    assert len(expenses) == 2
    assert expenses[0] == Expense(category="travel", amount=100.0)
    assert expenses[1] == Expense(category="food", amount=50.5)


def test_summarize_by_category_groups_and_sums():
    expenses = [
        Expense(category="travel", amount=100),
        Expense(category="travel", amount=50),
        Expense(category="food", amount=25),
    ]

    summary = summarize_by_category(expenses)

    assert summary == {"travel": 150.0, "food": 25.0}


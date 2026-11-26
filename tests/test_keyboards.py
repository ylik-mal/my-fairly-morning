
from app.keyboards.checkin import habits_keyboard, status_keyboard


def test_habits_keyboard_empty():
    """Если привычек нет, кнопок тоже нет."""
    keyboard = habits_keyboard([], [])

    assert keyboard.inline_keyboard == []


def test_habits_keyboard_without_checkins():
    """Неотмеченная привычка отображается с пустым кружком."""
    keyboard = habits_keyboard([(1, "Выпить воды")], {})

    button = keyboard.inline_keyboard[0][0]

    assert button.text == "⭕ Выпить воды"
    assert button.callback_data == "checkin:1"


def test_habits_keyboard_done():
    """Выполненная привычка получает зелёную отметку."""
    keyboard = habits_keyboard([(2, "Зарядка")], {2: "done"})

    button = keyboard.inline_keyboard[0][0]

    assert button.text == "✅ Зарядка"
    assert button.callback_data == "checkin:2"


def test_habits_keyboard_skipped():
    """Пропущенная привычка получает отдельный значок."""
    keyboard = habits_keyboard([(3, "Чтение")], {3: "skipped"})

    button = keyboard.inline_keyboard[0][0]

    assert button.text == "⏭ Чтение"


def test_habits_keyboard_long_title():
    """Длинное название обрезается до 20 символов."""
    title = "Очень длинное название привычки"
    keyboard = habits_keyboard([(4, title)], {})

    button = keyboard.inline_keyboard[0][0]

    assert button.text == "⭕ " + title[:19] + "…"


def test_habits_keyboard_multiple():
    """Каждая привычка размещается в отдельной строке."""
    habits = [(1, "Вода"), (2, "Спорт"), (3, "Чтение")]
    keyboard = habits_keyboard(habits, {})

    assert len(keyboard.inline_keyboard) == 3

    for row in keyboard.inline_keyboard:
        assert len(row) == 1


def test_status_keyboard():
    """Клавиатура содержит кнопки выполнения, пропуска и возврата."""
    keyboard = status_keyboard(7)

    buttons = [
        button
        for row in keyboard.inline_keyboard
        for button in row
    ]

    assert [button.text for button in buttons] == [
        "✅ Сделано",
        "⏭ Пропустить",
        "⬅️ Назад",
    ]

    assert [button.callback_data for button in buttons] == [
        "set:done:7",
        "set:skipped:7",
        "back:today",
    ]

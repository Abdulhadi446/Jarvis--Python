def count(noString):
    No = 0
    try:
        No = eval(noString)  # Evaluates expressions like "1 + 2" to 3
        return str(No)
    except Exception:
        return noString

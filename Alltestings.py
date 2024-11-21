def execute_code(code: str):
    """Execute Python code provided by the user."""
    local_vars = {}
    try:
        exec(code, {}, local_vars)
    except Exception as e:
        return {"error": str(e)}
    
    return local_vars
def execite(a):
    ans = execute_code(a)
    if ans == '' or a == '':
        return ans
    else:
        return str("")

if __name__ == "__main__":
    while True:
        execite(input(""))

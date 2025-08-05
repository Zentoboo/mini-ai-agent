from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

def run_tests():
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))
    print(get_file_content("calculator", "pkg/does_not_exist.py"))
if __name__ == "__main__":
    run_tests()

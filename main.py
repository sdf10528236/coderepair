from compiler.fix_printf_scanf import auto_fix_str
from model_test.model_fix import auto_model_fix
from compiler.compiler_mesg import compiler_mesg

if __name__ == '__main__':

    filename = "c1.c"
    folder_path = f'D:/program projects/coderepair/data/correct_data/{filename}'
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(compiler_mesg(folder_path))
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
    auto_fix_str(folder_path, filename)
    auto_model_fix(folder_path, filename)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
    print(compiler_mesg(folder_path))
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

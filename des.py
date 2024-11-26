
from des_table import *

# 初始置换函数
def initial_permutation_func(plain_txt):
    # 将 16 进制的明文转换为二进制
    plain_txt = bin(int(plain_txt, 16))[2:].zfill(64)
    # 进行初始置换
    cipher_txt = ""
    for index in IP:
        cipher_txt += plain_txt[index - 1]
    return cipher_txt

# 扩展置换函数
def expansion_permutation_func(r_value):
    # 进行扩展置换
    r_result = ""
    for index in E:
        r_result += r_value[index - 1]
    return r_result

# S 盒置换函数
def s_box_func(r):
    # 将 48 位的数据分为 8 组，每组 6 位
    r = [r[i:i + 6] for i in range(0, 48, 6)]
    # 保存 S 盒置换后的结果
    result_txt = ""
    # 遍历每一组数据
    for i in range(8):
        # 计算行号和列号
        row = int(r[i][0] + r[i][-1], 2)
        col = int(r[i][1:-1], 2)
        # 从 S 盒中取出对应的值
        value = S[i][row][col]
        # 将取出的值转换为 4 位的二进制
        binary_value = ""
        for j in range(3, -1, -1):
            binary_value += '1' if (value & (1 << j)) else '0'
        # 将结果保存到 result_txt 中
        result_txt += binary_value
    return result_txt

# P 置换函数
def permutation_func(r):
    # 进行 P 置换
    r_result = ""
    for index in P:
        r_result += r[index - 1]
    return r_result

# 生成 16 轮的子密钥
def generate_key_schedule_func(key):
    # 将 16 进制的密钥转换为二进制
    key = bin(int(key, 16))[2:]
    # 将密钥填充到 64 位
    key = key.zfill(64)
    # 进行 PC-1 置换
    key_result = ""
    for index in PC_1:
        key_result += key[index - 1]
    # 生成 16 轮的子密钥
    key_schedule_list = []
    for i in range(16):
        # 将密钥分为左右两部分
        c_part = key_result[:28]
        d_part = key_result[28:]
        # 循环左移
        if i in [0, 1, 8, 15]:
            c_part = c_part[1:] + c_part[0]
            d_part = d_part[1:] + d_part[0]
        else:
            c_part = c_part[2:] + c_part[:2]
            d_part = d_part[2:] + d_part[:2]
        # 进行 PC-2 置换
        key_result = c_part + d_part
        key_final = ""
        for j in PC_2:
            key_final += key_result[j - 1]
        key_schedule_list.append(key_final)
    return key_schedule_list

# 加密模式
def encrypt_func(plain_txt, key_value):
    # 进行初始置换
    plain_txt = initial_permutation_func(plain_txt)
    # 生成子密钥
    key_list = generate_key_schedule_func(key_value)
    # 进行 16 轮运算
    for i in range(16):
        # 将明文前 32 位和后 32 位分开
        l_part = plain_txt[:32]
        r_part = plain_txt[32:]
        l_next = r_part
        # 扩展置换
        r_part = expansion_permutation_func(r_part)
        # 异或子密钥
        r_part = ''.join(['1' if r_part[j]!= key_list[i][j] else '0' for j in range(48)])
        # S 盒置换
        r_part = s_box_func(r_part)
        # P 置换
        r_part = permutation_func(r_part)
        # 异或左半部分
        r_part = ''.join(['1' if r_part[j]!= l_part[j] else '0' for j in range(32)])
        # 拼接
        plain_txt = l_next + r_part
    # 交换前后 32 位
    plain_txt = plain_txt[32:] + plain_txt[:32]
    # 逆初始置换得到密文
    cipher_txt = ""
    for index in inverse_IP:
        cipher_txt += plain_txt[index - 1]
    # 转换为 16 进制
    cipher_hex = hex(int(cipher_txt, 2))[2:].zfill(16).upper()
    return cipher_hex

# 解密模式
def decrypt_func(plain_txt, key_value):
    # 进行初始置换
    plain_txt = initial_permutation_func(plain_txt)
    # 生成子密钥
    key_list = generate_key_schedule_func(key_value)
    # 进行 16 轮运算
    for i in range(16):
        # 将明文前 32 位和后 32 位分开
        l_part = plain_txt[:32]
        r_part = plain_txt[32:]
        l_next = r_part
        # 扩展置换
        r_part = expansion_permutation_func(r_part)
        # 异或子密钥
        r_part = ''.join(['1' if r_part[j]!= key_list[15 - i][j] else '0' for j in range(48)])
        # S 盒置换
        r_part = s_box_func(r_part)
        # P 置换
        r_part = permutation_func(r_part)
        # 异或左半部分
        r_part = ''.join(['1' if r_part[j]!= l_part[j] else '0' for j in range(32)])
        # 拼接
        plain_txt = l_next + r_part
    # 交换前后 32 位
    plain_txt = plain_txt[32:] + plain_txt[:32]
    # 逆初始置换得到密文
    cipher_txt = ""
    for index in inverse_IP:
        cipher_txt += plain_txt[index - 1]
    # 转换为 16 进制
    cipher_hex = hex(int(cipher_txt, 2))[2:].zfill(16).upper()
    return cipher_hex

# DES 函数
def des_function(plain_txt, key_value, mode_num):
    if mode_num == 0:
        plain_txt = encrypt_func(plain_txt, key_value)
    else:
        plain_txt = decrypt_func(plain_txt, key_value)
    return plain_txt

if __name__ == "__main__":
    try:
        # 从指定的文件中读入明文和密钥，16 进制
        with open("input_data_des.txt", "r") as file_obj:
            plain_text = file_obj.readline().strip()
            key = file_obj.readline().strip()

        # 询问是加密还是解密
        while True:
            try:
                mode = int(input("请输入模式(0 表示加密，1 表示解密): "))
                if mode in [0, 1]:
                    break
                else:
                    print("输入错误，请输入 0 或 1。")
            except ValueError:
                print("输入错误，请输入整数。")

        result = des_function(plain_text, key, mode)

        # 根据模式将结果写入不同的文件
        if mode == 0:
            with open("encrypted_output_des.txt", "w", encoding= 'utf-8') as encrypted_file:
                encrypted_file.write(result + "\n")
                encrypted_file.write("mode: 0 (加密)\n")
                encrypted_file.write("plain_text: " + plain_text + "\n")
                encrypted_file.write("key: " + key + "\n")
            print("加密结果已保存到 encrypted_output_des.txt 文件中。")
        else:
            with open("decrypted_output_des.txt", "w", encoding= 'utf-8') as decrypted_file:
                decrypted_file.write(result + "\n")
                decrypted_file.write("mode: 1 (解密)\n")
                decrypted_file.write("plain_text: " + plain_text + "\n")
                decrypted_file.write("key: " + key + "\n")
            print("解密结果已保存到 decrypted_output_des.txt 文件中。")

    except FileNotFoundError:
        print("文件不存在，请检查文件路径。")
    except Exception as e:
        print(f"发生错误：{e}")    
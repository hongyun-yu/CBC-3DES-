from des import *

# 填充函数
def ansi_x923_padding_func(plain_txt):
    # 计算需要填充的长度
    pad_len = (16 - len(plain_txt) % 16) // 2
    if pad_len!= 0:
        plain_txt += (pad_len * 2 - 1) * "0" + str(pad_len)
    return plain_txt

# ANSI X9.23 去除填充函数
def ansi_x923_unpad_func(data_txt):
    pad_len = int(data_txt[-1]) * 2
    return data_txt[:-pad_len]

# 3DES 函数
def triple_des_func(plain_text, k1, k2, k3, mode, init_vector):
    # 3DES 加密
    if mode == 0:
        plain_text = ansi_x923_padding_func(plain_text)
        plain_text_xor_val = init_vector
        encrypted_result = ""
        for i in range(0, len(plain_text), 16):
            # 3DES 函数
            print("第%d 次加密" % (i // 16 + 1))
            plain_text_part = plain_text[i:i + 16]
            print("plain_text_part:", plain_text_part)
            # plain_text_part 与 init_vector 异或
            plain_text_part = hex(int(plain_text_part, 16) ^ int(plain_text_xor_val, 16))[2:]
            plain_text_part = str(plain_text_part)
        # 3DES 加密过程
        cipher_text = des_function(plain_text, k1, 0)
        cipher_text = des_function(cipher_text, k2, 1)
        cipher_text = des_function(cipher_text, k3, 0)
        encrypted_result += cipher_text.upper()
        plain_text_xor_val = cipher_text

        with open("encrypted_output_triple_des_file.txt", "w", encoding = 'utf-8') as encrypted_output_file:
                encrypted_output_file.write(encrypted_result + "\n")
                encrypted_output_file.write("mode: " + str(mode) + "（加密） \n")
                encrypted_output_file.write("iv: " + init_vector + "\n")
                encrypted_output_file.write("text: " + plain_text + "\n")
                encrypted_output_file.write("key1: " + k1 + "\n")
                encrypted_output_file.write("key2: " + k2 + "\n")
                encrypted_output_file.write("key3: " + k3 + "\n")

        #print("加密结果已保存到 encrypted_output_triple_des_file.txt 文件中。")
        
        return cipher_text
    # 3DES 解密
    else:
        # 3DES 解密过程
        plain_text_xor_val = init_vector
        decrypted_result = ""
        for i in range(0, len(plain_text), 16):
        # 3DES 函数
            #print("第 %d 次解密" % (i // 16 + 1))
            plain_text_part = plain_text[i:i + 16]
            #print("text_part:", plain_text_part)
        plain_text = des_function(plain_text, k3, 1)
        plain_text = des_function(plain_text, k2, 0)
        plain_text = des_function(plain_text, k1, 1)
         # partial_res 与 init_vector 异或
        partial_res = plain_text
        partial_res = hex(int(partial_res, 16) ^ int(plain_text_xor_val, 16))[2:]
        partial_res = partial_res.zfill(16)
        decrypted_result += partial_res.upper()
        plain_text_xor_val = plain_text_part

        decrypted_result = ansi_x923_unpad_func(decrypted_result)

        with open("decrypted_output_triple_des_file.txt", "w",encoding = 'utf-8') as decrypted_output_file:
            decrypted_output_file.write(decrypted_result + "\n")
            decrypted_output_file.write("mode: " + str(mode) + " （解密）\n")
            decrypted_output_file.write("iv: " + init_vector + "\n")
            decrypted_output_file.write("text: " + plain_text + "\n")
            decrypted_output_file.write("key1: " + k1 + "\n")
            decrypted_output_file.write("key2: " + k2 + "\n")
            decrypted_output_file.write("key3: " + k3 + "\n")

        #    print("解密结果已保存到 decrypted_output_triple_des_file.txt 文件中。")
        return plain_text
    

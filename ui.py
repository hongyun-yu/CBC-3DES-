from des import *
from triple_des import *
import tkinter as tk
from tkinter import filedialog

def encrypt_decrypt():
    try:
        # 获取输入的内容和选择的模式
        plain_text = plain_text_entry.get()
        keys = []
        if des_3des_var.get() == 0:
            key = key_entry.get()
            keys.append(key)
        else:
            for i in range(1, 4):
                key = eval(f'key{i}_entry.get()')
                keys.append(key)
        mode = mode_var.get()
        init_vector = None
        if des_3des_var.get() == 1:
            init_vector = iv_entry.get()

        if des_3des_var.get() == 0:
            result = des_function(plain_text, keys[0], mode)
            if mode == 0:
                file_name = "encrypted_output_des.txt"
            else:
                file_name = "decrypted_output_des.txt"
        else:
            key1, key2, key3 = keys
            result = triple_des_func(plain_text, key1, key2, key3, mode, init_vector)
            if mode == 0:
                file_name = "encrypted_output_triple_des_file.txt"
            else:
                file_name = "decrypted_output_triple_des_file.txt"

        with open(file_name, "w") as file:
            file.write(result + "\n")
            file.write(f"mode: {mode}\n")
            file.write(f"plain_text: {plain_text}\n")
            if des_3des_var.get() == 0:
                file.write(f"key: {keys[0]}\n")
            else:
                file.write(f"key1: {key1}\n")
                file.write(f"key2: {key2}\n")
                file.write(f"key3: {key3}\n")
                if init_vector:
                    file.write(f"init_vector: {init_vector}\n")

        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"{('加密' if mode == 0 else '解密')}结果已保存到 {file_name} 文件中。\n结果：{result}")

    except Exception as e:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"发生错误：{e}")

def open_file_dialog(entry_widget):
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, "r") as file:
            content = file.readline().strip()
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, content)

root = tk.Tk()
root.title("加密解密工具")

# DES 和 3DES 切换选项
des_3des_var = tk.IntVar()
des_radio = tk.Radiobutton(root, text="DES", variable=des_3des_var, value=0)
des_radio.grid(row=0, column=0, padx=10, pady=10)
triple_des_radio = tk.Radiobutton(root, text="3DES", variable=des_3des_var, value=1)
triple_des_radio.grid(row=0, column=1, padx=10, pady=10)

# 明文输入框和按钮
plain_text_label = tk.Label(root, text="明文：")
plain_text_label.grid(row=1, column=0, padx=10, pady=10)
plain_text_entry = tk.Entry(root, width=50)
plain_text_entry.grid(row=1, column=1, padx=10, pady=10)
plain_text_button = tk.Button(root, text="选择文件", command=lambda: open_file_dialog(plain_text_entry))
plain_text_button.grid(row=1, column=2, padx=10, pady=10)

# 模式选择
mode_var = tk.IntVar()
encrypt_radio = tk.Radiobutton(root, text="加密", variable=mode_var, value=0)
encrypt_radio.grid(row=2, column=0, padx=10, pady=10)
decrypt_radio = tk.Radiobutton(root, text="解密", variable=mode_var, value=1)
decrypt_radio.grid(row=2, column=1, padx=10, pady=10)

# 根据选择显示不同的密钥输入框
def update_key_entries():
    if des_3des_var.get() == 0:
        key_label.grid(row=3, column=0, padx=10, pady=10)
        key_entry.grid(row=3, column=1, padx=10, pady=10)
        key1_label.grid_forget()
        key1_entry.grid_forget()
        key2_label.grid_forget()
        key2_entry.grid_forget()
        key3_label.grid_forget()
        key3_entry.grid_forget()
        iv_label.grid_forget()
        iv_entry.grid_forget()
    else:
        key1_label.grid(row=3, column=0, padx=10, pady=10)
        key1_entry.grid(row=3, column=1, padx=10, pady=10)
        key2_label.grid(row=4, column=0, padx=10, pady=10)
        key2_entry.grid(row=4, column=1, padx=10, pady=10)
        key3_label.grid(row=5, column=0, padx=10, pady=10)
        key3_entry.grid(row=5, column=1, padx=10, pady=10)
        key_label.grid_forget()
        key_entry.grid_forget()
        iv_label.grid(row=6, column=0, padx=10, pady=10)
        iv_entry.grid(row=6, column=1, padx=10, pady=10)

key_label = tk.Label(root, text="密钥：")
key_entry = tk.Entry(root, width=50)
key1_label = tk.Label(root, text="密钥 1：")
key1_entry = tk.Entry(root, width=50)
key2_label = tk.Label(root, text="密钥 2：")
key2_entry = tk.Entry(root, width=50)
key3_label = tk.Label(root, text="密钥 3：")
key3_entry = tk.Entry(root, width=50)
iv_label = tk.Label(root, text="初始化向量（IV）：")
iv_entry = tk.Entry(root, width=50)
update_key_entries()

# 加密解密按钮
encrypt_decrypt_button = tk.Button(root, text="加密/解密", command=encrypt_decrypt)
encrypt_decrypt_button.grid(row=7 if des_3des_var.get() == 0 else 8, column=0, columnspan=3, padx=10, pady=10)

# 结果显示文本框
result_text = tk.Text(root, height=5, width=60)
result_text.grid(row=8 if des_3des_var.get() == 0 else 9, column=0, columnspan=3, padx=10, pady=10)

des_3des_var.trace_add("write", lambda *args: update_key_entries())

root.mainloop()
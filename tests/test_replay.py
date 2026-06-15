import socket
import json
import zlib
import time
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Sig_PKCS1_v1_5
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes

def run_replay_attack():
    print("\n--- HACKER GIA LAP: TAN CONG GUI LAI GOI TIN CU (REPLAY ATTACK) ---")
    
    with open("sample_data/financial_small.txt", "rb") as f:
        original_data = f.read()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 65432))

    try:
        # BƯỚC 1: HANDSHAKE
        SENDER_KEY = RSA.generate(1024)
        handshake_packet = {"msg": "Hello!", "pub_key": SENDER_KEY.publickey().export_key().decode('utf-8')}
        client_socket.sendall(json.dumps(handshake_packet).encode('utf-8') + b'\n')
        resp1 = json.loads(client_socket.recv(4096).decode('utf-8'))
        receiver_pub_key = RSA.import_key(resp1["pub_key"])

        # BƯỚC 2: TRAO ĐỔI KHÓA (TẠO TIMESTAMP QUÁ HẠN)
        session_key = get_random_bytes(16)
        
        # ---- HÀNH VI CỦA HACKER: Tạo mốc thời gian cũ trong quá khứ ----
        # Giả lập gói tin này đã bị bắt giữ và đóng gói từ 5 phút trước (300 giây trước)
        old_timestamp = str(time.time() - 300) 
        metadata_str = f"financial_small.txt|{old_timestamp}|financial_doc"
        print(f"[-] Hacker sao chep goi tin co chua Timestamp cu: {old_timestamp}")

        hash_meta = SHA512.new(metadata_str.encode('utf-8'))
        signature = base64.b64encode(Sig_PKCS1_v1_5.new(SENDER_KEY).sign(hash_meta)).decode('utf-8')
        cipher_rsa = PKCS1_v1_5.new(receiver_pub_key)
        encrypted_key = base64.b64encode(cipher_rsa.encrypt(session_key)).decode('utf-8')
        
        # Gửi gói tin chứa mốc thời gian cũ qua mạng
        key_packet = {"enc_key": encrypted_key, "meta": metadata_str, "sig": signature}
        client_socket.sendall(json.dumps(key_packet).encode('utf-8') + b'\n')

        # Đọc phản hồi ngay lập tức từ Bước 2
        result = client_socket.recv(1024).decode('utf-8').strip()
        print(f"[>] Ket qua phan hoi tu May Nhan: {result}")

    except Exception as e:
        print(f"[-] Loi: {str(e)}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    run_replay_attack()
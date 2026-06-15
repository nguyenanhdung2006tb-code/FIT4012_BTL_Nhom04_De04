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

def run_tampering_attack():
    print("\n--- HACKER GIA LAP: TAN CONG SUA DOI DU LIEU (TAMPERING) ---")
    
    # 1. Đọc dữ liệu thô để chuẩn bị gửi
    with open("sample_data/financial_small.txt", "rb") as f:
        original_data = f.read()

    # 2. Kết nối tới Máy Nhận
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 65432))

    try:
        # BƯỚC 1: HANDSHAKE (Làm như bình thường để lọt qua vòng gửi xe)
        SENDER_KEY = RSA.generate(1024)
        handshake_packet = {"msg": "Hello!", "pub_key": SENDER_KEY.publickey().export_key().decode('utf-8')}
        client_socket.sendall(json.dumps(handshake_packet).encode('utf-8') + b'\n')
        resp1 = json.loads(client_socket.recv(4096).decode('utf-8'))
        receiver_pub_key = RSA.import_key(resp1["pub_key"])

        # BƯỚC 2: TRAO ĐỔI KHÓA (Vẫn làm đúng quy trình)
        session_key = get_random_bytes(16)
        timestamp = str(time.time())
        metadata_str = f"financial_small.txt|{timestamp}|financial_doc"
        hash_meta = SHA512.new(metadata_str.encode('utf-8'))
        signature = base64.b64encode(Sig_PKCS1_v1_5.new(SENDER_KEY).sign(hash_meta)).decode('utf-8')
        cipher_rsa = PKCS1_v1_5.new(receiver_pub_key)
        encrypted_key = base64.b64encode(cipher_rsa.encrypt(session_key)).decode('utf-8')
        
        key_packet = {"enc_key": encrypted_key, "meta": metadata_str, "sig": signature}
        client_socket.sendall(json.dumps(key_packet).encode('utf-8') + b'\n')

        # BƯỚC 3: MÃ HÓA VÀ THỰC HIỆN HÀNH VI PHÁ HOẠI (TAMPERING)
        compressed_data = zlib.compress(original_data)
        cipher_aes = AES.new(session_key, AES.MODE_GCM)
        ciphertext, tag = cipher_aes.encrypt_and_digest(compressed_data)

        # ---- HÀNH VI CỦA HACKER: Sửa đổi bản mã ----
        # Hacker đổi byte đầu tiên của bản mã để phá hoại số liệu báo cáo
        tampered_ciphertext = bytearray(ciphertext)
        tampered_ciphertext[0] = tampered_ciphertext[0] ^ 0xFF  # Đảo bit phá hoại
        ciphertext = bytes(tampered_ciphertext)
        print("[-] Hacker da can thiep va sua doi 1 byte trong chuoi Ciphertext!")

        # Đóng gói đồ giả gửi đi
        nonce_b64 = base64.b64encode(cipher_aes.nonce).decode('utf-8')
        cipher_b64 = base64.b64encode(ciphertext).decode('utf-8')
        tag_b64 = base64.b64encode(tag).decode('utf-8')
        
        # Tính lại mã băm đường truyền nhưng Tag mã hóa AES bên trong đã bị hỏng toán học
        hash_hex = SHA512.new(cipher_aes.nonce + ciphertext + tag).hexdigest()

        spec_metadata = {"orig_size": len(original_data), "comp_size": len(compressed_data), "comp_algo": "zlib", "comp_time_ms": 0.1, "enc_time_ms": 0.2}
        data_packet = {"nonce": nonce_b64, "cipher": cipher_b64, "tag": tag_b64, "hash": hash_hex, "sig": signature, "spec_meta": spec_metadata}
        
        client_socket.sendall(json.dumps(data_packet).encode('utf-8') + b'\n')

        # BƯỚC 4: XEM MÁY NHẬN TRẢ VỀ PHẢN HỒI GÌ
        result = client_socket.recv(1024).decode('utf-8').strip()
        print(f"[>] Ket qua phan hoi tu May Nhan: {result}")

    except Exception as e:
        print(f"[-] Loi: {str(e)}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    run_tampering_attack()
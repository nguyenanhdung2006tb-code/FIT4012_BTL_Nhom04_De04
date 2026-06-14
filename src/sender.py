import socket
import json
import zlib
import time
import os
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Sig_PKCS1_v1_5
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes

# Tự động khởi tạo cặp khóa RSA 1024-bit phía máy gửi phục vụ việc ký số định danh
SENDER_KEY = RSA.generate(1024)
SENDER_PUB_EXPORT = SENDER_KEY.publickey().export_key().decode('utf-8')

def start_sender(file_path):
    if not os.path.exists(file_path):
        print(f"[-] Không tìm thấy file nguồn: {file_path}"); return

    print(f"\n--- TIẾN TRÌNH TRUYỀN TẢI NÂNG CẤP HỆ THỐNG NĂM 2026: {file_path} ---")
    
    with open(file_path, "rb") as f:
        original_data = f.read()
    orig_size = len(original_data)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 65432))

    try:
        # BƯỚC 1: HANDSHAKE
        handshake_packet = {"msg": "Hello!", "pub_key": SENDER_PUB_EXPORT}
        client_socket.sendall(json.dumps(handshake_packet).encode('utf-8') + b'\n')
        
        resp1 = json.loads(client_socket.recv(4096).decode('utf-8'))
        if resp1.get("msg") == "Ready!":
            print("[+] Bước 1: Handshake thành công. Đã nhận khóa công khai RSA của máy nhận.")
            receiver_pub_key = RSA.import_key(resp1["pub_key"])
        else:
            print("[-] Thất bại tại bước bắt tay mạng."); return

        # BƯỚC 2: XÁC THỰC VÀ TRAO KHÓA PHIÊN RSA
        session_key = get_random_bytes(16) # Sinh khóa AES-128 ngẫu nhiên bảo mật
        
        # Nhúng cấu trúc Timestamp thời gian thực để máy nhận kiểm tra chống Replay Attack
        timestamp = str(time.time())
        metadata_str = f"{os.path.basename(file_path)}|{timestamp}|financial_doc"
        
        # Tạo chữ ký số RSA-SHA512 trên chuỗi Metadata vừa tạo
        hash_meta = SHA512.new(metadata_str.encode('utf-8'))
        signer = Sig_PKCS1_v1_5.new(SENDER_KEY)
        signature = base64.b64encode(signer.sign(hash_meta)).decode('utf-8')

        # Mã hóa khóa phiên đối xứng bằng khóa công khai RSA của máy nhận
        cipher_rsa = PKCS1_v1_5.new(receiver_pub_key)
        encrypted_key = base64.b64encode(cipher_rsa.encrypt(session_key)).decode('utf-8')

        # Gửi gói tin bảo mật bước 2 qua kênh truyền mạng công cộng
        key_packet = {"enc_key": encrypted_key, "meta": metadata_str, "sig": signature}
        client_socket.sendall(json.dumps(key_packet).encode('utf-8') + b'\n')
        print("[+] Bước 2: Đã gửi chữ ký số định danh hệ thống và khóa phiên mã hóa.")

        # BƯỚC 3: MÃ HÓA & TRUYỀN DỮ LIỆU ĐÃ TỐI ƯU NÉN
        # Kế thừa chức năng nền: Nén dữ liệu thô bằng zlib trước khi đưa vào vùng mã hóa
        compressed_data = zlib.compress(original_data)
        
        # Nâng cấp bảo mật: Mã hóa AES-GCM tự sinh nonce ngẫu nhiên
        cipher_aes = AES.new(session_key, AES.MODE_GCM)
        ciphertext, tag = cipher_aes.encrypt_and_digest(compressed_data)

        # Đóng gói an toàn Base64 bảo vệ tính toàn vẹn của cấu trúc JSON Payload
        nonce_b64 = base64.b64encode(cipher_aes.nonce).decode('utf-8')
        cipher_b64 = base64.b64encode(ciphertext).decode('utf-8')
        tag_b64 = base64.b64encode(tag).decode('utf-8')

        # Tính toán mã kiểm tra tính toàn vẹn đường truyền SHA-512 tổng thể
        raw_payload = cipher_aes.nonce + ciphertext + tag
        hash_hex = SHA512.new(raw_payload).hexdigest()

        # Đóng gói tệp tin gửi đi đúng định dạng mô tả trang 9 đề bài
        data_packet = {
            "nonce": nonce_b64,
            "cipher": cipher_b64,
            "tag": tag_b64,
            "hash": hash_hex,
            "sig": signature
        }
        client_socket.sendall(json.dumps(data_packet).encode('utf-8') + b'\n')
        print("[+] Bước 3: Đã gửi gói dữ liệu tài chính tối ưu mã hóa Base64 thành công.")

        # Bước 4: Nhận tín hiệu kết thúc giao thức
        result = client_socket.recv(1024).decode('utf-8').strip()
        if result == "ACK":
            print("[+] Bước 4: Máy nhận phản hồi ACK - Hệ thống hoàn thành truyền nhận an toàn đạt chuẩn 2026!")
        else:
            print(f"[-] Thất bại: Máy nhận từ chối xử lý gói tin (Mã lỗi: {result})")

    except Exception as e:
        print(f"[-] Lỗi kết nối truyền thông: {str(e)}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_sender("sample_data/financial_large.txt")
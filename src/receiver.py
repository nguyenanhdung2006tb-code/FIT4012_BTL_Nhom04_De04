import socket
import json
import zlib
import time
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Sig_PKCS1_v1_5
from Crypto.Hash import SHA512

def write_log(message):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_line = f"[{current_time}] {message}\n"
    print(log_line.strip())
    with open("security_audit.log", "a", encoding="utf-8") as log_file:
        log_file.write(log_line)

# Tự động khởi tạo cặp khóa RSA 1024-bit phục vụ giao thức mật mã lai
RECEIVER_KEY = RSA.generate(1024)
RECEIVER_PUB_EXPORT = RECEIVER_KEY.publickey().export_key().decode('utf-8')

class SocketReader:
    def __init__(self, sock):
        self.sock = sock
        self.buffer = b""
    def read_line(self):
        while b'\n' not in self.buffer:
            chunk = self.sock.recv(1024 * 1024)
            if not chunk:
                return self.buffer if self.buffer else b""
            self.buffer += chunk
        line, self.buffer = self.buffer.split(b'\n', 1)
        return line

def start_receiver():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 65432))
    server_socket.listen(1)
    write_log("MÁY NHẬN: Hệ thống khởi động nâng cấp thành công, đang đợi kết nối...")

    conn, addr = server_socket.accept()
    reader = SocketReader(conn)
    write_log(f"KẾT NỐI: Thực thể mạng kết nối tại địa chỉ: {addr}")

    session_key = None
    sender_pub_key = None

    try:
        # BƯỚC 1: HANDSHAKE
        msg1 = json.loads(reader.read_line().decode('utf-8'))
        if msg1.get("msg") == "Hello!":
            write_log("HANDSHAKE: Nhận tín hiệu 'Hello!'.")
            sender_pub_key = RSA.import_key(msg1["pub_key"])
            handshake_resp = {"msg": "Ready!", "pub_key": RECEIVER_PUB_EXPORT}
            conn.sendall(json.dumps(handshake_resp).encode('utf-8') + b'\n')
            write_log("HANDSHAKE: Đã phản hồi 'Ready!' kèm RSA Public Key.")
        else:
            write_log("LỖI BẢO MẬT: Tín hiệu bắt tay không hợp lệ."); conn.sendall(b"NACK\n"); return

        # BƯỚC 2: XÁC THỰC DANH TÍNH & GIẢI MÃ TRAO KHÓA RSA
        msg2 = json.loads(reader.read_line().decode('utf-8'))
        metadata_str = msg2["meta"]
        metadata_bytes = metadata_str.encode('utf-8')
        
        # Xác minh tính chân thực của chữ ký số phía người gửi
        hash_obj = SHA512.new(metadata_bytes)
        verifier = Sig_PKCS1_v1_5.new(sender_pub_key)
        
        if not verifier.verify(hash_obj, base64.b64decode(msg2["sig"])):
            write_log("CẢNH BÁO NGUY HIỂM: Chữ ký số không hợp lệ! Thực thể giả mạo."); conn.sendall(b"NACK\n"); return
        write_log("XÁC THỰC: Xác minh chữ ký số RSA-SHA512 thành công.")

        # Kiểm tra chống tấn công Replay Attack
        meta_parts = metadata_str.split('|')
        sent_time = float(meta_parts[1])
        current_time = time.time()
        
        if current_time - sent_time > 60:
            write_log("CẢNH BÁO AN NINH: Phát hiện gói tin nghi vấn REPLAY ATTACK! Từ chối xử lý.")
            conn.sendall(b"NACK_REPLAY\n"); return
        write_log("XÁC THỰC: Kiểm tra mốc thời gian hợp lệ (Chống Replay đạt chuẩn).")

        # Giải mã lấy khóa phiên AES
        cipher_rsa = PKCS1_v1_5.new(RECEIVER_KEY)
        session_key = cipher_rsa.decrypt(base64.b64decode(msg2["enc_key"]), None)
        write_log("MẬT MÃ: Khóa phiên Session Key đã được giải mã an toàn.")

        # BƯỚC 3: GIẢI MÃ DỮ LIỆU CÓ XÁC THỰC TOÀN VẸN
        msg3 = json.loads(reader.read_line().decode('utf-8'))
        nonce = base64.b64decode(msg3["nonce"])
        ciphertext = base64.b64decode(msg3["cipher"])
        tag = base64.b64decode(msg3["tag"])

        # Kiểm định mã băm SHA-512 đường truyền
        raw_payload = nonce + ciphertext + tag
        if SHA512.new(raw_payload).hexdigest() != msg3["hash"]:
            write_log("CẢNH BÁO TOÀN VẸN: Mã băm SHA-512 không khớp! Dữ liệu đường truyền bị can thiệp.")
            conn.sendall(b"NACK_INTEGRITY\n"); return

        # Tiến hành giải mã AES-GCM và giải nén dữ liệu thô
        try:
            cipher_aes = AES.new(session_key, AES.MODE_GCM, nonce=nonce)
            compressed_data = cipher_aes.decrypt_and_verify(ciphertext, tag)
            original_data = zlib.decompress(compressed_data)
        except ValueError:
            write_log("CẢNH BÁO BẢO MẬT: Thẻ xác thực Tag của hệ AES-GCM bị lỗi! Ciphertext đã bị sửa đổi.")
            conn.sendall(b"NACK_TAG\n"); return

        # Ghi lưu file thành phẩm xuống ổ đĩa
        with open("received_finance.txt", "wb") as f:
            f.write(original_data)
            
        # [NÂNGCẤP 2026]: Đọc gói đặc tả hiệu năng để ghi vết chi tiết vào Log hệ thống
        spec_meta = msg3.get("spec_meta", {})
        write_log(f"--- THÔNG SỐ KIỂM TOAN HIỆU NĂNG NHÓM 4 ---")
        write_log(f"File nhận thực tế: {meta_parts[0]}")
        write_log(f"Kích thước gốc: {spec_meta.get('orig_size')} bytes")
        write_log(f"Kích thước sau nén: {spec_meta.get('comp_size')} bytes")
        write_log(f"Thuật toán nén sử dụng: {spec_meta.get('comp_algo')}")
        write_log(f"Thời gian nén hệ thống: {spec_meta.get('comp_time_ms')} ms")
        write_log(f"Thời gian mã hóa hệ thống: {spec_meta.get('enc_time_ms')} ms")
        write_log(f"THÀNH CÔNG: Đã khôi phục tệp tin và hoàn tất kiểm toán an ninh.")
        conn.sendall(b"ACK\n")

    except Exception as e:
        write_log(f"LỖI HỆ THỐNG: {str(e)}")
        conn.sendall(b"NACK\n")
    finally:
        conn.close()
        server_socket.close()

if __name__ == "__main__":
    start_receiver()
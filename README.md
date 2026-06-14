# FIT4012 - He Thong Truyen Bao Cao Tai Chinh An Toan (Nang Cap 2026)

## Thong Tin Nhom Thuc Hien - Nhom 04
* Truong nhom: Nguyen Anh Dung - MSSV: 1871020167 - Lop: CNTT-1802
* Thanh vien: Nguyen Huu Manh - MSSV: 1871020381 - Lop: CNTT-1802
* Thanh vien: Ngo Gia Bao - MSSV: 1871020072 - Lop: CNTT-1802
* Thanh vien: Trần Đình Đức Toàn - MSSV: 1871020574 - Lop: CNTT-1802
**Hoc phan:** Nhap mon An toan va Bao mat thong tin
**De tai 4:** Secure Compressed Financial Report
**Don vi:** Dai hoc Dai Nam

---

## Cau Truc Thu Muc Du An
* src/: Chua ma nguon thuc thi he thong (sender.py, receiver.py).
* sample_data/: Chua cac tep du lieu kiem thu he thong voi 3 kich thuoc khac nhau.
* security_audit.log: Nhat ky ghi vet kiem toan an ninh bao mat thoi gian thuc.
* benchmark.md: Bao cao chi tiet hieu nang nen va mat ma lai cua he thong.

## Huong Dan Cai Dat Va Khoi Chay

### 1. Cai dat thu vien mat ma hoc
He thong su dung thu vien chuan pycryptodome de xu ly cac thuat toan mat ma. Cai dat bang lenh:
pip install pycryptodome

### 2. Cac buoc chay he thong
* Buoc 1 (Phia nhan): Mo mot Terminal va khoi chay may nhan truoc de dung doi ket noi:
python src/receiver.py

* Buoc 2 (Phia gui): Mo mot Terminal doc lap khac va khoi chay may gui de tien hanh truyen file:
python src/sender.py
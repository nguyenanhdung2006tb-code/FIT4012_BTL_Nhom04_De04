# BAO CAO BENCHMARK HIEU NANG HE THONG - NHOM 4

Mo ta: He thong thuc hien do dac thuc te tren moi truong Localhost voi 3 tep du lieu tai chinh co kich thuoc khac nhau de danh gia ty le nen cua thuat toan zlib va toc do xu ly cua he mat ma lai nang cap RSA 1024-bit (PKCS#1 v1.5) + AES-GCM 128-bit.

## Bang tong hop so lieu do dac thuc te (He mat ma lai nang cap)

| Ten Tep Thu Nghiem | Kich Thuoc Goc | Kich Thuoc Sau Nen | Ty Le Nen Dat | Thoi Gian Nen | Thoi Gian Ma Hoa (RSA + AES) | Thoi Gian Giai Ma + Xac Thuc |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| financial_small.txt | 41,500 bytes | 239 bytes | 99.42% | 0.16 ms | 14.20 ms | 15.35 ms |
| financial_medium.txt | 415,000 bytes | 1,505 bytes | 99.64% | 1.73 ms | 15.85 ms | 16.42 ms |
| financial_large.txt | 2,075,000 bytes | 7,135 bytes | 99.66% | 8.20 ms | 22.40 ms | 24.18 ms |

## Nhan xet ket qua cau hinh nang cap 2026
1. Toi uu dung luong: Thuat toan nen zlib duy tri ty le nen cuc cao (tren 99%), giup giam thieu toi da tai bang thong khi truyen tyeu tin tai chinh lon qua Socket TCP.
2. Anh huong cua RSA: Thoi gian ma hoa va giai ma co tang nhe so voi phien ban cu do he thong phai thuc hien ky so va xac thuc RSA-SHA512 de chong gia mao va kiem tra Timestamp chong Replay Attack. Tuy nhien, tong thoi gian xu ly van o muc cuc ky an toan va muot ma (duoi 25 ms cho file 2 MB), hoan toan dap ung tieu chuan bao mat thoi gian thuc.
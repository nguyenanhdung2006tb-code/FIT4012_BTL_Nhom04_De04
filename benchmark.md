# BAO CAO BENCHMARK HIEU NANG HE THONG - NHOM 4

Mo ta: He thong thuc hien do dac thuc te tren moi truong Localhost de danh gia ty le nen cua thuat toan zlib va toc do xu ly cua he mat ma lai nang cap RSA 1024-bit + AES-GCM 128-bit.

## Bang tong hop so lieu do dac thuc te (Ghi nhan truc tiep tu he thong)

| Ten Tep Thu Nghi Nghi | Kich Thuoc Goc | Kich Thuoc Sau Nen | Ty Le Nen Dat | Thoi Gian Nen | Thoi Gian Ma Hoa (RSA + AES) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| financial_small.txt | 41,500 bytes | 239 bytes | 99.42% | 1.2451 ms | 7.2549 ms |
| financial_medium.txt | 415,000 bytes | 1,505 bytes | 99.64% | 1.7953 ms | 5.2567 ms |
| financial_large.txt | 2,075,000 bytes | 7,135 bytes | 99.66% | 9.7208 ms | 4.7983 ms |

## Nhan xet ket qua cau hinh nang cap 2026
1. Toi uu dung luong: Thuat toan nen zlib hoat dong cuc ky hieu qua tren cac tep tin van ban bao cao tai chinh cua cong ty, giup tiet kiem trung binh hon 99% bang thong duong truyen truoc khi day qua Socket TCP.
2. Hieu nang mat ma: Thoi gian ma hoa va xu ly goi tin luon duy tri o muc sieu nhanh (duoi 10 ms cho tat ca cac phan vung kich thuoc file), bao dam tinh an toan tuyet doi nhung khong he gay tre he thong.
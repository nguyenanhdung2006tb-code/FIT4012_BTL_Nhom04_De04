# THREAT MODEL - MO HINH MOI NGUY HAI HE THONG

## 1. Tai san can bao ve
* Cac tep tin bao cao tai chinh doanh nghiep (financial_small.txt, financial_medium.txt, financial_large.txt).
* Khoa phien bi mat (Session Key) dung de ma hoa du lieu.

## 2. Tac nhan tan cong gia dinh
* Ke tan cong dung giua duong truyen mang (Man-in-the-middle) de nghe len hoac danh cap thong tin.
* Thuc the gia mao thong tin gui du lieu doc hai den may nhan.
* Ke tan cong thu thap goi tin cu va gui lai nhieu lan (Replay Attack) de lam te liet he thong.

## 3. Giai phap phong thu cua Nhom 4
* Tinh bi mat: Ma hoa toan bo du lieu bang thuat toan AES-GCM 128-bit.
* Tinh toan ven: Su dung ma bam SHA-512 va the xac thuc Tag cua AES-GCM.
* Chong Replay: Nhuyen cau truc Timestamp vao chu ky so, gioi han thoi gian hop le trong 60 giay.
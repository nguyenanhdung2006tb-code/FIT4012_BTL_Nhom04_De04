# TEST REPORT - KET QUA KIEM THU BAO MAT NHOM 4

## Kich ban 1: Chay voi du lieu hop le (Valid Flow)
* Dau vao: File tai chinh dung quy chuan, goi tin truyen tai thoi gian thuc.
* Ket qua: May nhan xac minh chu ky so thanh cong, giai ma muer ma va tra ve ACK.
* Trang thai: PASS.

## Kich ban 2: Phat hien goi tin bi sua doi (Tampering Attack)
* Dau vao: Gia lap sua doi 1 byte trong chuoi Ciphertext hoac the Tag tren duong truyen.
* Ket qua: May nhan kiem tra ma bam SHA-512 hoac Tag AES-GCM thay sai lech, lap tuc ngat ket noi va tra ve NACK_INTEGRITY / NACK_TAG.
* Trang thai: PASS.

## Kich ban 3: Phat hien tan cong gui lai du lieu cu (Replay Attack)
* Dau vao: Gui lai mot goi tin ma hoa da danh cap tu truoc do (Thoi gian lech qua 60 giay).
* Ket qua: May nhan trich xuat Timestamp, phat hien goi tin da het han va tu choi xu ly (NACK_REPLAY).
* Trang thai: PASS.
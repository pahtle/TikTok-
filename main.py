import os
import time
import threading
import random
from datetime import datetime

try:
    from colorama import Style, Fore
    import tls_client
    from fake_useragent import UserAgent
    from Static.Methods import StaticMethods
    from Static.Values import StaticValues
    from Handler.ErrorHandler import Handler
except:
    print("Đang cài đặt thư viện...")
    os.system("pip install -r requirements.txt")
    os.system("python3 main.py")

class ChuongTrinh:
    def _xoa_man_hinh(self):
        os.system("cls") if os.name == 'nt' else os.system("clear")

    def chinh(self):
        self._xoa_man_hinh()
        while True:
            print(f"{StaticValues.WAITING}Nhập URL hoặc @ của nạn nhân ➤ ", end="")
            self.nan_nhan = input()
            self.nan_nhan = StaticMethods.get_userData(self.nan_nhan, "id")
            if "Invalid" in self.nan_nhan:
                print(f"{StaticValues.WARNING} URL hoặc @ không hợp lệ!")
            else:
                break
        self._xoa_man_hinh()
        print(f"{StaticValues.SUCCESS}Người dùng hợp lệ!")
        print(f"{StaticValues.WAITING}Đang thu thập thông tin người dùng...")
        self.du_lieu_nan_nhan = {
            "id": StaticMethods.get_userData(self.nan_nhan, "id"),
            "nickname": StaticMethods.get_userData(self.nan_nhan, "nickname"),
            "secUid": StaticMethods.get_userData(self.nan_nhan, "secUid"),
        }
        print(f"{StaticValues.SUCCESS}Thành công!")
        self._xoa_man_hinh()
        print(f"{StaticValues.WAITING}Chọn một tùy chọn để báo cáo nạn nhân.")
        for key, value in StaticValues.REPORT_TYPES.items():
            print(f"{key}: {value[1]}")
        while True:
            self.loai_bao_cao = Handler.integer_handler(f"{Fore.YELLOW}➤ {Fore.RESET}", 1, 15)
            if self.loai_bao_cao in StaticValues.REPORT_TYPES:
                break
        self.payload = StaticMethods._getpayload(
            datetime.now().timestamp(),
            UserAgent().random,
            random.randint(7000000000000000000, 9999999999999999999),
            random.randint(7000000000000000000, 9999999999999999999),
            self.du_lieu_nan_nhan,
            self.loai_bao_cao,
        )

    def bao_cao(self):
        while True:
            session = tls_client.Session(client_identifier="chrome_106")
            response = session.get(
                "https://www.tiktok.com/aweme/v2/aweme/feedback/", params=self.payload
            )

            StaticValues.TONG_SO_YEU_CAU += 1
            if "Thanks for your feedback" in response.text or response.status_code == 200:
                StaticValues.SO_LUONG_BAO_CAO += 1
                self._xoa_man_hinh()
                print(
                    f"{StaticValues.SUCCESS}{self.du_lieu_nan_nhan['nickname']} đã được báo cáo {StaticValues.SO_LUONG_BAO_CAO} lần! (Tỷ lệ thành công {(StaticValues.SO_LUONG_BAO_CAO/StaticValues.TONG_SO_YEU_CAU)*100:.2f}%)"
                )
            else:
                print(
                    f"{StaticValues.WARNING}Lỗi (Tỷ lệ thành công {(StaticValues.SO_LUONG_BAO_CAO/StaticValues.TONG_SO_YEU_CAU)*100:.2f}%)"
                )
                StaticValues.COOLDOWN = True
                break

if __name__ == "__main__":
    cac_luong = []
    StaticMethods.check_version("0.0.3")
    os.system("cls") if os.name == 'nt' else os.system("clear")
    StaticMethods.vk()
    os.system("cls") if os.name == 'nt' else os.system("clear")
    StaticMethods.is_first_run()
    StaticMethods.show_credits()
    so_luong_luong = Handler.integer_handler(f"{StaticValues.WAITING}SỐ LƯỢNG LUỒNG ➤ ")
    time.sleep(1)
    chuong_trinh = ChuongTrinh()
    chuong_trinh.chinh()
    for _ in range(so_luong_luong):
        luong = threading.Thread(target=chuong_trinh.bao_cao)
        cac_luong.append(luong)
        luong.start()
    for luong in cac_luong:
        if not StaticValues.COOLDOWN:
            luong.join()
        else:
            print(f"{StaticValues.WAITING}Phát hiện cooldown. Chờ 10 giây...")
            time.sleep(10)
            StaticValues.COOLDOWN = False

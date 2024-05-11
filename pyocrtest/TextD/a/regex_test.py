import re
#^([01]?[0-9]|2[0-3])([:.])([0-5][0-9])$ time
#^(0[1-9]|[12][0-9]|3[01])([./])(0[1-9]|1[0-2])\2(\d{4})$ date
#^([^\*]+)\*\s*(\d+)\s*,\s*(\d+\.\d{2})$ product name, quantity, price (test regex)


def get_valid_date():

    date_pattern = r"^(0[1-9]|[12][0-9]|3[01])([./])(0[1-9]|1[0-2])\2(\d{4})$"
    
    while True:

        user_date = input("Lütfen tarihi 'gg.aa.yyyy' veya 'gg/aa/yyyy' formatında giriniz: ")
        

        if re.match(date_pattern, user_date):
            print("Teşekkürler, girdiğiniz tarih doğru formatı kullanıyor:", user_date)
            break
        else:
            print("Hatalı format. Lütfen tarihi 'gg.aa.yyyy' veya 'gg/aa/yyyy' formatında giriniz.")


def get_valid_time():
    time_pattern = r"^([01]?[0-9]|2[0-3])([:.])([0-5][0-9])$"
    
    while True:
        user_time = input("Lütfen saati 'ss:dd' veya 'ss.dd' formatında giriniz (örn: 23:59 veya 23.59): ")

        if re.match(time_pattern, user_time):
            print("Teşekkürler, girdiğiniz saat doğru formatı kullanıyor:", user_time)
            break
        else:
            print("Hatalı format. Lütfen saati 'ss:dd' veya 'ss.dd' formatında doğru bir şekilde giriniz.")


# get_valid_time()
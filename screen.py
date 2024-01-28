import tkinter as tk
import re
import FIR
import IIR

# pre setting
mode = ["FIR", "IIR"]
mode_FIR = ["thông cao", "thông thấp", "thông dải", "chắn dải"]
window_mode = ["Chữ nhật", "Barlett", "Hanning", "Hamming", "Black Man"]
window_IIRmode = ["Butterworth", "Chebyshev 1", "Chebyshev 2", "Elliptic"]


# thông thấp screen
def IIR_Thong_thap_click():
    filter = ""

    def on_radio_button_clicked(value):
        print("value")
        global filter
        filter = value
        print(filter)

    def on_button_click():
        global filter
        print("clik")
        # clear previous error
        clear_label = tk.Label(
            Thong_thap_screen,
            text="                                                  ",
            font=("Arial", 24),
        )
        clear_label.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
        # Get values from the entry widgets
        input1_value = dao_dong_trong_giai_thong.get()
        input2_value = suy_giam_trong_giai_chan.get()
        input3_value = tan_so_chan_duoi.get()
        input4_value = tan_so_chan_tren.get()
        if filter == "":
            return
        try:
            Rp = float(input1_value)
        except Exception as ve:
            error_label = tk.Label(
                Thong_thap_screen,
                text="Lỗi giá trị Rp",
                font=("Arial", 24),
            )
            error_label.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
            return
        try:
            As = float(input2_value)
        except Exception as ve:
            error_label = tk.Label(
                Thong_thap_screen,
                text="Lỗi giá trị As",
                font=("Arial", 24),
            )
            error_label.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
            return
        try:
            filter_input = re.findall(r"^[0123456789]*.[0123456789]*\*pi", input3_value)
            if len(filter_input[0]) != len(input3_value):
                raise ValueError()
            chan_duoi = float(input3_value.split("*")[0])
        except Exception as ve:
            print(ve)
            error_label = tk.Label(
                Thong_thap_screen,
                text="Lỗi giá trị tần số góc chắn dưới",
                font=("Arial", 24),
            )
            error_label.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
            return
        try:
            filter_input = re.findall(r"^[0123456789]*.[0123456789]*\*pi", input4_value)
            if len(filter_input[0]) != len(input4_value):
                raise ValueError()
            chan_tren = float(input4_value.split("*")[0])
            print(chan_tren)
        except Exception as ve:
            print(ve)
            error_label = tk.Label(
                Thong_thap_screen,
                text="Lỗi giá trị tần số góc chắn trên",
                font=("Arial", 24),
            )
            error_label.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
            return
        IIR.lowpassDraw(chan_duoi, chan_tren, Rp, As, filter)

    Thong_thap_screen = tk.Toplevel(app)
    Thong_thap_screen.title("Input Screen")
    Thong_thap_screen.geometry("900x600")
    Thong_thap_screen.title("Bộ lọc IIR với thông thấp")
    # Create input fields
    dao_dong_trong_giai_thong_label = tk.Label(Thong_thap_screen, text="Rp:")
    dao_dong_trong_giai_thong_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    dao_dong_trong_giai_thong = tk.Entry(Thong_thap_screen)
    dao_dong_trong_giai_thong.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_dao_dong_trong_giai_thong = tk.Label(Thong_thap_screen, text="dB")
    chuthich_dao_dong_trong_giai_thong.grid(
        row=0, column=2, padx=5, pady=5, sticky=tk.W
    )
    # input As
    suy_giam_trong_giai_chan_label = tk.Label(Thong_thap_screen, text="As:")
    suy_giam_trong_giai_chan_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    suy_giam_trong_giai_chan = tk.Entry(Thong_thap_screen)
    suy_giam_trong_giai_chan.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_suy_giam_trong_giai_chan = tk.Label(Thong_thap_screen, text="dB")
    chuthich_suy_giam_trong_giai_chan.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)

    tan_so_chan_duoi_label = tk.Label(Thong_thap_screen, text="tần số góc chắn dưới:")
    tan_so_chan_duoi_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    tan_so_chan_duoi = tk.Entry(Thong_thap_screen)
    tan_so_chan_duoi.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_tan_so_chan_duoi = tk.Label(Thong_thap_screen, text="Vd: 0.5*pi")
    chuthich_tan_so_chan_duoi.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)

    tan_so_chan_tren_label = tk.Label(Thong_thap_screen, text="tần số góc chắn trên:")
    tan_so_chan_tren_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
    tan_so_chan_tren = tk.Entry(Thong_thap_screen)
    tan_so_chan_tren.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_tan_so_chan_tren = tk.Label(Thong_thap_screen, text="Vd: 0.5*pi")
    chuthich_tan_so_chan_tren.grid(row=3, column=2, padx=5, pady=5, sticky=tk.W)
    # choose filter
    selected_option = tk.StringVar()
    i = 0
    for option in window_IIRmode:
        radio_button = tk.Radiobutton(
            Thong_thap_screen,
            text=option,
            variable=selected_option,
            value=option,
            command=lambda value=option: on_radio_button_clicked(value),
        )
        radio_button.grid(row=4, column=i, padx=5, pady=5, sticky=tk.W)
        i += 1
    # Create a button
    button = tk.Button(Thong_thap_screen, text="Submit", command=on_button_click)
    button.grid(row=5, column=0, columnspan=3, padx=5, pady=5)
    new_label = tk.Label(Thong_thap_screen, text="tham số pi được ký hiệu là pi")
    new_label.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
    new_label = tk.Label(
        Thong_thap_screen, text="nếu giá trị tần số góc là 0 thì nhập vào input là 0*pi"
    )
    new_label.grid(row=7, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)


def IIR_Thong_cao_click():
    filter = ""

    def on_radio_button_clicked(value):
        print("value")
        global filter
        filter = value
        print(filter)

    def on_button_click():
        global filter
        print("clik")
        # clear previous error
        clear_label = tk.Label(
            Thong_thap_screen,
            text="                                                  ",
            font=("Arial", 24),
        )
        clear_label.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
        # Get values from the entry widgets
        input1_value = dao_dong_trong_giai_thong.get()
        input2_value = suy_giam_trong_giai_chan.get()
        input3_value = tan_so_chan_duoi.get()
        input4_value = tan_so_chan_tren.get()
        if filter == "":
            return
        try:
            Rp = float(input1_value)
        except Exception as ve:
            error_label = tk.Label(
                Thong_thap_screen,
                text="Lỗi giá trị Rp",
                font=("Arial", 24),
            )
            error_label.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
            return
        try:
            As = float(input2_value)
        except Exception as ve:
            error_label = tk.Label(
                Thong_thap_screen,
                text="Lỗi giá trị As",
                font=("Arial", 24),
            )
            error_label.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
            return
        try:
            filter_input = re.findall(r"^[0123456789]*.[0123456789]*\*pi", input3_value)
            if len(filter_input[0]) != len(input3_value):
                raise ValueError()
            chan_duoi = float(input3_value.split("*")[0])
        except Exception as ve:
            print(ve)
            error_label = tk.Label(
                Thong_thap_screen,
                text="Lỗi giá trị tần số góc chắn dưới",
                font=("Arial", 24),
            )
            error_label.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
            return
        try:
            filter_input = re.findall(r"^[0123456789]*.[0123456789]*\*pi", input4_value)
            if len(filter_input[0]) != len(input4_value):
                raise ValueError()
            chan_tren = float(input4_value.split("*")[0])
            print(chan_tren)
        except Exception as ve:
            print(ve)
            error_label = tk.Label(
                Thong_thap_screen,
                text="Lỗi giá trị tần số góc chắn trên",
                font=("Arial", 24),
            )
            error_label.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
            return
        IIR.highpassDraw(chan_duoi, chan_tren, Rp, As, filter)

    Thong_thap_screen = tk.Toplevel(app)
    Thong_thap_screen.title("Input Screen")
    Thong_thap_screen.geometry("900x600")
    Thong_thap_screen.title("Bộ lọc IIR với thông cao")
    # Create input fields
    dao_dong_trong_giai_thong_label = tk.Label(Thong_thap_screen, text="Rp:")
    dao_dong_trong_giai_thong_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    dao_dong_trong_giai_thong = tk.Entry(Thong_thap_screen)
    dao_dong_trong_giai_thong.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_dao_dong_trong_giai_thong = tk.Label(Thong_thap_screen, text="dB")
    chuthich_dao_dong_trong_giai_thong.grid(
        row=0, column=2, padx=5, pady=5, sticky=tk.W
    )
    # input As
    suy_giam_trong_giai_chan_label = tk.Label(Thong_thap_screen, text="As:")
    suy_giam_trong_giai_chan_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    suy_giam_trong_giai_chan = tk.Entry(Thong_thap_screen)
    suy_giam_trong_giai_chan.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_suy_giam_trong_giai_chan = tk.Label(Thong_thap_screen, text="dB")
    chuthich_suy_giam_trong_giai_chan.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)

    tan_so_chan_duoi_label = tk.Label(Thong_thap_screen, text="tần số góc chắn dưới:")
    tan_so_chan_duoi_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    tan_so_chan_duoi = tk.Entry(Thong_thap_screen)
    tan_so_chan_duoi.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_tan_so_chan_duoi = tk.Label(Thong_thap_screen, text="Vd: 0.5*pi")
    chuthich_tan_so_chan_duoi.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)

    tan_so_chan_tren_label = tk.Label(Thong_thap_screen, text="tần số góc chắn trên:")
    tan_so_chan_tren_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
    tan_so_chan_tren = tk.Entry(Thong_thap_screen)
    tan_so_chan_tren.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_tan_so_chan_tren = tk.Label(Thong_thap_screen, text="Vd: 0.5*pi")
    chuthich_tan_so_chan_tren.grid(row=3, column=2, padx=5, pady=5, sticky=tk.W)
    # choose filter
    selected_option = tk.StringVar()
    i = 0
    for option in window_IIRmode:
        radio_button = tk.Radiobutton(
            Thong_thap_screen,
            text=option,
            variable=selected_option,
            value=option,
            command=lambda value=option: on_radio_button_clicked(value),
        )
        radio_button.grid(row=4, column=i, padx=5, pady=5, sticky=tk.W)
        i += 1
    # Create a button
    button = tk.Button(Thong_thap_screen, text="Submit", command=on_button_click)
    button.grid(row=5, column=0, columnspan=3, padx=5, pady=5)
    new_label = tk.Label(Thong_thap_screen, text="tham số pi được ký hiệu là pi")
    new_label.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
    new_label = tk.Label(
        Thong_thap_screen, text="nếu giá trị tần số góc là 0 thì nhập vào input là 0*pi"
    )
    new_label.grid(row=7, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)


def IIR_Thong_dai_click():
    filter = ""

    def on_radio_button_clicked(value):
        print("value")
        global filter
        filter = value
        print(filter)

    def on_button_click():
        global filter
        print("clik")
        # clear previous error
        clear_label = tk.Label(
            Thong_thap_screen,
            text="                                                  ",
            font=("Arial", 24),
        )
        clear_label.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
        # Get values from the entry widgets
        input1_value = dao_dong_trong_giai_thong.get()
        input2_value = suy_giam_trong_giai_chan.get()
        input3_value = tan_so_cat_duoi.get()
        input4_value = tan_so_thong_duoi.get()
        input5_value = tan_so_cat_tren.get()
        input6_value = tan_so_thong_tren
        if filter == "":
            return
        try:
            Rp = float(input1_value)
        except Exception as ve:
            error_label = tk.Label(
                Thong_thap_screen,
                text="Lỗi giá trị Rp",
                font=("Arial", 24),
            )
            error_label.grid(
                row=10, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W
            )
            return
        try:
            As = float(input2_value)
        except Exception as ve:
            error_label = tk.Label(
                Thong_thap_screen,
                text="Lỗi giá trị As",
                font=("Arial", 24),
            )
            error_label.grid(
                row=10, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W
            )
            return
        try:
            filter_input = re.findall(r"^[0123456789]*.[0123456789]*\*pi", input3_value)
            if len(filter_input[0]) != len(input3_value):
                raise ValueError()
            chan_duoi = float(input3_value.split("*")[0])
        except Exception as ve:
            print(ve)
            error_label = tk.Label(
                Thong_thap_screen,
                text="Lỗi giá trị tần số góc cắt dưới",
                font=("Arial", 24),
            )
            error_label.grid(
                row=10, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W
            )
            return
        try:
            filter_input = re.findall(r"^[0123456789]*.[0123456789]*\*pi", input4_value)
            if len(filter_input[0]) != len(input4_value):
                raise ValueError()
            chan_tren = float(input4_value.split("*")[0])
            print(chan_tren)
        except Exception as ve:
            print(ve)
            error_label = tk.Label(
                Thong_thap_screen,
                text="Lỗi giá trị tần số góc thông dưới",
                font=("Arial", 24),
            )
            error_label.grid(
                row=10, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W
            )
            return
        try:
            filter_input = re.findall(r"^[0123456789]*.[0123456789]*\*pi", input5_value)
            if len(filter_input[0]) != len(input5_value):
                raise ValueError()
            thong_duoi = float(input4_value.split("*")[0])
            print(chan_tren)
        except Exception as ve:
            print(ve)
            error_label = tk.Label(
                Thong_thap_screen,
                text="Lỗi giá trị tần số góc cắt trên",
                font=("Arial", 24),
            )
            error_label.grid(
                row=10, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W
            )
            return
        try:
            filter_input = re.findall(r"^[0123456789]*.[0123456789]*\*pi", input6_value)
            if len(filter_input[0]) != len(input6_value):
                raise ValueError()
            thong_tren = float(input4_value.split("*")[0])
            print(chan_tren)
        except Exception as ve:
            print(ve)
            error_label = tk.Label(
                Thong_thap_screen,
                text="Lỗi giá trị tần số góc thông trên",
                font=("Arial", 24),
            )
            error_label.grid(
                row=10, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W
            )
            return
        IIR.bandpassDraw(
            [chan_duoi, thong_duoi], [chan_tren, thong_tren], Rp, As, filter
        )

    Thong_thap_screen = tk.Toplevel(app)
    Thong_thap_screen.title("Input Screen")
    Thong_thap_screen.geometry("900x600")
    Thong_thap_screen.title("Bộ lọc IIR với thông dải")
    # Create input fields
    dao_dong_trong_giai_thong_label = tk.Label(Thong_thap_screen, text="Rp:")
    dao_dong_trong_giai_thong_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    dao_dong_trong_giai_thong = tk.Entry(Thong_thap_screen)
    dao_dong_trong_giai_thong.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_dao_dong_trong_giai_thong = tk.Label(Thong_thap_screen, text="dB")
    chuthich_dao_dong_trong_giai_thong.grid(
        row=0, column=2, padx=5, pady=5, sticky=tk.W
    )
    # input As
    suy_giam_trong_giai_chan_label = tk.Label(Thong_thap_screen, text="As:")
    suy_giam_trong_giai_chan_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    suy_giam_trong_giai_chan = tk.Entry(Thong_thap_screen)
    suy_giam_trong_giai_chan.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_suy_giam_trong_giai_chan = tk.Label(Thong_thap_screen, text="dB")
    chuthich_suy_giam_trong_giai_chan.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)

    tan_so_cat_duoi_label = tk.Label(Thong_thap_screen, text="tần số góc cắt dưới Wp1:")
    tan_so_cat_duoi_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    tan_so_cat_duoi = tk.Entry(Thong_thap_screen)
    tan_so_cat_duoi.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_tan_so_cat_duoi = tk.Label(Thong_thap_screen, text="Vd: 0.5*pi")
    chuthich_tan_so_cat_duoi.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)

    tan_so_thong_duoi_label = tk.Label(
        Thong_thap_screen, text="tần số góc thông dưới Ws1:"
    )
    tan_so_thong_duoi_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
    tan_so_thong_duoi = tk.Entry(Thong_thap_screen)
    tan_so_thong_duoi.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_tan_so_thong_duoi = tk.Label(Thong_thap_screen, text="Vd: 0.5*pi")
    chuthich_tan_so_thong_duoi.grid(row=3, column=2, padx=5, pady=5, sticky=tk.W)

    # Create input fields
    tan_so_cat_tren_label = tk.Label(Thong_thap_screen, text="tần số góc cắt trên Wp2:")
    tan_so_cat_tren_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
    tan_so_cat_tren = tk.Entry(Thong_thap_screen)
    tan_so_cat_tren.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_tan_so_cat_tren = tk.Label(Thong_thap_screen, text="Vd: 0.5*pi")
    chuthich_tan_so_cat_tren.grid(row=4, column=2, padx=5, pady=5, sticky=tk.W)

    tan_so_thong_tren_label = tk.Label(
        Thong_thap_screen, text="tần số góc thông trên Ws2:"
    )
    tan_so_thong_tren_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
    tan_so_thong_tren = tk.Entry(Thong_thap_screen)
    tan_so_thong_tren.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_tan_so_thong_tren = tk.Label(Thong_thap_screen, text="Vd: 0.5*pi")
    chuthich_tan_so_thong_tren.grid(row=5, column=2, padx=5, pady=5, sticky=tk.W)
    # choose filter
    selected_option = tk.StringVar()
    i = 0
    for option in window_IIRmode:
        radio_button = tk.Radiobutton(
            Thong_thap_screen,
            text=option,
            variable=selected_option,
            value=option,
            command=lambda value=option: on_radio_button_clicked(value),
        )
        radio_button.grid(row=6, column=i, padx=5, pady=5, sticky=tk.W)
        i += 1
    # Create a button
    button = tk.Button(Thong_thap_screen, text="Submit", command=on_button_click)
    button.grid(row=7, column=0, columnspan=3, padx=5, pady=5)
    new_label = tk.Label(Thong_thap_screen, text="tham số pi được ký hiệu là pi")
    new_label.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
    new_label = tk.Label(
        Thong_thap_screen, text="nếu giá trị tần số góc là 0 thì nhập vào input là 0*pi"
    )
    new_label.grid(row=9, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)


def IIR_Chan_dai_click():
    filter = ""

    def on_radio_button_clicked(value):
        print("value")
        global filter
        filter = value
        print(filter)

    def on_button_click():
        global filter
        print("clik")
        # clear previous error
        clear_label = tk.Label(
            Thong_thap_screen,
            text="                                                  ",
            font=("Arial", 24),
        )
        clear_label.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
        # Get values from the entry widgets
        input1_value = dao_dong_trong_giai_thong.get()
        input2_value = suy_giam_trong_giai_chan.get()
        input3_value = tan_so_cat_duoi.get()
        input4_value = tan_so_thong_duoi.get()
        input5_value = tan_so_cat_tren.get()
        input6_value = tan_so_thong_tren
        if filter == "":
            return
        try:
            Rp = float(input1_value)
        except Exception as ve:
            error_label = tk.Label(
                Thong_thap_screen,
                text="Lỗi giá trị Rp",
                font=("Arial", 24),
            )
            error_label.grid(
                row=10, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W
            )
            return
        try:
            As = float(input2_value)
        except Exception as ve:
            error_label = tk.Label(
                Thong_thap_screen,
                text="Lỗi giá trị As",
                font=("Arial", 24),
            )
            error_label.grid(
                row=10, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W
            )
            return
        try:
            filter_input = re.findall(r"^[0123456789]*.[0123456789]*\*pi", input3_value)
            if len(filter_input[0]) != len(input3_value):
                raise ValueError()
            chan_duoi = float(input3_value.split("*")[0])
        except Exception as ve:
            print(ve)
            error_label = tk.Label(
                Thong_thap_screen,
                text="Lỗi giá trị tần số góc cắt dưới",
                font=("Arial", 24),
            )
            error_label.grid(
                row=10, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W
            )
            return
        try:
            filter_input = re.findall(r"^[0123456789]*.[0123456789]*\*pi", input4_value)
            if len(filter_input[0]) != len(input4_value):
                raise ValueError()
            chan_tren = float(input4_value.split("*")[0])
            print(chan_tren)
        except Exception as ve:
            print(ve)
            error_label = tk.Label(
                Thong_thap_screen,
                text="Lỗi giá trị tần số góc thông dưới",
                font=("Arial", 24),
            )
            error_label.grid(
                row=10, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W
            )
            return
        try:
            filter_input = re.findall(r"^[0123456789]*.[0123456789]*\*pi", input5_value)
            if len(filter_input[0]) != len(input5_value):
                raise ValueError()
            thong_duoi = float(input4_value.split("*")[0])
            print(chan_tren)
        except Exception as ve:
            print(ve)
            error_label = tk.Label(
                Thong_thap_screen,
                text="Lỗi giá trị tần số góc cắt trên",
                font=("Arial", 24),
            )
            error_label.grid(
                row=10, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W
            )
            return
        try:
            filter_input = re.findall(r"^[0123456789]*.[0123456789]*\*pi", input6_value)
            if len(filter_input[0]) != len(input6_value):
                raise ValueError()
            thong_tren = float(input4_value.split("*")[0])
            print(chan_tren)
        except Exception as ve:
            print(ve)
            error_label = tk.Label(
                Thong_thap_screen,
                text="Lỗi giá trị tần số góc thông trên",
                font=("Arial", 24),
            )
            error_label.grid(
                row=10, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W
            )
            return
        IIR.bandstopDraw(
            [chan_duoi, thong_duoi], [chan_tren, thong_tren], Rp, As, filter
        )

    Thong_thap_screen = tk.Toplevel(app)
    Thong_thap_screen.title("Input Screen")
    Thong_thap_screen.geometry("900x600")
    Thong_thap_screen.title("Bộ lọc IIR với chắn dải")
    # Create input fields
    dao_dong_trong_giai_thong_label = tk.Label(Thong_thap_screen, text="Rp:")
    dao_dong_trong_giai_thong_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    dao_dong_trong_giai_thong = tk.Entry(Thong_thap_screen)
    dao_dong_trong_giai_thong.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_dao_dong_trong_giai_thong = tk.Label(Thong_thap_screen, text="dB")
    chuthich_dao_dong_trong_giai_thong.grid(
        row=0, column=2, padx=5, pady=5, sticky=tk.W
    )
    # input As
    suy_giam_trong_giai_chan_label = tk.Label(Thong_thap_screen, text="As:")
    suy_giam_trong_giai_chan_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    suy_giam_trong_giai_chan = tk.Entry(Thong_thap_screen)
    suy_giam_trong_giai_chan.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_suy_giam_trong_giai_chan = tk.Label(Thong_thap_screen, text="dB")
    chuthich_suy_giam_trong_giai_chan.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)

    tan_so_cat_duoi_label = tk.Label(Thong_thap_screen, text="tần số góc cắt dưới Wp1:")
    tan_so_cat_duoi_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    tan_so_cat_duoi = tk.Entry(Thong_thap_screen)
    tan_so_cat_duoi.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_tan_so_cat_duoi = tk.Label(Thong_thap_screen, text="Vd: 0.5*pi")
    chuthich_tan_so_cat_duoi.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)

    tan_so_thong_duoi_label = tk.Label(
        Thong_thap_screen, text="tần số góc thông dưới Ws1:"
    )
    tan_so_thong_duoi_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
    tan_so_thong_duoi = tk.Entry(Thong_thap_screen)
    tan_so_thong_duoi.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_tan_so_thong_duoi = tk.Label(Thong_thap_screen, text="Vd: 0.5*pi")
    chuthich_tan_so_thong_duoi.grid(row=3, column=2, padx=5, pady=5, sticky=tk.W)

    # Create input fields
    tan_so_cat_tren_label = tk.Label(Thong_thap_screen, text="tần số góc cắt trên Wp2:")
    tan_so_cat_tren_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
    tan_so_cat_tren = tk.Entry(Thong_thap_screen)
    tan_so_cat_tren.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_tan_so_cat_tren = tk.Label(Thong_thap_screen, text="Vd: 0.5*pi")
    chuthich_tan_so_cat_tren.grid(row=4, column=2, padx=5, pady=5, sticky=tk.W)

    tan_so_thong_tren_label = tk.Label(
        Thong_thap_screen, text="tần số góc thông trên Ws2:"
    )
    tan_so_thong_tren_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
    tan_so_thong_tren = tk.Entry(Thong_thap_screen)
    tan_so_thong_tren.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_tan_so_thong_tren = tk.Label(Thong_thap_screen, text="Vd: 0.5*pi")
    chuthich_tan_so_thong_tren.grid(row=5, column=2, padx=5, pady=5, sticky=tk.W)
    # choose filter
    selected_option = tk.StringVar()
    i = 0
    for option in window_IIRmode:
        radio_button = tk.Radiobutton(
            Thong_thap_screen,
            text=option,
            variable=selected_option,
            value=option,
            command=lambda value=option: on_radio_button_clicked(value),
        )
        radio_button.grid(row=6, column=i, padx=5, pady=5, sticky=tk.W)
        i += 1
    # Create a button
    button = tk.Button(Thong_thap_screen, text="Submit", command=on_button_click)
    button.grid(row=7, column=0, columnspan=3, padx=5, pady=5)
    new_label = tk.Label(Thong_thap_screen, text="tham số pi được ký hiệu là pi")
    new_label.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
    new_label = tk.Label(
        Thong_thap_screen, text="nếu giá trị tần số góc là 0 thì nhập vào input là 0*pi"
    )
    new_label.grid(row=9, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)


# thông thấp screen
def Thong_thap_click():
    def on_button_click():
        # clear previous error
        clear_label = tk.Label(
            Thong_thap_screen,
            text="                                                  ",
            font=("Arial", 24),
        )
        clear_label.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
        # Get values from the entry widgets
        input1_value = do_gon_song.get()
        input2_value = tan_so_chan_duoi.get()
        input3_value = tan_so_chan_tren.get()
        try:
            gon_song = float(input1_value)
        except Exception as ve:
            error_label = tk.Label(
                Thong_thap_screen,
                text="Lỗi giá trị độ gợn sóng",
                font=("Arial", 24),
            )
            error_label.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
            return
        try:
            filter_input = re.findall(r"^[0123456789]*.[0123456789]*\*pi", input2_value)
            if len(filter_input[0]) != len(input2_value):
                raise ValueError()
            chan_duoi = float(input2_value.split("*")[0])
        except Exception as ve:
            print(ve)
            error_label = tk.Label(
                Thong_thap_screen,
                text="Lỗi giá trị tần số góc chắn dưới",
                font=("Arial", 24),
            )
            error_label.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
            return
        try:
            filter_input = re.findall(r"^[0123456789]*.[0123456789]*\*pi", input3_value)
            if len(filter_input[0]) != len(input2_value):
                raise ValueError()
            chan_tren = float(input3_value.split("*")[0])
            print(chan_tren)
        except Exception as ve:
            print(ve)
            error_label = tk.Label(
                Thong_thap_screen,
                text="Lỗi giá trị tần số góc chắn trên",
                font=("Arial", 24),
            )
            error_label.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
            return
        FIR.thongthap(chan_duoi, chan_tren, gon_song)

    Thong_thap_screen = tk.Toplevel(app)
    Thong_thap_screen.title("Input Screen")
    Thong_thap_screen.geometry("900x600")
    Thong_thap_screen.title("Bộ lọc FIR với thông thấp")
    # Create input fields
    do_gon_song_label = tk.Label(Thong_thap_screen, text="Độ gợn sóng:")
    do_gon_song_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    do_gon_song = tk.Entry(Thong_thap_screen)
    do_gon_song.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_do_gon_song = tk.Label(Thong_thap_screen, text="Vd: 0.0005")
    chuthich_do_gon_song.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

    tan_so_chan_duoi_label = tk.Label(Thong_thap_screen, text="tần số góc chắn dưới:")
    tan_so_chan_duoi_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    tan_so_chan_duoi = tk.Entry(Thong_thap_screen)
    tan_so_chan_duoi.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_tan_so_chan_duoi = tk.Label(Thong_thap_screen, text="Vd: 0.5*pi")
    chuthich_tan_so_chan_duoi.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)

    tan_so_chan_tren_label = tk.Label(Thong_thap_screen, text="tần số góc chắn trên:")
    tan_so_chan_tren_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    tan_so_chan_tren = tk.Entry(Thong_thap_screen)
    tan_so_chan_tren.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_tan_so_chan_tren = tk.Label(Thong_thap_screen, text="Vd: 0.5*pi")
    chuthich_tan_so_chan_tren.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)

    # Create a button
    button = tk.Button(Thong_thap_screen, text="Submit", command=on_button_click)
    button.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
    new_label = tk.Label(Thong_thap_screen, text="tham số pi được ký hiệu là pi")
    new_label.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
    new_label = tk.Label(
        Thong_thap_screen, text="nếu giá trị tần số góc là 0 thì nhập vào input là 0*pi"
    )
    new_label.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)


# thông cao
def Thong_cao_click():
    def on_button_click():
        # clear previous error
        clear_label = tk.Label(
            Thong_cao_screen,
            text="                                                  ",
            font=("Arial", 24),
        )
        clear_label.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
        # Get values from the entry widgets
        input1_value = do_gon_song.get()
        input2_value = tan_so_chan_duoi.get()
        input3_value = tan_so_chan_tren.get()
        try:
            gon_song = float(input1_value)
        except Exception as ve:
            error_label = tk.Label(
                Thong_cao_screen,
                text="Lỗi giá trị độ gợn sóng",
                font=("Arial", 24),
            )
            error_label.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
            return
        try:
            filter_input = re.findall(r"^[0123456789]*.[0123456789]*\*pi", input2_value)
            if len(filter_input[0]) != len(input2_value):
                raise ValueError()
            chan_duoi = float(input2_value.split("*")[0])
        except Exception as ve:
            print(ve)
            error_label = tk.Label(
                Thong_cao_screen,
                text="Lỗi giá trị tần số góc chắn dưới",
                font=("Arial", 24),
            )
            error_label.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
            return
        try:
            filter_input = re.findall(r"^[0123456789]*.[0123456789]*\*pi", input3_value)
            if len(filter_input[0]) != len(input2_value):
                raise ValueError()
            chan_tren = float(input3_value.split("*")[0])
        except Exception as ve:
            print(ve)
            error_label = tk.Label(
                Thong_cao_screen,
                text="Lỗi giá trị tần số góc chắn trên",
                font=("Arial", 24),
            )
            error_label.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
            return
        FIR.thongcao(chan_duoi, chan_tren, gon_song)
        return

    Thong_cao_screen = tk.Toplevel(app)
    Thong_cao_screen.geometry("900x600")
    Thong_cao_screen.title("Bộ lọc FIR với thông cao")
    # Create input fields
    do_gon_song_label = tk.Label(Thong_cao_screen, text="Độ gợn sóng:")
    do_gon_song_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    do_gon_song = tk.Entry(Thong_cao_screen)
    do_gon_song.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_do_gon_song = tk.Label(Thong_cao_screen, text="Vd: 0.0005")
    chuthich_do_gon_song.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

    tan_so_chan_duoi_label = tk.Label(Thong_cao_screen, text="tần số góc chắn dưới:")
    tan_so_chan_duoi_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    tan_so_chan_duoi = tk.Entry(Thong_cao_screen)
    tan_so_chan_duoi.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_tan_so_chan_duoi = tk.Label(Thong_cao_screen, text="Vd: 0.5*pi")
    chuthich_tan_so_chan_duoi.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)

    tan_so_chan_tren_label = tk.Label(Thong_cao_screen, text="tần số góc chắn trên:")
    tan_so_chan_tren_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    tan_so_chan_tren = tk.Entry(Thong_cao_screen)
    tan_so_chan_tren.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_tan_so_chan_tren = tk.Label(Thong_cao_screen, text="Vd: 0.5*pi")
    chuthich_tan_so_chan_tren.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)

    # Create a button
    button = tk.Button(Thong_cao_screen, text="Submit", command=on_button_click)
    button.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
    new_label = tk.Label(Thong_cao_screen, text="tham số pi được ký hiệu là pi")
    new_label.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
    new_label = tk.Label(
        Thong_cao_screen, text="nếu giá trị tần số góc là 0 thì nhập vào input là 0*pi"
    )
    new_label.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)


# thông dải
def Thong_dai_click():
    def on_button_click():
        # clear previous error
        clear_label = tk.Label(
            Thong_dai_screen,
            text="                                                  ",
            font=("Arial", 24),
        )
        clear_label.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
        # Get values from the entry widgets
        input1_value = do_gon_song.get()
        input2_value = tan_so_cat_duoi.get()
        input3_value = tan_so_thong_duoi.get()
        input4_value = tan_so_cat_tren.get()
        input5_value = tan_so_thong_tren.get()
        try:
            gon_song = float(input1_value)
        except Exception as ve:
            error_label = tk.Label(
                Thong_dai_screen,
                text="Lỗi giá trị độ gợn sóng",
                font=("Arial", 24),
            )
            error_label.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
            return
        try:
            filter_input = re.findall(r"^[0123456789]*.[0123456789]*\*pi", input2_value)
            if len(filter_input[0]) != len(input2_value):
                raise ValueError()
            cat_duoi = float(input2_value.split("*")[0])
        except Exception as ve:
            print(ve)
            error_label = tk.Label(
                Thong_dai_screen,
                text="Lỗi giá trị tần số góc cắt dưới",
                font=("Arial", 24),
            )
            error_label.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
            return
        try:
            filter_input = re.findall(r"^[0123456789]*.[0123456789]*\*pi", input3_value)
            if len(filter_input[0]) != len(input3_value):
                raise ValueError()
            thong_duoi = float(input3_value.split("*")[0])
        except Exception as ve:
            print(ve)
            error_label = tk.Label(
                Thong_dai_screen,
                text="Lỗi giá trị tần số góc thông dưới",
                font=("Arial", 24),
            )
            error_label.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
            return
        try:
            filter_input = re.findall(r"^[0123456789]*.[0123456789]*\*pi", input4_value)
            if len(filter_input[0]) != len(input4_value):
                raise ValueError()
            cat_tren = float(input4_value.split("*")[0])
        except Exception as ve:
            print(ve)
            error_label = tk.Label(
                Thong_dai_screen,
                text="Lỗi giá trị tần số góc cắt trên",
                font=("Arial", 24),
            )
            error_label.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
            return
        try:
            filter_input = re.findall(r"^[0123456789]*.[0123456789]*\*pi", input5_value)
            if len(filter_input[0]) != len(input5_value):
                raise ValueError()
            thong_tren = float(input5_value.split("*")[0])
        except Exception as ve:
            print(ve)
            error_label = tk.Label(
                Thong_dai_screen,
                text="Lỗi giá trị tần số góc thông trên",
                font=("Arial", 24),
            )
            error_label.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
            return
        FIR.thongdai(cat_duoi, thong_duoi, cat_tren, thong_tren, gon_song)

    Thong_dai_screen = tk.Toplevel(app)
    Thong_dai_screen.geometry("900x600")
    Thong_dai_screen.title("Bộ lọc FIR với thông dải")

    # Create input fields
    do_gon_song_label = tk.Label(Thong_dai_screen, text="Độ gợn sóng:")
    do_gon_song_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    do_gon_song = tk.Entry(Thong_dai_screen)
    do_gon_song.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_do_gon_song = tk.Label(Thong_dai_screen, text="Vd: 0.0005")
    chuthich_do_gon_song.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

    tan_so_cat_duoi_label = tk.Label(Thong_dai_screen, text="tần số góc cắt dưới:")
    tan_so_cat_duoi_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    tan_so_cat_duoi = tk.Entry(Thong_dai_screen)
    tan_so_cat_duoi.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_tan_so_cat_duoi = tk.Label(Thong_dai_screen, text="Vd: 0.5*pi")
    chuthich_tan_so_cat_duoi.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)

    tan_so_thong_duoi_label = tk.Label(Thong_dai_screen, text="tần số góc thông dưới:")
    tan_so_thong_duoi_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    tan_so_thong_duoi = tk.Entry(Thong_dai_screen)
    tan_so_thong_duoi.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_tan_so_thong_duoi = tk.Label(Thong_dai_screen, text="Vd: 0.5*pi")
    chuthich_tan_so_thong_duoi.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)

    # Create input fields
    tan_so_cat_tren_label = tk.Label(Thong_dai_screen, text="tần số góc cắt trên:")
    tan_so_cat_tren_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
    tan_so_cat_tren = tk.Entry(Thong_dai_screen)
    tan_so_cat_tren.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_tan_so_cat_tren = tk.Label(Thong_dai_screen, text="Vd: 0.5*pi")
    chuthich_tan_so_cat_tren.grid(row=3, column=2, padx=5, pady=5, sticky=tk.W)

    tan_so_thong_tren_label = tk.Label(Thong_dai_screen, text="tần số góc thông trên:")
    tan_so_thong_tren_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
    tan_so_thong_tren = tk.Entry(Thong_dai_screen)
    tan_so_thong_tren.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_tan_so_thong_tren = tk.Label(Thong_dai_screen, text="Vd: 0.5*pi")
    chuthich_tan_so_thong_tren.grid(row=4, column=2, padx=5, pady=5, sticky=tk.W)

    # Create a button
    button = tk.Button(Thong_dai_screen, text="Submit", command=on_button_click)
    button.grid(row=5, column=0, columnspan=3, padx=5, pady=5)
    new_label = tk.Label(Thong_dai_screen, text="tham số pi được ký hiệu là pi")
    new_label.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
    new_label = tk.Label(
        Thong_dai_screen, text="nếu giá trị tần số góc là 0 thì nhập vào input là 0*pi"
    )
    new_label.grid(row=7, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)


# chắn dải
def Chan_dai_click():
    def on_button_click():
        # clear previous error
        clear_label = tk.Label(
            Chan_dai_screen,
            text="                                                  ",
            font=("Arial", 24),
        )
        clear_label.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
        # Get values from the entry widgets
        input1_value = do_gon_song.get()
        input2_value = tan_so_cat_duoi.get()
        input3_value = tan_so_thong_duoi.get()
        input4_value = tan_so_cat_tren.get()
        input5_value = tan_so_thong_tren.get()
        try:
            gon_song = float(input1_value)
        except Exception as ve:
            error_label = tk.Label(
                Chan_dai_screen,
                text="Lỗi giá trị độ gợn sóng",
                font=("Arial", 24),
            )
            error_label.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
            return
        try:
            filter_input = re.findall(r"^[0123456789]*.[0123456789]*\*pi", input2_value)
            if len(filter_input[0]) != len(input2_value):
                raise ValueError()
            cat_duoi = float(input2_value.split("*")[0])
        except Exception as ve:
            print(ve)
            error_label = tk.Label(
                Chan_dai_screen,
                text="Lỗi giá trị tần số góc cắt dưới",
                font=("Arial", 24),
            )
            error_label.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
            return
        try:
            filter_input = re.findall(r"^[0123456789]*.[0123456789]*\*pi", input3_value)
            if len(filter_input[0]) != len(input3_value):
                raise ValueError()
            thong_duoi = float(input3_value.split("*")[0])
        except Exception as ve:
            print(ve)
            error_label = tk.Label(
                Chan_dai_screen,
                text="Lỗi giá trị tần số góc thông dưới",
                font=("Arial", 24),
            )
            error_label.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
            return
        try:
            filter_input = re.findall(r"^[0123456789]*.[0123456789]*\*pi", input4_value)
            if len(filter_input[0]) != len(input4_value):
                raise ValueError()
            cat_tren = float(input3_value.split("*")[0])
        except Exception as ve:
            print(ve)
            error_label = tk.Label(
                Chan_dai_screen,
                text="Lỗi giá trị tần số góc cắt trên",
                font=("Arial", 24),
            )
            error_label.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
            return
        try:
            filter_input = re.findall(r"^[0123456789]*.[0123456789]*\*pi", input5_value)
            if len(filter_input[0]) != len(input5_value):
                raise ValueError()
            thong_tren = float(input3_value.split("*")[0])
        except Exception as ve:
            print(ve)
            error_label = tk.Label(
                Chan_dai_screen,
                text="Lỗi giá trị tần số góc thông trên",
                font=("Arial", 24),
            )
            error_label.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
            return
        FIR.chandai(cat_duoi, thong_duoi, cat_tren, thong_tren, gon_song)

    Chan_dai_screen = tk.Toplevel(app)
    Chan_dai_screen.geometry("900x600")
    Chan_dai_screen.title("Bộ lọc FIR với chắn dải")

    # Create input fields
    do_gon_song_label = tk.Label(Chan_dai_screen, text="Độ gợn sóng:")
    do_gon_song_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    do_gon_song = tk.Entry(Chan_dai_screen)
    do_gon_song.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_do_gon_song = tk.Label(Chan_dai_screen, text="Vd: 0.0005")
    chuthich_do_gon_song.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

    tan_so_cat_duoi_label = tk.Label(Chan_dai_screen, text="tần số góc cắt dưới:")
    tan_so_cat_duoi_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    tan_so_cat_duoi = tk.Entry(Chan_dai_screen)
    tan_so_cat_duoi.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_tan_so_cat_duoi = tk.Label(Chan_dai_screen, text="Vd: 0.5*pi")
    chuthich_tan_so_cat_duoi.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)

    tan_so_thong_duoi_label = tk.Label(Chan_dai_screen, text="tần số góc thông dưới:")
    tan_so_thong_duoi_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    tan_so_thong_duoi = tk.Entry(Chan_dai_screen)
    tan_so_thong_duoi.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_tan_so_thong_duoi = tk.Label(Chan_dai_screen, text="Vd: 0.5*pi")
    chuthich_tan_so_thong_duoi.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)

    # Create input fields
    tan_so_cat_tren_label = tk.Label(Chan_dai_screen, text="tần số góc cắt trên:")
    tan_so_cat_tren_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
    tan_so_cat_tren = tk.Entry(Chan_dai_screen)
    tan_so_cat_tren.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_tan_so_cat_tren = tk.Label(Chan_dai_screen, text="Vd: 0.5*pi")
    chuthich_tan_so_cat_tren.grid(row=3, column=2, padx=5, pady=5, sticky=tk.W)

    tan_so_thong_tren_label = tk.Label(Chan_dai_screen, text="tần số góc thông trên:")
    tan_so_thong_tren_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
    tan_so_thong_tren = tk.Entry(Chan_dai_screen)
    tan_so_thong_tren.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
    chuthich_tan_so_thong_tren = tk.Label(Chan_dai_screen, text="Vd: 0.5*pi")
    chuthich_tan_so_thong_tren.grid(row=4, column=2, padx=5, pady=5, sticky=tk.W)

    # Create a button
    button = tk.Button(Chan_dai_screen, text="Submit", command=on_button_click)
    button.grid(row=5, column=0, columnspan=3, padx=5, pady=5)
    new_label = tk.Label(Chan_dai_screen, text="tham số pi được ký hiệu là pi")
    new_label.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
    new_label = tk.Label(
        Chan_dai_screen, text="nếu giá trị tần số góc là 0 thì nhập vào input là 0*pi"
    )
    new_label.grid(row=7, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)


func_mode = [Thong_cao_click, Thong_thap_click, Thong_dai_click, Chan_dai_click]
func_IIRmode = [
    IIR_Thong_cao_click,
    IIR_Thong_thap_click,
    IIR_Thong_dai_click,
    IIR_Chan_dai_click,
]


def button1_click():
    # Create a new window
    new_window = tk.Toplevel(app)
    new_window.geometry("900x600")
    new_window.title("Button 1 Clicked")

    # Create a label in the new window
    new_label = tk.Label(new_window, text="Xây dựng bộ lọc FIR")
    new_label.pack(pady=10)
    # Create four buttons in the new window
    for i in range(0, 4):
        new_button = tk.Button(
            new_window,
            text=f"Bộ lọc {mode_FIR[i]}",
            command=func_mode[i],
        )
        new_button.pack(pady=5)


def button2_click():
    # Create a new window
    new_window = tk.Toplevel(app)
    new_window.geometry("900x600")
    new_window.title("Button 1 Clicked")
    # Create a label in the new window
    new_label = tk.Label(new_window, text="Xây dựng bộ lọc IIR")
    new_label.pack(pady=10)
    # Create four buttons in the new window
    for i in range(0, 4):
        new_button = tk.Button(
            new_window,
            text=f"Bộ lọc {mode_FIR[i]}",
            command=func_IIRmode[i],
        )
        new_button.pack(pady=5)


# Create the main window
app = tk.Tk()
app.title("Main Screen")

# Set the default width and height
app.geometry("900x600")  # Width x Height

# Create a label widget
label = tk.Label(app, text="Main Screen")
label.pack(pady=10)

# Create the first button
button1 = tk.Button(app, text="Button 1: FIR", command=button1_click)
button1.pack(pady=5)

# Create the second button
button2 = tk.Button(app, text="Button 2: IIR", command=button2_click)
button2.pack(pady=5)

# Start the Tkinter event loop
app.mainloop()

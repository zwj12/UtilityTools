import os
import sys
import threading
import socket
import time
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import unicodedata

# ===================== 配置区 =====================
TCP_PORT = 8086
FRAME_END_MARK = "||END||"
SINGLE_ITEM_MARK = "||SINGLE||"
ALL_DONE_MARK = "||ALL_DONE||"

# 焊缝 txt 结果固定存放目录，机器人只传文件名，不传完整路径
WELD_RESULT_ROOT = r"D:/weld_result"
# True = 调试模式：忽略机器人发来路径，复用 GUI 手动解析的数据；False = 正式工作模式
DEBUG_MODE = True
# ==================================================

TCP_RUN_FLAG = True
tcp_server_thread = None


def wait_file_ready(filepath, max_wait_sec=10, stable_delay=0.3):
    """等待文件写入完成，检测文件大小稳定"""
    start = time.time()
    prev_size = -1
    while time.time() - start < max_wait_sec:
        if not os.path.exists(filepath):
            time.sleep(0.25)
            continue
        try:
            curr_size = os.path.getsize(filepath)
            if curr_size == prev_size and curr_size > 0:
                time.sleep(stable_delay)
                return True
            prev_size = curr_size
        except OSError:
            pass
        time.sleep(0.2)
    return False


def parse_fault_items(filepath):
    """解析检测 txt，返回 [(name, start, stop, length), ...]"""
    fault_list = []
    try:
        with open(filepath, 'r', encoding="utf-8") as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding="gbk") as f:
            lines = f.readlines()
    idx = 0
    total_lines = len(lines)
    while idx < total_lines:
        line = lines[idx].strip()
        if line.startswith("Measures"):
            measure_name = ""
            measure_result = ""
            idx += 1
            # 跳到 Measures 下一行
            while idx < total_lines:
                sub_line = lines[idx].strip()
                if sub_line.startswith("Measures"):
                    break  # 遇到下一个 Measures，退出本 Measure 块
                if sub_line.startswith("Name:"):
                    measure_name = sub_line.split(":", 1)[-1].strip()
                if sub_line.startswith("Result:"):
                    measure_result = sub_line.split(":", 1)[-1].strip()
                if sub_line.startswith("Defect"):
                    d_start = None
                    d_stop = None
                    d_len = None
                    idx += 1
                    # 解析 Defect 下面的 Start/Stop/Length
                    while idx < total_lines:
                        d_line = lines[idx].strip()
                        if d_line.startswith(("Defect", "Measures")):
                            break
                        if d_line.startswith("Start:"):
                            d_start = float(d_line.split(":", 1)[-1])
                        elif d_line.startswith("Stop:"):
                            d_stop = float(d_line.split(":", 1)[-1])
                        elif d_line.startswith("Length:"):
                            d_len = float(d_line.split(":", 1)[-1])
                        idx += 1
                    # 收集缺陷
                    if measure_result == "Failed" and d_start is not None and d_stop is not None and d_len is not None:
                        fault_list.append((measure_name, d_start, d_stop, d_len))
                    continue
                idx += 1
        else:
            idx += 1
    return fault_list


class FaultSendApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weld Fault Parse Service (Robot Auto‑Trigger)")
        self.root.geometry("980x640")
        self.file_path_var = tk.StringVar()
        self.fault_data = []

        top_frame = tk.Frame(root, padx=6, pady=8)
        top_frame.pack(fill=tk.X)
        tk.Label(top_frame, text="TXT File Path:").pack(side=tk.LEFT)
        tk.Entry(top_frame, textvariable=self.file_path_var, width=74).pack(side=tk.LEFT, padx=6)
        tk.Button(top_frame, text="Select File", command=self.select_file).pack(side=tk.LEFT, padx=4)
        tk.Button(top_frame, text="Manual Parse", command=self.parse_txt, bg="#3478db", fg="white").pack(side=tk.LEFT, padx=4)
        tk.Button(top_frame, text="Debug‑Show‑Payload", command=self.debug_show_payload, bg="#9955bb", fg="white").pack(side=tk.LEFT, padx=4)
        tk.Button(top_frame, text="Manual Send (NoConn)", command=self.send_fault_to_client, bg="#23aa44", fg="white").pack(side=tk.LEFT, padx=4)

        tk.Label(root, text=f"Log | DEBUG_MODE={DEBUG_MODE} | Robot cmd example: GET_FAULT|result.txt||END||",
                 font=("Consolas", 11), fg="#204099").pack(anchor="w", padx=8)
        self.log_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 11))
        self.log_text.pack(expand=True, fill=tk.BOTH, padx=6, pady=4)

        self.start_tcp_server()

    def log(self, msg):
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def select_file(self):
        fp = filedialog.askopenfilename(filetypes=[("Text file", "*.txt")])
        if fp:
            self.file_path_var.set(fp)

    def parse_txt(self):
        fp = self.file_path_var.get().strip()
        if not os.path.exists(fp):
            messagebox.showerror("Error", "File not found")
            return
        self.log_text.delete(1.0, tk.END)
        self.log(f"Manual parse file: {fp}")
        self.fault_data = parse_fault_items(fp)
        self.log(f"DEBUG: fault_data length = {len(self.fault_data)}")
        self.log(f"DEBUG raw list: {self.fault_data}")
        if len(self.fault_data) == 0:
            self.log("✅Parse complete, zero Failed faults")
            return
        self.log(f"====Parsed {len(self.fault_data)} faults====")
        for name, s, st, l in self.fault_data:
            self.log(f"{name} | Start={s:.3f} | Stop={st:.3f} | Length={l:.3f}")

    def debug_show_payload(self):
        """本地预览将要发送的每条报文，不发送网络"""
        self.log("=======Preview per‑item payload (NO SEND)======")
        for name, start, stop, length in self.fault_data:
            line = f"FAULT|{name}|{start:.3f}|{stop:.3f}|{length:.3f}|||{SINGLE_ITEM_MARK}\n"
            self.log(repr(line))
        self.log(repr(f"{ALL_DONE_MARK}\n"))
        self.log("============================================")

    def send_fault_to_client(self, conn=None):
        """逐条发送缺陷，每条独立报文；全部完成发送 ALL_DONE 标记"""
        if conn is None:
            self.log("⚠️ No client connected, skip socket send")
            return
        try:
            send_count = 0
            for name, start, stop, length in self.fault_data:
                msg = f"FAULT|{name}|{start:.3f}|{stop:.3f}|{length:.3f}|||{SINGLE_ITEM_MARK}\n"
                conn.sendall(msg.encode("ascii"))
                send_count += 1
                self.log(f"SEND item:{msg.strip()}")
                time.sleep(0.008)
            # 发送结束标记
            conn.sendall(f"{ALL_DONE_MARK}\n".encode("ascii"))
            self.log(f"✅All faults sent one‑by‑one, total={send_count}, sent {ALL_DONE_MARK}")
        except Exception as e:
            self.log(f"❌Send exception: {str(e)}")

    def tcp_server_loop(self):
        global TCP_RUN_FLAG
        srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            srv_socket.bind(("0.0.0.0", TCP_PORT))
        except Exception as e:
            self.log(f"❌Bind port {TCP_PORT} fail: {e}")
            return
        srv_socket.listen(3)
        self.log(f"✅TCP server started, listening port {TCP_PORT}")
        while TCP_RUN_FLAG:
            try:
                conn, addr = srv_socket.accept()
            except OSError:
                break
            self.log(f"\n🤖Robot client connected: {addr}")
            self.handle_client(conn)
        srv_socket.close()
        self.log("TCP server thread exit")

    def handle_client(self, conn):
        buf = b""
        mark_bytes = FRAME_END_MARK.encode("utf‑8")
        while True:
            try:
                recv_bytes = conn.recv(2048)
            except Exception:
                break
            if not recv_bytes:
                break
            buf += recv_bytes
            if mark_bytes in buf:
                req_bytes, _ = buf.split(mark_bytes, 1)
                buf = b""
                req_str = req_bytes.decode("utf‑8", errors="ignore").strip()
                self.log(f"Received command: {req_str}")
                if req_str.startswith("GET_FAULT|"):
                    parts = req_str.split("|", 1)
                    if len(parts) >= 2:
                        filename = parts[1].strip()
                        self.log(f"Request filename: {filename}")
                        if DEBUG_MODE:
                            self.log(f"⚠️ DEBUG_MODE ON: reuse UI parsed fault count={len(self.fault_data)}")
                            self.send_fault_to_client(conn)
                        else:
                            full_path = os.path.join(WELD_RESULT_ROOT, filename)
                            self.log(f"Full file path: {full_path}")
                            if not os.path.exists(full_path):
                                resp = f"FILE_NOT_FOUND\n"
                                conn.sendall(resp.encode("ascii"))
                            elif not wait_file_ready(full_path):
                                resp = f"FILE_TIMEOUT\n"
                                conn.sendall(resp.encode("ascii"))
                            else:
                                self.fault_data = parse_fault_items(full_path)
                                self.file_path_var.set(full_path)
                                self.log(f"Parsed fault count={len(self.fault_data)}")
                                self.send_fault_to_client(conn)

                        # ============握手应答逻辑【新增】============
                        self.log("⏳Waiting robot OK acknowledge...")
                        # Windows内核缓冲区刷出延时
                        time.sleep(0.04)
                        ack_buf = b""
                        ack_ok = False
                        conn.settimeout(1.5)
                        try:
                            while True:
                                ack_recv = conn.recv(512)
                                if not ack_recv:
                                    break
                                ack_buf += ack_recv
                                if b"OK" in ack_buf:
                                    ack_ok = True
                                    self.log("✅Received robot OK ack")
                                    break
                        except socket.timeout:
                            self.log("⚠️Wait robot OK timeout(1.5s)")
                        except Exception as e:
                            self.log(f"❌Ack recv error:{e}")
                        # =============================================

                    break
        try:
            conn.close()
        except Exception:
            pass
        self.log("Client connection closed")

    def start_tcp_server(self):
        global tcp_server_thread, TCP_RUN_FLAG
        TCP_RUN_FLAG = True
        tcp_server_thread = threading.Thread(target=self.tcp_server_loop, daemon=True)
        tcp_server_thread.start()


if __name__ == "__main__":
    main_window = tk.Tk()
    app = FaultSendApp(main_window)
    main_window.mainloop()
    TCP_RUN_FLAG = False

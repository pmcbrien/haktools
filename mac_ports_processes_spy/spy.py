import subprocess

def run_lsof(command_args, description):
    print(f"\n=== {description} ===\n")
    try:
        result = subprocess.run(
            ["lsof"] + command_args,
            capture_output=True,
            text=True,
            check=True
        )
        if result.stdout.strip():
            for line in result.stdout.strip().split("\n"):
                print(line)
        else:
            print("No results found.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def get_open_ports():
    # TCP ports in LISTEN state with process info
    run_lsof(["-nP", "-iTCP", "-sTCP:LISTEN"], "TCP Ports (LISTEN) with Process Info")

    # UDP ports in use with process info
    run_lsof(["-nP", "-iUDP"], "UDP Ports (in use) with Process Info")

if __name__ == "__main__":
    get_open_ports()

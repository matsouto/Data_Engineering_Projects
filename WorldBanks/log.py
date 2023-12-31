from datetime import datetime


def log_process(message):
    log_name = "code_log.txt"
    timestamp_format = "%Y-%h-%d-%H:%M:%S"  # Year-Monthname-Day-Hour-Minute-Second
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open("./WorldBanks/" + log_name, "a") as f:
        f.write(timestamp + " " + message + "\n")


if __name__ == "__main__":
    log_process("test")

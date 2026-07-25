# Banker's Algorithm - ENCS3390 Project 2
# Run:
#   python bankers.py
# or:
#   python bankers.py input.txt

import sys

N = 0
M = 0
max_matrix = []
allocation = []
need = []
available = []


def load_input(filename):
    global N, M, max_matrix, allocation, need, available

    try:
        f = open(filename, "r")
        tokens = f.read().split()
        f.close()
    except FileNotFoundError:
        print("Error: input file not found:", filename)
        sys.exit(1)

    try:
        n_index = tokens.index("N")
        m_index = tokens.index("M")

        N = int(tokens[n_index + 2])
        M = int(tokens[m_index + 2])

        max_index = tokens.index("MAX")
        values = []

        for i in range(N * M):
            values.append(int(tokens[max_index + 1 + i]))

        max_matrix = []
        k = 0
        for i in range(N):
            row = []
            for j in range(M):
                row.append(values[k])
                k += 1
            max_matrix.append(row)

        av_index = tokens.index("AVAILABLE")
        available = []
        for i in range(M):
            available.append(int(tokens[av_index + 1 + i]))

        allocation = []
        for i in range(N):
            row = []
            for j in range(M):
                row.append(0)
            allocation.append(row)

        calculate_need()

    except:
        print("Error: invalid input file format.")
        sys.exit(1)

    print("Input loaded successfully:", N, "processes,", M, "resource types.")


def calculate_need():
    global need

    need = []
    for i in range(N):
        row = []
        for j in range(M):
            row.append(max_matrix[i][j] - allocation[i][j])
        need.append(row)


def print_vector(name, vector):
    print(name + ":")
    for j in range(M):
        print("R" + str(j), end="\t")
    print()

    for j in range(M):
        print(vector[j], end="\t")
    print("\n")


def print_matrix(name, matrix):
    print(name + ":")
    print("Process", end="\t")
    for j in range(M):
        print("R" + str(j), end="\t")
    print()

    for i in range(N):
        print("P" + str(i), end="\t")
        for j in range(M):
            print(matrix[i][j], end="\t")
        print()
    print()


def print_state():
    print("\n================ SYSTEM STATE ================\n")
    print_vector("Available", available)
    print_matrix("Max", max_matrix)
    print_matrix("Allocation", allocation)
    print_matrix("Need", need)
    print("==============================================\n")


def is_safe():
    work = available[:]

    finish = []
    for i in range(N):
        finish.append(False)

    safe_sequence = []

    while len(safe_sequence) < N:
        found = False

        for i in range(N):
            if finish[i] == False:
                can_run = True

                for j in range(M):
                    if need[i][j] > work[j]:
                        can_run = False
                        break

                if can_run == True:
                    for j in range(M):
                        work[j] = work[j] + allocation[i][j]

                    finish[i] = True
                    safe_sequence.append(i)
                    found = True
                    break

        if found == False:
            return False, []

    return True, safe_sequence


def print_safe_sequence(sequence):
    print("Safe sequence:", end=" ")
    for i in range(len(sequence)):
        print("P" + str(sequence[i]), end="")
        if i != len(sequence) - 1:
            print(" -> ", end="")
    print()


def request_resources(pid, request):
    if pid < 0 or pid >= N:
        print("Error: invalid process ID.")
        return

    if len(request) != M:
        print("Error: wrong number of resource values.")
        return

    for j in range(M):
        if request[j] < 0:
            print("Error: resource values cannot be negative.")
            return

    for j in range(M):
        if request[j] > need[pid][j]:
            print("Request denied: request is greater than process need.")
            return

    for j in range(M):
        if request[j] > available[j]:
            print("Request denied: not enough available resources.")
            return

    for j in range(M):
        available[j] = available[j] - request[j]
        allocation[pid][j] = allocation[pid][j] + request[j]
        need[pid][j] = need[pid][j] - request[j]

    safe, sequence = is_safe()

    if safe == True:
        print("Request granted.")
        print_safe_sequence(sequence)
    else:
        for j in range(M):
            available[j] = available[j] + request[j]
            allocation[pid][j] = allocation[pid][j] - request[j]
            need[pid][j] = need[pid][j] + request[j]

        print("Request denied: unsafe state.")


def release_resources(pid, release):
    if pid < 0 or pid >= N:
        print("Error: invalid process ID.")
        return

    if len(release) != M:
        print("Error: wrong number of resource values.")
        return

    for j in range(M):
        if release[j] < 0:
            print("Error: resource values cannot be negative.")
            return

    for j in range(M):
        if release[j] > allocation[pid][j]:
            print("Invalid release: release is greater than allocation.")
            return

    for j in range(M):
        allocation[pid][j] = allocation[pid][j] - release[j]
        available[j] = available[j] + release[j]
        need[pid][j] = need[pid][j] + release[j]

    print("Release successful.")


def run_system():
    safe, sequence = is_safe()

    if safe == False:
        print("No safe sequence exists. System is unsafe.")
        return

    print_safe_sequence(sequence)
    print("\nRunning processes:\n")

    for pid in sequence:
        print("Running P" + str(pid))

        for j in range(M):
            available[j] = available[j] + allocation[pid][j]
            allocation[pid][j] = 0
            need[pid][j] = max_matrix[pid][j]

        print("P" + str(pid) + " finished.")
        print("Available:", available)
        print()

    print("All processes finished.")


def parse_numbers(parts):
    nums = []
    for x in parts:
        nums.append(int(x))
    return nums


def handle_command(line):
    parts = line.split()

    if len(parts) == 0:
        return

    cmd = parts[0].upper()

    if cmd == "*":
        if len(parts) != 1:
            print("Error: * command takes no arguments.")
        else:
            print_state()

    elif cmd == "RQ":
        if len(parts) != M + 2:
            print("Error: use RQ <process_id> r1 r2 ... rm")
            return

        try:
            pid = int(parts[1])
            request = parse_numbers(parts[2:])
            request_resources(pid, request)
        except:
            print("Error: RQ arguments must be integers.")

    elif cmd == "RL":
        if len(parts) != M + 2:
            print("Error: use RL <process_id> r1 r2 ... rm")
            return

        try:
            pid = int(parts[1])
            release = parse_numbers(parts[2:])
            release_resources(pid, release)
        except:
            print("Error: RL arguments must be integers.")

    elif cmd == "RUN":
        if len(parts) != 1:
            print("Error: RUN command takes no arguments.")
        else:
            run_system()

    elif cmd == "EXIT":
        if len(parts) != 1:
            print("Error: EXIT command takes no arguments.")
        else:
            print("Exiting.")
            sys.exit(0)

    else:
        print("Unknown command. Use: RQ, RL, *, RUN, EXIT")


def main():
    if len(sys.argv) == 1:
        filename = "input.txt"
    elif len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        print("Usage: python bankers.py <input_file>")
        sys.exit(1)

    load_input(filename)
    print_state()

    print("Commands:")
    print("RQ <process_id> r1 r2 ... rm")
    print("RL <process_id> r1 r2 ... rm")
    print("*")
    print("RUN")
    print("EXIT")

    while True:
        line = input(">>> ")
        handle_command(line)


main()
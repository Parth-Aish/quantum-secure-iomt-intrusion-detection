import numpy as np

def simulate_bb84(num_qubits=1000, num_trials=100, eve_present=False):
    qber_list = []
    key_agreement_list = []

    for _ in range(num_trials):
        alice_bits = np.random.randint(2, size=num_qubits)
        alice_bases = np.random.randint(2, size=num_qubits)

        bob_bases = np.random.randint(2, size=num_qubits)

        if eve_present:
            eve_bases = np.random.randint(2, size=num_qubits)
            eve_measurements = np.where(alice_bases == eve_bases, alice_bits, np.random.randint(2, size=num_qubits))
            bob_measurements = np.where(bob_bases == eve_bases, eve_measurements, np.random.randint(2, size=num_qubits))
        else:
            bob_measurements = np.where(alice_bases == bob_bases, alice_bits, np.random.randint(2, size=num_qubits))

        matching_bases = (alice_bases == bob_bases)
        if np.sum(matching_bases) == 0:
            continue

        alice_key = alice_bits[matching_bases]
        bob_key = bob_measurements[matching_bases]

        errors = np.sum(alice_key != bob_key)
        qber = errors / len(alice_key)
        qber_list.append(qber)

        if qber < 0.10:
            key_agreement_list.append(1)
        else:
            key_agreement_list.append(0)

    return np.mean(qber_list), np.mean(key_agreement_list)

if __name__ == "__main__":
    print("=== BB84 QKD Simulation ===")

    qber_no_eve, key_no_eve = simulate_bb84(eve_present=False)
    print("\nScenario 1: No Eavesdropper")
    print(f"Average QBER: {qber_no_eve*100:.2f}%")
    print(f"Key Agreement Rate: {key_no_eve*100:.2f}%")

    qber_eve, key_eve = simulate_bb84(eve_present=True)
    print("\nScenario 2: Eavesdropper Present (Eve)")
    print(f"Average QBER: {qber_eve*100:.2f}%")
    print(f"Key Agreement Rate: {key_eve*100:.2f}%")
    print(f"Man-in-the-middle attack detected: {'Yes' if qber_eve > 0.10 else 'No'}")

from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram

def create_deutsch_jozsa_oracle(n, oracle_type='constant'):
    """
    Generates a Deutsch-Jozsa oracle circuit.

    Args:
        n (int): Number of input qubits.
        oracle_type (str): Type of the oracle ('constant' or 'balanced').

    Returns:
        QuantumCircuit: A quantum circuit implementing the oracle.
    """
    oracle = QuantumCircuit(n + 1)
    
    if oracle_type == 'constant':
        # Constant function: Either always 0 (do nothing) or always 1 (apply X gate to output qubit)
        oracle.i(n)  # Identity gate (explicitly doing nothing)
    elif oracle_type == 'balanced':
        # Balanced function: Apply CNOT gates to flip the output qubit for half the inputs
        for qubit in range(n):
            oracle.cx(qubit, n)
    else:
        raise ValueError("Invalid oracle type. Choose 'constant' or 'balanced'.")
    
    return oracle

def deutsch_jozsa_algorithm(n, oracle):
    """
    Constructs and executes the Deutsch-Jozsa algorithm circuit.

    Args:
        n (int): Number of input qubits.
        oracle (QuantumCircuit): Oracle circuit.

    Returns:
        dict: Measurement results.
    """
    # Create a quantum circuit with n input qubits, 1 output qubit, and n classical bits
    dj_circuit = QuantumCircuit(n + 1, n)

    # Step 1: Initialize output qubit in |1⟩ state
    dj_circuit.x(n)

    # Step 2: Apply Hadamard gates to all qubits
    dj_circuit.h(range(n + 1))

    # Step 3: Apply the oracle
    dj_circuit.append(oracle, range(n + 1))

    # Step 4: Apply Hadamard gates to the input qubits again
    dj_circuit.h(range(n))

    # Step 5: Measure the input qubits
    dj_circuit.measure(range(n), range(n))

    # Execute the circuit on a quantum simulator
    simulator = Aer.get_backend('qasm_simulator')
    result = execute(dj_circuit, simulator, shots=1024).result()

    return result.get_counts()

# Define the number of qubits
n = 6

# Create and execute the Deutsch-Jozsa algorithm with a balanced oracle
oracle = create_deutsch_jozsa_oracle(n, oracle_type='balanced')
measurement_results = deutsch_jozsa_algorithm(n, oracle)

# Output the results
print("Measurement results:", measurement_results)
plot_histogram(measurement_results)

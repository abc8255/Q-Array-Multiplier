# Q-Array-Multiplier
This repository contains the different multiplication techniques that I have compared/developed/tested. For more information on each of the different implementations, read their corresponding section and go through the code. In each case, a Python file and a Jupyter notebook are provided. The Quantum Fourier Transform (QFT) and Inverse Quantum Fourier Transform (IQFT) are used heavily throughout the algorithms in this repository, so it is recommended to get at least a rudimentary understanding of these concepts before continuing into the code.

## Repeated Addition
The repeated addition multiplier is fairly self-explanatory. It takes in two inputs, a _multiplier_ and a _multiplicand_ and uses them to generate a _product_. This is accomplished by repeatedly adding the multiplicand to the product register and decrementing the multiplicand until the multiplicand has reached 0. Once this condition is __true__ the resulting product register is measured and output.
### Stages
#### Initialization
In the initialization stage, for our purposes we are encoding the multiplier and multiplicand values into their respective registers using X gates wherever the input bits are "1".

#### Accumulator QFT
The QFT operator applied to the accumulator transforms its representation from the computational basis |k⟩ to the phase basis |j⟩. This is added every iteration of the multiplication before the addition stage.

#### Addition
The evolution stages occur after the accumulator has been placed into the phase domain and are responsible for the addition acting upon the accumulator by the multiplicand, which is repeated each iteration.

#### Accumulator Inverse QFT
Similar to the QFT operator, an IQFT operator is used to change the basis of each qubit of the accumulator from the phase domain back to the computational basis, allowing for the result of the multiplier to be measured into the classical bits. This stage is repeated every iteration after the addition takes place.

#### Decrement
The purpose of this stage is to decrement the multiplier by a constant value of “1” and then check if the multiplier is equal to “0” via a classical measurement. If so, the algorithm stops. If the multiplier is non-zero, another round of the algorithm must be performed. The subtraction circuit is controlled by an ancillary qubit that has been initialized to "1".

## Improved Repeated Addition
The improved repeated addition takes some of the inefficient components of the repeated addition and improves or removes them. Namely, the use of an ancillary qubit and the repeated use of QFT and IQFT are removed. Instead, the operations that relied on the ancillary qubit as a control are set as standard gates that are always active, as the ancillary was always set to 1 in the original algorithm. The additional QFT and IQFT being performed were unnecessary in between stages, as there was no need to interact with the product register outside of the quantum phase domain. Both of these improvements led to fairly significant reductions in depth as the size of the multiplier and multiplicand increased.
### Stages
The stages for the improved repeated addition are almost the same as the normal version, with the aforementioned improvements included.
#### Initialization
In the initialization stage, for our purposes, we are encoding the multiplier and multiplicand values into their respective registers using X gates wherever the input bits are "1".

#### Accumulator QFT
The QFT operator applied to the accumulator transforms its representation from the computational basis |k⟩ to the phase basis |j⟩. This is performed once at the beginning of the algorithm, no longer needing to be repeated each iteration.

#### Addition
The evolution stages occur after the accumulator has been placed into the phase domain and are responsible for the addition acting upon the accumulator by the multiplicand, which is repeated each iteration.

#### Decrement
The purpose of this stage is to decrement the multiplier by a constant value of “1” and then check if the multiplier is equal to “0” via a classical measurement. If so, the algorithm stops. If the multiplier is non-zero, another round of the algorithm must be performed. The subtraction circuit is no longer controlled by an ancillary qubit; instead, it utilizes gates without controls acting directly on the multiplier.

#### Accumulator Inverse QFT
Similar to the QFT operator, an IQFT operator is used to change the basis of each qubit of the accumulator from the phase domain back to the computational basis, allowing for the result of the multiplier to be measured into the classical bits. This is now only performed at the end of the circuit, once all iterations of addition have been completed.

## Quantum Array Multiplier
This algorithm also uses the QFT and IQFT to operate in the quantum phase domain, but in this case the additions are not repeated but rather weighted in a similar way to the classical array multiplier structure. The QFT is performed on the product register, and following this, the multiplier and multiplicand are both used as controls in a network of multiple controlled phase shifts. These phase shifts are generated without regard to the state of the multiplier, as in the two repeated addition implementations, which means that no measurements have to be performed __during__ runtime. When multiplying numbers of at least 5 bits in size, the quantum array multiplier has a much more favorable depth than either the repeated addition or the improved repeated addition algorithms.
### Stages
#### Initialization
In the initialization stage, for our purposes, we are encoding the multiplier and multiplicand values into their respective registers using X gates wherever the input bits are "1".

#### Product QFT
The QFT operator applied to the product register transforms its representation from the computational basis |k⟩ to the phase basis |j⟩.

#### Array Multiplication
A series of weighted additions, each using two controls, one qubit from each of the multiplication operands, using phase shifts to change the state of the product register.

#### Product Inverse QFT
The IQFT operator is used to change the basis of each qubit of the product register from the phase domain back to the computational basis, allowing for the result of the multiplier to be measured into the classical bits.

## Approximate Quantum Array Multiplier
This algorithm is still a work in progress, but it applies research into the use of approximation methods in quantum phase domain operations. In this case, a minimum phase gate size is allowed to be generated. Once a gate is applied that is less than that minimum size, it will not be added to the circuit. While this method does theoretically reduce the overall accuracy of the algorithm, the hope is that a reduction in overall noise from depth and gate count will offset the impact of the approximation, leading to a more accurate and efficient calculation.
### Stages
The stages for the approximate version are the same as the normal version, with the exception of the array multiplication having an additional condition.
#### Initialization
In the initialization stage, for our purposes, we are encoding the multiplier and multiplicand values into their respective registers using X gates wherever the input bits are "1".

#### Product QFT
The QFT operator applied to the product register transforms its representation from the computational basis |k⟩ to the phase basis |j⟩.

#### Array Multiplication
A series of weighted additions, each using two controls, one qubit from each of the multiplication operands, using phase shifts to change the state of the product register If any of the phase shift gates fall below a pre-specified threshold, then the gate will be excluded from the resulting circuit.

#### Product Inverse QFT
The IQFT operator is used to change the basis of each qubit of the product register from the phase domain back to the computational basis, allowing for the result of the multiplier to be measured into the classical bits.

## Known-input Quantum Array Multiplier
There is currently no work put into this method, but if both inputs are known classically when constructing the circuit, then any multiply-controlled phase gate that has a control bit that is going to be "0" can be ignored and not added to the circuit. This method will no longer generate a circuit that is generalizable to any input, which was one of the goals of the previous circuits, but may lead to other findings if produced and simulated. In the case where all bits of both inputs are "1," it should theoretically generate the same circuit as the normal quantum array multiplier.

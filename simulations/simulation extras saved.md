### Developmental py sims

#Antoniou Gyrator Synthetic Inductor

* Antoniou Gyrator Synthetic Inductor
* For Piezo RL Shunt @ ~430 Hz (L ≈ 0.14 H example)
* Nodes: 1 = Input (piezo hot), 0 = GND

.param Rbase=10k
.param Cval=100n   ; Adjust for exact L = (R1*R3*C)/R2

.subckt opamp nonin inv out
  E1 out 0 value={1e6 * (v(nonin) - v(inv))}
.ends

* Opamps (use real models like OPA445 for high-voltage in LTspice)
XU1 3 4 5 opamp
XU2 6 7 8 opamp

* Antoniou Connections
R1 1 3 {Rbase}
R2 4 0 {Rbase}
R3 5 6 {Rbase}
R4 7 1 {Rbase}
C1 8 0 {Cval}
R5 8 6 {Rbase}

* Test circuit
Vin 1 0 AC 1 SIN(0 1 430)
.ac dec 50 10 10k
.tran 0 0.01 0 1u
.probe V(1) I(R1)
.end
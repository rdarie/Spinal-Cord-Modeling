UNITS { 
	(mV) = (millivolt) 
	(mA) = (milliamp) 
} 
NEURON { 
	SUFFIX nap
	USEION na READ ena WRITE ina
	RANGE gbar, ina
}

PARAMETER { 
	gbar = 0.0 	(mho/cm2)
	v ena 		(mV)  
} 
ASSIGNED { 
	ina 		(mA/cm2) 
	hinf 		(1)
	htau 		(ms) 
} 
STATE {
	minf h
}

BREAKPOINT { 
	SOLVE states METHOD cnexp
	ina = gbar * minf * h * ( v - ena ) 
} 

INITIAL { 
	settables(v) 
	h = 0
}

DERIVATIVE states { 
	settables(v) 
	h' = ( hinf - h ) / htau 
}
UNITSOFF
 
PROCEDURE settables(v) {
	minf = 1 / ( 1 + exp( - ( v + 47.1 ) / 3.1 ) )
	hinf = 1 / ( 1 + exp( ( v + 59 ) / 8 ) )
	htau = 1200 / cosh(( v + 59 ) / 16)
}
UNITSON






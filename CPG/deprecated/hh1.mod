COMMENT
 This is the original Hodgkin-Huxley treatment for the set of sodium, 
  potassium, and leakage channels found in the squid giant axon membrane.
  ("A quantitative description of membrane current and its application 
  conduction and excitation in nerve" J.Physiol. (Lond.) 117:500-544 (1952).)
 Membrane voltage is in absolute mV and has been reversed in polarity
  from the original HH convention and shifted to reflect a resting potential
  of -65 mV.
 Initialize this mechanism to steady-state voltage by calling
  rates_gsquid(v) from HOC, then setting m_gsquid=minf_gsquid, etc.
 Remember to set celsius=6.3 (or whatever) in your HOC file.
 See hh1.hoc for an example of a simulation using this model.
 SW Jaslove  6 March, 1992
ENDCOMMENT

UNITS {
(mA) = (milliamp)
(mV) = (millivolt)
(S) = (siemens)
}
 
NEURON {
SUFFIX hh1
USEION na READ ena WRITE ina
USEION k READ ek WRITE ik
NONSPECIFIC_CURRENT il
RANGE gnabar, gkbar, gl, el, gnapbar
GLOBAL minf, mpinf, hinf, hpinf, ninf, htau, hptau, ntau, mtau, mptau
}

PARAMETER {
v (mV)
dt (ms)
gnabar = 0 (S/cm2)
gnapbar = 0 (S/cm2)
ena = 55 (mV)
gkbar = 0 (S/cm2)
ek = -80 (mV)
gl = 0 (S/cm2)
el = 0 (mV)
}
 
STATE {
m mp h hp n
}
 
ASSIGNED {
ina (mA/cm2)
ik (mA/cm2)
il (mA/cm2)
minf mpinf hinf hpinf ninf htau hptau ntau mtau mptau
}
 
BREAKPOINT {
SOLVE states METHOD cnexp
ina = gnapbar * mp * hp * ( v - ena ) + gnabar*m*m*m*h*(v - ena)
ik = gkbar*n*n*n*n*(v - ek)
il = gl*(v - el)
}

	UNITSOFF
INITIAL {
rates(v)
m = minf
mp = mpinf
h = hinf
hp = hpinf
n = ninf
:m = 0
:mp = 0
:h = 0
:hp = 0
:n = 0
}

DERIVATIVE states {
:Computes state variables m, h, and n 
rates(v)
h' = ( hinf - h ) / htau
hp' = ( hpinf - hp ) / hptau
n' = ( ninf - n ) / ntau
m' = (minf - m) / mtau
mp' = (mpinf - mp) / mptau
}
	UNITSON
 
PROCEDURE rates(v) {
	TABLE minf, mpinf, hinf, hpinf, hptau, ninf, htau, ntau  FROM -120 TO 10 WITH 2048
	:"m" sodium activation system
	minf = 1 / (1 + exp(-(v+35)/7.8))

	mtau = 1e-3
	:"h" sodium inactivation system

	hinf = 1 / (1 + exp((v+55)/7))
	htau = 30 / (exp((v+50)/15) + exp(-(v+50)/16))

	:"n" potassium activation system

	ninf = 1 / (1 + exp(-(v+28)/15))
	ntau = 7 / (exp((v+40)/40) + exp(-(v+40)/50))

	mpinf = 1 / ( 1 + exp( - ( v + 47.1 ) / 3.1 ) )

	mptau = 1e-3

	hpinf = 1 / ( 1 + exp( ( v + 59 ) / 8 ) )
	hptau = 1200/ cosh(( v + 59 ) / 16)
}
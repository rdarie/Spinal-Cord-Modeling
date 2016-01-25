:SOMA

TITLE Motor Axon Soma
INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}

NEURON {
	SUFFIX clarke
	NONSPECIFIC_CURRENT ina
	NONSPECIFIC_CURRENT inap
	NONSPECIFIC_CURRENT ikrect
	NONSPECIFIC_CURRENT ikca
	NONSPECIFIC_CURRENT il
	NONSPECIFIC_CURRENT icaN
	NONSPECIFIC_CURRENT icaL
	RANGE  gnabar, gnapbar, gl, ena, ek, el, gkrect, gcaN, gcaL, gcak
	RANGE p_inf, mp_inf, m_inf, h_inf, n_inf, mc_inf, hc_inf
	RANGE tau_p, tau_mp, tau_mp_bar, tau_n_bar, tau_m, tau_h, tau_n, tau_mc, tau_hc
}


UNITS {
	(mA) = (milliamp)
	(mV) = (millivolt)
}

PARAMETER {
	:SOMA PARAMETERS
	gnabar	= 0.05	(mho/cm2)
	gnapbar = 0.0001	(mho/cm2)
	gl	= 0.002 (mho/cm2)
	gkrect = 0.3  (mho/cm2)
	gcaN = 0.05  (mho/cm2)
	gcaL = 0.0001  (mho/cm2)
	gcak = 0.3  (mho/cm2)
	ca0 = 2  
	ena     = 50.0  (mV)
	ek      = -80.0 (mV)
	el	= -70.0 (mV)
	dt              (ms)
	v               (mV)
	amA = 0.4
	amB = 66
	amC = 5
	ampA = 0.01
	ampB = 27
	ampC = 10.2
	bmpA = 0.000250
	bmpB = 34
	bmpC = 10
	bmA = 0.4
	bmB = 32
	bmC = 5
	R=8.314472
	F=96485.34
	tau_mc = 15
	tau_hc = 50
	tau_mp_bar = 1
	tau_n_bar = 5
}

STATE {
	 p mp m h n cai mc hc
}

ASSIGNED {
	ina	 (mA/cm2)
	inap	 (mA/cm2)
	il      (mA/cm2)
	ikrect    (mA/cm2)
	icaN  (mA/cm2)
	icaL  (mA/cm2)
	ikca  (mA/cm2)
	Eca  (mV)
	m_inf
	mp_inf
	mc_inf
	h_inf
	hc_inf
	n_inf
	p_inf
	q10_1
	tau_mp
	tau_m
	tau_h
	tau_p
	tau_n
}

BREAKPOINT {
	SOLVE states METHOD cnexp
	ina = gnabar * m*m*m*h*(v - ena)
	inap = gnapbar * mp*mp*mp * (v - ena)
	ikrect   = gkrect *n*n*n*n*(v - ek)   :stesso ek di sotto
	il   = gl * (v - el)
	Eca = ((1000*R*309.15)/(2*F))*log(ca0/cai)
	icaN = gcaN*mc*mc*hc*(v-Eca)
	icaL = gcaL*p*(v-Eca)
	ikca = gcak*(cai*cai)/(cai*cai+0.014*0.014)*(v-ek)
}

DERIVATIVE states {  
	 : exact Hodgkin-Huxley equations
        evaluate_fct(v)
	m' = (m_inf - m) / tau_m
	mp'= (mp_inf - mp) / tau_mp
	h' = (h_inf - h) / tau_h
	p' = (p_inf - p) / tau_p
	n' = (n_inf - n) / tau_n
	mc' = (mc_inf - mc) / tau_mc
	hc' = (hc_inf - hc) / tau_hc
	cai'= 0.01*(-(icaN+icaL) - 4*cai)
}

UNITSOFF

INITIAL {
	q10_1 = 2.2 ^ ((celsius-20)/ 10 )
	evaluate_fct(v)
	m = m_inf
	mp = mp_inf
	h = h_inf
	p = p_inf
	n = n_inf
	mc=mc_inf
	hc=hc_inf
	cai = 0.0001
}

PROCEDURE evaluate_fct(v(mV)) { LOCAL a,b,v2
	  
	 
	:FAST SODIUM
	:m
	a = alpham(v)
	b = betam(v)
	tau_m = 1 / (a + b)
	m_inf = a / (a + b)
	:h
	tau_h = 30 / (Exp((v+60)/15) + Exp(-(v+60)/16))
	h_inf = 1 / (1 + Exp((v+65)/7))
	: PERSISTENT SODIUM
	:mp
	a = q10_1*vtrap1(v)
	b = q10_1*vtrap2(v)
	tau_mp = tau_mp_bar / (a + b)
	mp_inf = a / (a + b)
	
	:DELAYED RECTIFIER POTASSIUM 
	tau_n = tau_n_bar / (Exp((v+50)/40) + Exp(-(v+50)/50))
	n_inf = 1 / (1 + Exp(-(v+38)/15))

	:CALCIUM DYNAMICS
        :N-type
	mc_inf = 1/(1+Exp(-(v+32)/5))
	hc_inf =  1/(1+Exp((v+50)/5))
	
	:L-type
	tau_p=400
	p_inf=1/(1+Exp(-(v+55.8)/3.7))

}


FUNCTION alpham(x) {
	if (fabs((x+amB)/amC) < 1e-6) {
		alpham = amA*amC
	}else{
		alpham = (amA*(x+amB)) / (1 - Exp(-(x+amB)/amC))
	}
}



FUNCTION betam(x) {
	if (fabs((x+bmB)/bmC) < 1e-6) {
		betam = -bmA*bmC
	}else{
		betam = (bmA*(-(x+bmB))) / (1 - Exp((x+bmB)/bmC))
	}
}

FUNCTION Exp(x) {
	if (x < -100) {
		Exp = 0
	}else{
		Exp = exp(x)
	}
}

FUNCTION vtrap1(x) {
	if (fabs((x+ampB)/ampC) < 1e-6) {
		vtrap1 = ampA*ampC
	}else{
		vtrap1 = (ampA*(x+ampB)) / (1 - Exp(-(x+ampB)/ampC))
	}
}

FUNCTION vtrap2(x) {
	if (fabs((x+bmpB)/bmpC) < 1e-6) {
		vtrap2 = -bmpA*bmpC
	}else{
		vtrap2 = (bmpA*(-(x+bmpB))) / (1 - Exp((x+bmpB)/bmpC))
	}
}
UNITSON

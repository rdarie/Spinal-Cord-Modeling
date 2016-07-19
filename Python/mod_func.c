#include <stdio.h>
#include "hocdec.h"
#define IMPORT extern __declspec(dllimport)
IMPORT int nrnmpi_myid, nrn_nobanner_;

extern void _AMPA_reg();
extern void _AXNODE_reg();
extern void _HH2new_reg();
extern void _INITIAL_reg();
extern void _Kslow_reg();
extern void _MOTONEURON_reg();
extern void _caL13_reg();
extern void _clarke_reg();

modl_reg(){
	//nrn_mswindll_stdio(stdin, stdout, stderr);
    if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
	fprintf(stderr, "Additional mechanisms from files\n");

fprintf(stderr," AMPA.mod");
fprintf(stderr," AXNODE.mod");
fprintf(stderr," HH2new.mod");
fprintf(stderr," INITIAL.mod");
fprintf(stderr," Kslow.mod");
fprintf(stderr," MOTONEURON.mod");
fprintf(stderr," caL13.mod");
fprintf(stderr," clarke.mod");
fprintf(stderr, "\n");
    }
_AMPA_reg();
_AXNODE_reg();
_HH2new_reg();
_INITIAL_reg();
_Kslow_reg();
_MOTONEURON_reg();
_caL13_reg();
_clarke_reg();
}

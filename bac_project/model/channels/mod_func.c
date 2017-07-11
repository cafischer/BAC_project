#include <stdio.h>
#include "hocdec.h"
#define IMPORT extern __declspec(dllimport)
IMPORT int nrnmpi_myid, nrn_nobanner_;

extern void _BK_reg();
extern void _IKM_reg();
extern void _ITGHK_reg();
extern void _NMDA_reg();
extern void _SK_reg();
extern void _SlowCa_reg();
extern void _cad_reg();
extern void _fdsexp2s_reg();
extern void _h_reg();
extern void _hh2_reg();
extern void _izap_reg();
extern void _kca_reg();
extern void _kfast_reg();
extern void _kslow_reg();
extern void _nap_reg();
extern void _nat_reg();
extern void _vecevent_reg();
extern void _xtra_reg();

modl_reg(){
	//nrn_mswindll_stdio(stdin, stdout, stderr);
    if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
	fprintf(stderr, "Additional mechanisms from files\n");

fprintf(stderr," BK.mod");
fprintf(stderr," IKM.mod");
fprintf(stderr," ITGHK.mod");
fprintf(stderr," NMDA.mod");
fprintf(stderr," SK.mod");
fprintf(stderr," SlowCa.mod");
fprintf(stderr," cad.mod");
fprintf(stderr," fdsexp2s.mod");
fprintf(stderr," h.mod");
fprintf(stderr," hh2.mod");
fprintf(stderr," izap.mod");
fprintf(stderr," kca.mod");
fprintf(stderr," kfast.mod");
fprintf(stderr," kslow.mod");
fprintf(stderr," nap.mod");
fprintf(stderr," nat.mod");
fprintf(stderr," vecevent.mod");
fprintf(stderr," xtra.mod");
fprintf(stderr, "\n");
    }
_BK_reg();
_IKM_reg();
_ITGHK_reg();
_NMDA_reg();
_SK_reg();
_SlowCa_reg();
_cad_reg();
_fdsexp2s_reg();
_h_reg();
_hh2_reg();
_izap_reg();
_kca_reg();
_kfast_reg();
_kslow_reg();
_nap_reg();
_nat_reg();
_vecevent_reg();
_xtra_reg();
}

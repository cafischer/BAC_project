#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern void _BK_reg(void);
extern void _Gfluct_reg(void);
extern void _IKM_reg(void);
extern void _IM_reg(void);
extern void _IT_reg(void);
extern void _ITGHK_reg(void);
extern void _SK_reg(void);
extern void _SlowCa_reg(void);
extern void _cad_reg(void);
extern void _cadecay_reg(void);
extern void _epsp_reg(void);
extern void _h_reg(void);
extern void _hh2_reg(void);
extern void _izap_reg(void);
extern void _kca_reg(void);
extern void _kfast_reg(void);
extern void _kslow_reg(void);
extern void _nap_reg(void);
extern void _nat_reg(void);
extern void _vecevent_reg(void);
extern void _xtra_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," BK.mod");
    fprintf(stderr," Gfluct.mod");
    fprintf(stderr," IKM.mod");
    fprintf(stderr," IM.mod");
    fprintf(stderr," IT.mod");
    fprintf(stderr," ITGHK.mod");
    fprintf(stderr," SK.mod");
    fprintf(stderr," SlowCa.mod");
    fprintf(stderr," cad.mod");
    fprintf(stderr," cadecay.mod");
    fprintf(stderr," epsp.mod");
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
  _Gfluct_reg();
  _IKM_reg();
  _IM_reg();
  _IT_reg();
  _ITGHK_reg();
  _SK_reg();
  _SlowCa_reg();
  _cad_reg();
  _cadecay_reg();
  _epsp_reg();
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

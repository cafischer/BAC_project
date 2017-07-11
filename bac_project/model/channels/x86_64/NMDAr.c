/* Created by Language version: 6.2.0 */
/* NOT VECTORIZED */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "scoplib_ansi.h"
#undef PI
#define nil 0
#include "md1redef.h"
#include "section.h"
#include "nrniv_mf.h"
#include "md2redef.h"
 
#if METHOD3
extern int _method3;
#endif

#if !NRNGPU
#undef exp
#define exp hoc_Exp
extern double hoc_Exp(double);
#endif
 
#define _threadargscomma_ /**/
#define _threadargs_ /**/
 
#define _threadargsprotocomma_ /**/
#define _threadargsproto_ /**/
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *getarg();
 static double *_p; static Datum *_ppvar;
 
#define t nrn_threads->_t
#define dt nrn_threads->_dt
#define nchan _p[0]
#define gamma _p[1]
#define del _p[2]
#define dur _p[3]
#define conc _p[4]
#define i _p[5]
#define g _p[6]
#define rb _p[7]
#define mg_on _p[8]
#define mg_off _p[9]
#define C _p[10]
#define state_C0 _p[11]
#define state_C1 _p[12]
#define state_C2 _p[13]
#define state_D _p[14]
#define state_O _p[15]
#define state_B _p[16]
#define state_DB _p[17]
#define state_C2B _p[18]
#define state_C1B _p[19]
#define state_CB _p[20]
#define Dstate_C0 _p[21]
#define Dstate_C1 _p[22]
#define Dstate_C2 _p[23]
#define Dstate_D _p[24]
#define Dstate_O _p[25]
#define Dstate_B _p[26]
#define Dstate_DB _p[27]
#define Dstate_C2B _p[28]
#define Dstate_C1B _p[29]
#define Dstate_CB _p[30]
#define _g _p[31]
#define _tsav _p[32]
#define _nd_area  *_ppvar[0]._pval
 
#if MAC
#if !defined(v)
#define v _mlhv
#endif
#if !defined(h)
#define h _mlhh
#endif
#endif
 
#if defined(__cplusplus)
extern "C" {
#endif
 static int hoc_nrnpointerindex =  -1;
 /* external NEURON variables */
 /* declaration of user functions */
 static double _hoc_rates();
 static double _hoc_transmitter();
 static int _mechtype;
extern void _nrn_cacheloop_reg(int, int);
extern void hoc_register_prop_size(int, int, int);
extern void hoc_register_limits(int, HocParmLimits*);
extern void hoc_register_units(int, HocParmUnits*);
extern void nrn_promote(Prop*, int, int);
extern Memb_func* memb_func;
 extern Prop* nrn_point_prop_;
 static int _pointtype;
 static void* _hoc_create_pnt(_ho) Object* _ho; { void* create_point_process();
 return create_point_process(_pointtype, _ho);
}
 static void _hoc_destroy_pnt();
 static double _hoc_loc_pnt(_vptr) void* _vptr; {double loc_point_process();
 return loc_point_process(_pointtype, _vptr);
}
 static double _hoc_has_loc(_vptr) void* _vptr; {double has_loc_point();
 return has_loc_point(_vptr);
}
 static double _hoc_get_loc_pnt(_vptr)void* _vptr; {
 double get_loc_point_process(); return (get_loc_point_process(_vptr));
}
 extern void _nrn_setdata_reg(int, void(*)(Prop*));
 static void _setdata(Prop* _prop) {
 _p = _prop->param; _ppvar = _prop->dparam;
 }
 static void _hoc_setdata(void* _vptr) { Prop* _prop;
 _prop = ((Point_process*)_vptr)->_prop;
   _setdata(_prop);
 }
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 0,0
};
 static Member_func _member_func[] = {
 "loc", _hoc_loc_pnt,
 "has_loc", _hoc_has_loc,
 "get_loc", _hoc_get_loc_pnt,
 "rates", _hoc_rates,
 "transmitter", _hoc_transmitter,
 0, 0
};
 /* declare global and static user variables */
#define Erev Erev_NMDA
 double Erev = -3;
#define alpha_mg alpha_mg_NMDA
 double alpha_mg = 0.229;
#define alpha alpha_NMDA
 double alpha = 0.0916;
#define beta_mg beta_mg_NMDA
 double beta_mg = 0.04185;
#define beta beta_NMDA
 double beta = 0.0465;
#define kd_mg kd_mg_NMDA
 double kd_mg = 0.0084;
#define kr_mg kr_mg_NMDA
 double kr_mg = 0.0018;
#define kon_mg kon_mg_NMDA
 double kon_mg = 0.005;
#define koff_mg koff_mg_NMDA
 double koff_mg = 0.082;
#define kr kr_NMDA
 double kr = 0.0018;
#define kd kd_NMDA
 double kd = 0.0084;
#define koff koff_NMDA
 double koff = 0.082;
#define kon kon_NMDA
 double kon = 0.005;
#define mg mg_NMDA
 double mg = 1;
#define normfactor normfactor_NMDA
 double normfactor = 0.0694817;
#define rb_mg rb_mg_NMDA
 double rb_mg = 0;
#define vmax vmax_NMDA
 double vmax = 100;
#define vmin vmin_NMDA
 double vmin = -180;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "Erev_NMDA", "mV",
 "mg_NMDA", "mM",
 "vmin_NMDA", "mV",
 "vmax_NMDA", "mV",
 "kon_NMDA", "/uM",
 "koff_NMDA", "/ms",
 "beta_NMDA", "/ms",
 "alpha_NMDA", "/ms",
 "kr_NMDA", "/ms",
 "kd_NMDA", "/ms",
 "kon_mg_NMDA", "/uM",
 "koff_mg_NMDA", "/ms",
 "beta_mg_NMDA", "/ms",
 "alpha_mg_NMDA", "/ms",
 "kr_mg_NMDA", "/ms",
 "kd_mg_NMDA", "/ms",
 "rb_mg_NMDA", "/ms",
 "gamma", "uS",
 "del", "ms",
 "dur", "ms",
 "conc", "uM",
 "i", "nA",
 "g", "uS",
 "rb", "/ms",
 "mg_on", "/mM /ms",
 "mg_off", "/ms",
 "C", "uM",
 0,0
};
 static double delta_t = 1;
 static double state_CB0 = 0;
 static double state_C1B0 = 0;
 static double state_C2B0 = 0;
 static double state_DB0 = 0;
 static double state_B0 = 0;
 static double state_O0 = 0;
 static double state_D0 = 0;
 static double state_C20 = 0;
 static double state_C10 = 0;
 static double state_C00 = 0;
 static double v = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "Erev_NMDA", &Erev_NMDA,
 "mg_NMDA", &mg_NMDA,
 "vmin_NMDA", &vmin_NMDA,
 "vmax_NMDA", &vmax_NMDA,
 "normfactor_NMDA", &normfactor_NMDA,
 "kon_NMDA", &kon_NMDA,
 "koff_NMDA", &koff_NMDA,
 "beta_NMDA", &beta_NMDA,
 "alpha_NMDA", &alpha_NMDA,
 "kr_NMDA", &kr_NMDA,
 "kd_NMDA", &kd_NMDA,
 "kon_mg_NMDA", &kon_mg_NMDA,
 "koff_mg_NMDA", &koff_mg_NMDA,
 "beta_mg_NMDA", &beta_mg_NMDA,
 "alpha_mg_NMDA", &alpha_mg_NMDA,
 "kr_mg_NMDA", &kr_mg_NMDA,
 "kd_mg_NMDA", &kd_mg_NMDA,
 "rb_mg_NMDA", &rb_mg_NMDA,
 0,0
};
 static DoubVec hoc_vdoub[] = {
 0,0,0
};
 static double _sav_indep;
 static void nrn_alloc(Prop*);
static void  nrn_init(_NrnThread*, _Memb_list*, int);
static void nrn_state(_NrnThread*, _Memb_list*, int);
 static void nrn_cur(_NrnThread*, _Memb_list*, int);
static void  nrn_jacob(_NrnThread*, _Memb_list*, int);
 static void _hoc_destroy_pnt(_vptr) void* _vptr; {
   destroy_point_process(_vptr);
}
 
static int _ode_count(int);
static void _ode_map(int, double**, double**, double*, Datum*, double*, int);
static void _ode_spec(_NrnThread*, _Memb_list*, int);
static void _ode_matsol(_NrnThread*, _Memb_list*, int);
 
#define _cvode_ieq _ppvar[2]._i
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "6.2.0",
"NMDA",
 "nchan",
 "gamma",
 "del",
 "dur",
 "conc",
 0,
 "i",
 "g",
 "rb",
 "mg_on",
 "mg_off",
 "C",
 0,
 "state_C0",
 "state_C1",
 "state_C2",
 "state_D",
 "state_O",
 "state_B",
 "state_DB",
 "state_C2B",
 "state_C1B",
 "state_CB",
 0,
 0};
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
  if (nrn_point_prop_) {
	_prop->_alloc_seq = nrn_point_prop_->_alloc_seq;
	_p = nrn_point_prop_->param;
	_ppvar = nrn_point_prop_->dparam;
 }else{
 	_p = nrn_prop_data_alloc(_mechtype, 33, _prop);
 	/*initialize range parameters*/
 	nchan = 10;
 	gamma = 5e-05;
 	del = 100;
 	dur = 10;
 	conc = 0;
  }
 	_prop->param = _p;
 	_prop->param_size = 33;
  if (!nrn_point_prop_) {
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 3, _prop);
  }
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 
}
 static void _initlists();
  /* some states have an absolute tolerance */
 static Symbol** _atollist;
 static HocStateTolerance _hoc_state_tol[] = {
 0,0
};
 static void _net_receive(Point_process*, double*, double);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*f)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, _NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _NMDAr_reg() {
	int _vectorized = 0;
  _initlists();
 	_pointtype = point_register_mech(_mechanism,
	 nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init,
	 hoc_nrnpointerindex, 0,
	 _hoc_create_pnt, _hoc_destroy_pnt, _member_func);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
  hoc_register_dparam_size(_mechtype, 3);
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 pnt_receive[_mechtype] = _net_receive;
 pnt_receive_size[_mechtype] = 1;
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 NMDA /home/ubuntu/Dropbox/NEURON/Python/oscillatory_inhibition/channels/x86_64/NMDAr.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
static int _reset;
static char *modelname = "Asymmetric trapping block model of NMDA receptors";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int rates(double);
static int transmitter();
 
#define _MATELM1(_row,_col)	*(_getelm(_row + 1, _col + 1))
 
#define _RHS1(_arg) _coef1[_arg + 1]
 static double *_coef1;
 static void* _cvsparseobj1;
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 extern double *_getelm();
 
#define _MATELM1(_row,_col)	*(_getelm(_row + 1, _col + 1))
 
#define _RHS1(_arg) _coef1[_arg + 1]
 static double *_coef1;
 
#define _linmat1  1
 static void* _sparseobj1;
 static int _slist1[10], _dlist1[10]; static double *_temp1;
 static int kstates();
 
static int kstates ()
 {_reset=0;
 {
   double b_flux, f_flux, _term; int _i;
 {int _i; double _dt1 = 1.0/dt;
for(_i=1;_i<10;_i++){
  	_RHS1(_i) = -_dt1*(_p[_slist1[_i]] - _p[_dlist1[_i]]);
	_MATELM1(_i, _i) = _dt1;
      
} }
 rates ( _threadargscomma_ v ) ;
   rb = kon * C ;
   rb_mg = kon_mg * C ;
   /* ~ state_C0 <-> state_C1 ( 2.0 * rb , koff )*/
 f_flux =  2.0 * rb * state_C0 ;
 b_flux =  koff * state_C1 ;
 _RHS1( 9) -= (f_flux - b_flux);
 _RHS1( 8) += (f_flux - b_flux);
 
 _term =  2.0 * rb ;
 _MATELM1( 9 ,9)  += _term;
 _MATELM1( 8 ,9)  -= _term;
 _term =  koff ;
 _MATELM1( 9 ,8)  -= _term;
 _MATELM1( 8 ,8)  += _term;
 /*REACTION*/
  /* ~ state_C1 <-> state_C2 ( rb , 2.0 * koff )*/
 f_flux =  rb * state_C1 ;
 b_flux =  2.0 * koff * state_C2 ;
 _RHS1( 8) -= (f_flux - b_flux);
 _RHS1( 7) += (f_flux - b_flux);
 
 _term =  rb ;
 _MATELM1( 8 ,8)  += _term;
 _MATELM1( 7 ,8)  -= _term;
 _term =  2.0 * koff ;
 _MATELM1( 8 ,7)  -= _term;
 _MATELM1( 7 ,7)  += _term;
 /*REACTION*/
  /* ~ state_C2 <-> state_D ( kd , kr )*/
 f_flux =  kd * state_C2 ;
 b_flux =  kr * state_D ;
 _RHS1( 7) -= (f_flux - b_flux);
 _RHS1( 6) += (f_flux - b_flux);
 
 _term =  kd ;
 _MATELM1( 7 ,7)  += _term;
 _MATELM1( 6 ,7)  -= _term;
 _term =  kr ;
 _MATELM1( 7 ,6)  -= _term;
 _MATELM1( 6 ,6)  += _term;
 /*REACTION*/
  /* ~ state_C2 <-> state_O ( beta , alpha )*/
 f_flux =  beta * state_C2 ;
 b_flux =  alpha * state_O ;
 _RHS1( 7) -= (f_flux - b_flux);
 _RHS1( 5) += (f_flux - b_flux);
 
 _term =  beta ;
 _MATELM1( 7 ,7)  += _term;
 _MATELM1( 5 ,7)  -= _term;
 _term =  alpha ;
 _MATELM1( 7 ,5)  -= _term;
 _MATELM1( 5 ,5)  += _term;
 /*REACTION*/
  /* ~ state_O <-> state_B ( mg_on , mg_off )*/
 f_flux =  mg_on * state_O ;
 b_flux =  mg_off * state_B ;
 _RHS1( 5) -= (f_flux - b_flux);
 _RHS1( 4) += (f_flux - b_flux);
 
 _term =  mg_on ;
 _MATELM1( 5 ,5)  += _term;
 _MATELM1( 4 ,5)  -= _term;
 _term =  mg_off ;
 _MATELM1( 5 ,4)  -= _term;
 _MATELM1( 4 ,4)  += _term;
 /*REACTION*/
  /* ~ state_C2B <-> state_DB ( kd_mg , kr_mg )*/
 f_flux =  kd_mg * state_C2B ;
 b_flux =  kr_mg * state_DB ;
 _RHS1( 2) -= (f_flux - b_flux);
 _RHS1( 3) += (f_flux - b_flux);
 
 _term =  kd_mg ;
 _MATELM1( 2 ,2)  += _term;
 _MATELM1( 3 ,2)  -= _term;
 _term =  kr_mg ;
 _MATELM1( 2 ,3)  -= _term;
 _MATELM1( 3 ,3)  += _term;
 /*REACTION*/
  /* ~ state_B <-> state_C2B ( alpha_mg , beta_mg )*/
 f_flux =  alpha_mg * state_B ;
 b_flux =  beta_mg * state_C2B ;
 _RHS1( 4) -= (f_flux - b_flux);
 _RHS1( 2) += (f_flux - b_flux);
 
 _term =  alpha_mg ;
 _MATELM1( 4 ,4)  += _term;
 _MATELM1( 2 ,4)  -= _term;
 _term =  beta_mg ;
 _MATELM1( 4 ,2)  -= _term;
 _MATELM1( 2 ,2)  += _term;
 /*REACTION*/
  /* ~ state_C2B <-> state_C1B ( 2.0 * koff_mg , rb_mg )*/
 f_flux =  2.0 * koff_mg * state_C2B ;
 b_flux =  rb_mg * state_C1B ;
 _RHS1( 2) -= (f_flux - b_flux);
 _RHS1( 1) += (f_flux - b_flux);
 
 _term =  2.0 * koff_mg ;
 _MATELM1( 2 ,2)  += _term;
 _MATELM1( 1 ,2)  -= _term;
 _term =  rb_mg ;
 _MATELM1( 2 ,1)  -= _term;
 _MATELM1( 1 ,1)  += _term;
 /*REACTION*/
  /* ~ state_C1B <-> state_CB ( koff_mg , 2.0 * rb_mg )*/
 f_flux =  koff_mg * state_C1B ;
 b_flux =  2.0 * rb_mg * state_CB ;
 _RHS1( 1) -= (f_flux - b_flux);
 
 _term =  koff_mg ;
 _MATELM1( 1 ,1)  += _term;
 _term =  2.0 * rb_mg ;
 _MATELM1( 1 ,0)  -= _term;
 /*REACTION*/
   /* state_C0 + state_C1 + state_C2 + state_D + state_O + state_B + state_DB + state_C2B + state_C1B + state_CB = 1.0 */
 _RHS1(0) =  1.0;
 _MATELM1(0, 0) = 1;
 _RHS1(0) -= state_CB ;
 _MATELM1(0, 1) = 1;
 _RHS1(0) -= state_C1B ;
 _MATELM1(0, 2) = 1;
 _RHS1(0) -= state_C2B ;
 _MATELM1(0, 3) = 1;
 _RHS1(0) -= state_DB ;
 _MATELM1(0, 4) = 1;
 _RHS1(0) -= state_B ;
 _MATELM1(0, 5) = 1;
 _RHS1(0) -= state_O ;
 _MATELM1(0, 6) = 1;
 _RHS1(0) -= state_D ;
 _MATELM1(0, 7) = 1;
 _RHS1(0) -= state_C2 ;
 _MATELM1(0, 8) = 1;
 _RHS1(0) -= state_C1 ;
 _MATELM1(0, 9) = 1;
 _RHS1(0) -= state_C0 ;
 /*CONSERVATION*/
   } return _reset;
 }
 
static int  rates (  double _lv ) {
   mg_on = 610.0 * exp ( - _lv / 17.0 ) * ( 1.0 / 1000.0 ) ;
   mg_off = 5.4 * exp ( _lv / 47.0 ) ;
    return 0; }
 
static double _hoc_rates(void* _vptr) {
 double _r;
    _hoc_setdata(_vptr);
 _r = 1.;
 rates (  *getarg(1) );
 return(_r);
}
 
static void _net_receive (_pnt, _args, _lflag) Point_process* _pnt; double* _args; double _lflag; 
{    _p = _pnt->_prop->param; _ppvar = _pnt->_prop->dparam;
  if (_tsav > t){ extern char* hoc_object_name(); hoc_execerror(hoc_object_name(_pnt->ob), ":Event arrived out of order. Must call ParallelContext.set_maxstep AFTER assigning minimum NetCon.delay");}
 _tsav = t; {
   del = t ;
   conc = _args[0] ;
   } }
 
static int  transmitter (  ) {
   if ( ( conc  != 0.0 )  && ( t >= del )  && ( t <= del + dur ) ) {
     C = conc ;
     }
   else {
     C = 0.0 ;
     conc = 0.0 ;
     }
    return 0; }
 
static double _hoc_transmitter(void* _vptr) {
 double _r;
    _hoc_setdata(_vptr);
 _r = 1.;
 transmitter (  );
 return(_r);
}
 
/*CVODE ode begin*/
 static int _ode_spec1() {_reset=0;{
 double b_flux, f_flux, _term; int _i;
 {int _i; for(_i=0;_i<10;_i++) _p[_dlist1[_i]] = 0.0;}
 rates ( _threadargscomma_ v ) ;
 rb = kon * C ;
 rb_mg = kon_mg * C ;
 /* ~ state_C0 <-> state_C1 ( 2.0 * rb , koff )*/
 f_flux =  2.0 * rb * state_C0 ;
 b_flux =  koff * state_C1 ;
 Dstate_C0 -= (f_flux - b_flux);
 Dstate_C1 += (f_flux - b_flux);
 
 /*REACTION*/
  /* ~ state_C1 <-> state_C2 ( rb , 2.0 * koff )*/
 f_flux =  rb * state_C1 ;
 b_flux =  2.0 * koff * state_C2 ;
 Dstate_C1 -= (f_flux - b_flux);
 Dstate_C2 += (f_flux - b_flux);
 
 /*REACTION*/
  /* ~ state_C2 <-> state_D ( kd , kr )*/
 f_flux =  kd * state_C2 ;
 b_flux =  kr * state_D ;
 Dstate_C2 -= (f_flux - b_flux);
 Dstate_D += (f_flux - b_flux);
 
 /*REACTION*/
  /* ~ state_C2 <-> state_O ( beta , alpha )*/
 f_flux =  beta * state_C2 ;
 b_flux =  alpha * state_O ;
 Dstate_C2 -= (f_flux - b_flux);
 Dstate_O += (f_flux - b_flux);
 
 /*REACTION*/
  /* ~ state_O <-> state_B ( mg_on , mg_off )*/
 f_flux =  mg_on * state_O ;
 b_flux =  mg_off * state_B ;
 Dstate_O -= (f_flux - b_flux);
 Dstate_B += (f_flux - b_flux);
 
 /*REACTION*/
  /* ~ state_C2B <-> state_DB ( kd_mg , kr_mg )*/
 f_flux =  kd_mg * state_C2B ;
 b_flux =  kr_mg * state_DB ;
 Dstate_C2B -= (f_flux - b_flux);
 Dstate_DB += (f_flux - b_flux);
 
 /*REACTION*/
  /* ~ state_B <-> state_C2B ( alpha_mg , beta_mg )*/
 f_flux =  alpha_mg * state_B ;
 b_flux =  beta_mg * state_C2B ;
 Dstate_B -= (f_flux - b_flux);
 Dstate_C2B += (f_flux - b_flux);
 
 /*REACTION*/
  /* ~ state_C2B <-> state_C1B ( 2.0 * koff_mg , rb_mg )*/
 f_flux =  2.0 * koff_mg * state_C2B ;
 b_flux =  rb_mg * state_C1B ;
 Dstate_C2B -= (f_flux - b_flux);
 Dstate_C1B += (f_flux - b_flux);
 
 /*REACTION*/
  /* ~ state_C1B <-> state_CB ( koff_mg , 2.0 * rb_mg )*/
 f_flux =  koff_mg * state_C1B ;
 b_flux =  2.0 * rb_mg * state_CB ;
 Dstate_C1B -= (f_flux - b_flux);
 Dstate_CB += (f_flux - b_flux);
 
 /*REACTION*/
   /* state_C0 + state_C1 + state_C2 + state_D + state_O + state_B + state_DB + state_C2B + state_C1B + state_CB = 1.0 */
 /*CONSERVATION*/
   } return _reset;
 }
 
/*CVODE matsol*/
 static int _ode_matsol1() {_reset=0;{
 double b_flux, f_flux, _term; int _i;
   b_flux = f_flux = 0.;
 {int _i; double _dt1 = 1.0/dt;
for(_i=0;_i<10;_i++){
  	_RHS1(_i) = _dt1*(_p[_dlist1[_i]]);
	_MATELM1(_i, _i) = _dt1;
      
} }
 rates ( _threadargscomma_ v ) ;
 rb = kon * C ;
 rb_mg = kon_mg * C ;
 /* ~ state_C0 <-> state_C1 ( 2.0 * rb , koff )*/
 _term =  2.0 * rb ;
 _MATELM1( 9 ,9)  += _term;
 _MATELM1( 8 ,9)  -= _term;
 _term =  koff ;
 _MATELM1( 9 ,8)  -= _term;
 _MATELM1( 8 ,8)  += _term;
 /*REACTION*/
  /* ~ state_C1 <-> state_C2 ( rb , 2.0 * koff )*/
 _term =  rb ;
 _MATELM1( 8 ,8)  += _term;
 _MATELM1( 7 ,8)  -= _term;
 _term =  2.0 * koff ;
 _MATELM1( 8 ,7)  -= _term;
 _MATELM1( 7 ,7)  += _term;
 /*REACTION*/
  /* ~ state_C2 <-> state_D ( kd , kr )*/
 _term =  kd ;
 _MATELM1( 7 ,7)  += _term;
 _MATELM1( 6 ,7)  -= _term;
 _term =  kr ;
 _MATELM1( 7 ,6)  -= _term;
 _MATELM1( 6 ,6)  += _term;
 /*REACTION*/
  /* ~ state_C2 <-> state_O ( beta , alpha )*/
 _term =  beta ;
 _MATELM1( 7 ,7)  += _term;
 _MATELM1( 5 ,7)  -= _term;
 _term =  alpha ;
 _MATELM1( 7 ,5)  -= _term;
 _MATELM1( 5 ,5)  += _term;
 /*REACTION*/
  /* ~ state_O <-> state_B ( mg_on , mg_off )*/
 _term =  mg_on ;
 _MATELM1( 5 ,5)  += _term;
 _MATELM1( 4 ,5)  -= _term;
 _term =  mg_off ;
 _MATELM1( 5 ,4)  -= _term;
 _MATELM1( 4 ,4)  += _term;
 /*REACTION*/
  /* ~ state_C2B <-> state_DB ( kd_mg , kr_mg )*/
 _term =  kd_mg ;
 _MATELM1( 2 ,2)  += _term;
 _MATELM1( 3 ,2)  -= _term;
 _term =  kr_mg ;
 _MATELM1( 2 ,3)  -= _term;
 _MATELM1( 3 ,3)  += _term;
 /*REACTION*/
  /* ~ state_B <-> state_C2B ( alpha_mg , beta_mg )*/
 _term =  alpha_mg ;
 _MATELM1( 4 ,4)  += _term;
 _MATELM1( 2 ,4)  -= _term;
 _term =  beta_mg ;
 _MATELM1( 4 ,2)  -= _term;
 _MATELM1( 2 ,2)  += _term;
 /*REACTION*/
  /* ~ state_C2B <-> state_C1B ( 2.0 * koff_mg , rb_mg )*/
 _term =  2.0 * koff_mg ;
 _MATELM1( 2 ,2)  += _term;
 _MATELM1( 1 ,2)  -= _term;
 _term =  rb_mg ;
 _MATELM1( 2 ,1)  -= _term;
 _MATELM1( 1 ,1)  += _term;
 /*REACTION*/
  /* ~ state_C1B <-> state_CB ( koff_mg , 2.0 * rb_mg )*/
 _term =  koff_mg ;
 _MATELM1( 1 ,1)  += _term;
 _MATELM1( 0 ,1)  -= _term;
 _term =  2.0 * rb_mg ;
 _MATELM1( 1 ,0)  -= _term;
 _MATELM1( 0 ,0)  += _term;
 /*REACTION*/
   /* state_C0 + state_C1 + state_C2 + state_D + state_O + state_B + state_DB + state_C2B + state_C1B + state_CB = 1.0 */
 /*CONSERVATION*/
   } return _reset;
 }
 
/*CVODE end*/
 
static int _ode_count(int _type){ return 10;}
 
static void _ode_spec(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
     _ode_spec1 ();
 }}
 
static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) { 
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 10; ++_i) {
		_pv[_i] = _pp + _slist1[_i];  _pvdot[_i] = _pp + _dlist1[_i];
		_cvode_abstol(_atollist, _atol, _i);
	}
 }
 
static void _ode_matsol(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
 _cvode_sparse(&_cvsparseobj1, 10, _dlist1, _p, _ode_matsol1, &_coef1);
 }}

static void initmodel() {
  int _i; double _save;_ninits++;
 _save = t;
 t = 0.0;
{
  state_CB = state_CB0;
  state_C1B = state_C1B0;
  state_C2B = state_C2B0;
  state_DB = state_DB0;
  state_B = state_B0;
  state_O = state_O0;
  state_D = state_D0;
  state_C2 = state_C20;
  state_C1 = state_C10;
  state_C0 = state_C00;
 {
   error = _ss_sparse(&_sparseobj1, 10, _slist1, _dlist1, _p, &t, dt, kstates,&_coef1, _linmat1);
 if(error){fprintf(stderr,"at line 125 in file NMDAr.mod:\nSOLVE kstates STEADYSTATE sparse\n"); nrn_complain(_p); abort_run(error);}
 }
  _sav_indep = t; t = _save;

}
}

static void nrn_init(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
 _tsav = -1e20;
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v = _v;
 initmodel();
}}

static double _nrn_current(double _v){double _current=0.;v=_v;{ {
   transmitter ( _threadargs_ ) ;
   g = nchan * state_O * gamma ;
   i = g * ( v - Erev ) ;
   }
 _current += i;

} return _current;
}

static void nrn_cur(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; int* _ni; double _rhs, _v; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 _g = _nrn_current(_v + .001);
 	{ _rhs = _nrn_current(_v);
 	}
 _g = (_g - _rhs)/.001;
 _g *=  1.e2/(_nd_area);
 _rhs *= 1.e2/(_nd_area);
#if CACHEVEC
  if (use_cachevec) {
	VEC_RHS(_ni[_iml]) -= _rhs;
  }else
#endif
  {
	NODERHS(_nd) -= _rhs;
  }
 
}}

static void nrn_jacob(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml];
#if CACHEVEC
  if (use_cachevec) {
	VEC_D(_ni[_iml]) += _g;
  }else
#endif
  {
     _nd = _ml->_nodelist[_iml];
	NODED(_nd) += _g;
  }
 
}}

static void nrn_state(_NrnThread* _nt, _Memb_list* _ml, int _type){
 double _break, _save;
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
 _nd = _ml->_nodelist[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 _break = t + .5*dt; _save = t;
 v=_v;
{
 { {
 for (; t < _break; t += dt) {
 error = sparse(&_sparseobj1, 10, _slist1, _dlist1, _p, &t, dt, kstates,&_coef1, _linmat1);
 if(error){fprintf(stderr,"at line 131 in file NMDAr.mod:\n\n"); nrn_complain(_p); abort_run(error);}
 
}}
 t = _save;
 }}}

}

static void terminal(){}

static void _initlists() {
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = &(state_CB) - _p;  _dlist1[0] = &(Dstate_CB) - _p;
 _slist1[1] = &(state_C1B) - _p;  _dlist1[1] = &(Dstate_C1B) - _p;
 _slist1[2] = &(state_C2B) - _p;  _dlist1[2] = &(Dstate_C2B) - _p;
 _slist1[3] = &(state_DB) - _p;  _dlist1[3] = &(Dstate_DB) - _p;
 _slist1[4] = &(state_B) - _p;  _dlist1[4] = &(Dstate_B) - _p;
 _slist1[5] = &(state_O) - _p;  _dlist1[5] = &(Dstate_O) - _p;
 _slist1[6] = &(state_D) - _p;  _dlist1[6] = &(Dstate_D) - _p;
 _slist1[7] = &(state_C2) - _p;  _dlist1[7] = &(Dstate_C2) - _p;
 _slist1[8] = &(state_C1) - _p;  _dlist1[8] = &(Dstate_C1) - _p;
 _slist1[9] = &(state_C0) - _p;  _dlist1[9] = &(Dstate_C0) - _p;
_first = 0;
}

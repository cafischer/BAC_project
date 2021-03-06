: $Id: izap.mod,v 1.3 2010/06/22 06:40:59 ted Exp $

COMMENT
izap.mod

delivers an oscillating current that starts at t = delay >= 0.
The frequency of the oscillation increases linearly with time
from f0 at t == delay to f1 at t == delay + dur, 
where both delay and dur are > 0.

ENDCOMMENT

NEURON {
  POINT_PROCESS Izap
  RANGE delay, dur, f0, f1, amp, f, i, std
  ELECTRODE_CURRENT i
}

UNITS {
  (nA) = (nanoamp)
  PI = (pi) (1)
}

PARAMETER {
  delay = 0 (ms)
  dur = 100 (ms)
  f0 = 0 (1/s)  : frequency is in Hz
  f1 = 0 (1/s)
  amp = 0.05 (nA)
  std = 0 (nA)
}

ASSIGNED {
  f (1/s)
  i_tmp (nA)
  i (nA)
  on (1)
  noise (nA)
}

INITIAL {
  f = 0
  i_tmp = 0
  i = 0
  on = 0
  noise = 0

  if (delay<0) { delay=0 }
  if (dur<0) { dur=0 }
  if (f0<=0) { f0=0 (1/s) }
  if (f1<=0) { f1=0 (1/s) }

  : do nothing if dur == 0
  if (dur>0) {
    net_send(delay, 1)  : to turn it on and start frequency ramp
  }
}

COMMENT
The angular velocity in radians/sec is w = 2*PI*f, 
where f is the instantaneous frequency in Hz.

Assume for the moment that the frequency ramp starts at t = 0.
f = f0 + (f1 - f0)*t/dur

Then the angular displacement is
theta = 2*PI * ( f0*t + (f1 - f0)*(t^2)/(2*dur) ) 
      = 2*PI * t * (f0 + (f1 - f0)*t/(2*dur))
But the ramp starts at t = delay, so just substitute t-delay for every occurrence of t
in the formula for theta.
ENDCOMMENT

BEFORE BREAKPOINT {
  if (on==0) {
    f = 0
    i = 0
  } else {
    f = f0 + (f1 - f0)*(t-delay)/dur
    if (f0==0 && f1==0) {
      i_tmp = amp
    } else {
      i_tmp = amp * sin( 2*PI * (t-delay) * (f0 + (f1 - f0)*(t-delay)/(2*dur)) * (0.001) )
    }
    noise = normrand(0,std*1(/nA))*1(nA)
    i_tmp = i_tmp + noise
  }
}

BREAKPOINT {
  i = i_tmp
}

NET_RECEIVE (w) {
  : respond only to self-events with flag > 0
  if (flag == 1) {
    if (on==0) {
      on = 1  : turn it on
      net_send(t+dur, 1)  : to stop frequency ramp, freezing frequency at f1
    } else {
      on = 0  : turn it off
    }
  }
}

#ifndef KB_H
#define KB_H

#include "quantum.h"

#define KEYMAP( \
	K00, K01, K02, K03, K04, K05, K06, \
	K10,      K12, K13, K14, K15, K16, \
	K20,      K22, K23, K24, K25, K26, \
	K30,      K32, K33, K34, K35, K36, \
	K40, K41,      K43,      K45, K46  \
) { \
	{ K00,   K01,   K02,   K03,   K04,   K05,   K06 }, \
	{ K10,   KC_NO, K12,   K13,   K14,   K15,   K16 }, \
	{ K20,   KC_NO, K22,   K23,   K24,   K25,   K26 }, \
	{ K30,   KC_NO, K32,   K33,   K34,   K35,   K36 }, \
	{ K40,   K41,   KC_NO, K43,   KC_NO, K45,   K46 }  \
}

#endif
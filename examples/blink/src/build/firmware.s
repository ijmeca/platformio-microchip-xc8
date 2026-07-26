subtitle "Microchip MPLAB XC8 C Compiler v3.10 (Free license) build 20250813170317 Og1 "

pagewidth 120

	opt flic

	processor	12F675
include "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/12f675.cgen.inc"
getbyte	macro	val,pos
	(((val) >> (8 * pos)) and 0xff)
endm
byte0	macro	val
	(getbyte(val,0))
endm
byte1	macro	val
	(getbyte(val,1))
endm
byte2	macro	val
	(getbyte(val,2))
endm
byte3	macro	val
	(getbyte(val,3))
endm
byte4	macro	val
	(getbyte(val,4))
endm
byte5	macro	val
	(getbyte(val,5))
endm
byte6	macro	val
	(getbyte(val,6))
endm
byte7	macro	val
	(getbyte(val,7))
endm
getword	macro	val,pos
	(((val) >> (8 * pos)) and 0xffff)
endm
word0	macro	val
	(getword(val,0))
endm
word1	macro	val
	(getword(val,2))
endm
word2	macro	val
	(getword(val,4))
endm
word3	macro	val
	(getword(val,6))
endm
gettword	macro	val,pos
	(((val) >> (8 * pos)) and 0xffffff)
endm
tword0	macro	val
	(gettword(val,0))
endm
tword1	macro	val
	(gettword(val,3))
endm
tword2	macro	val
	(gettword(val,6))
endm
getdword	macro	val,pos
	(((val) >> (8 * pos)) and 0xffffffff)
endm
dword0	macro	val
	(getdword(val,0))
endm
dword1	macro	val
	(getdword(val,4))
endm
clrc	macro
	bcf	3,0
	endm
clrz	macro
	bcf	3,2
	endm
setc	macro
	bsf	3,0
	endm
setz	macro
	bsf	3,2
	endm
skipc	macro
	btfss	3,0
	endm
skipz	macro
	btfss	3,2
	endm
skipnc	macro
	btfsc	3,0
	endm
skipnz	macro
	btfsc	3,2
	endm
# 54 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
INDF equ 00h ;# 
# 74 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
TMR0 equ 01h ;# 
# 94 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
PCL equ 02h ;# 
# 114 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
STATUS equ 03h ;# 
# 200 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
FSR equ 04h ;# 
# 220 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
GPIO equ 05h ;# 
# 308 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
PCLATH equ 0Ah ;# 
# 328 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
INTCON equ 0Bh ;# 
# 406 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
PIR1 equ 0Ch ;# 
# 454 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
TMR1 equ 0Eh ;# 
# 461 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
TMR1L equ 0Eh ;# 
# 481 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
TMR1H equ 0Fh ;# 
# 501 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
T1CON equ 010h ;# 
# 566 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
CMCON equ 019h ;# 
# 625 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
ADRESH equ 01Eh ;# 
# 645 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
ADCON0 equ 01Fh ;# 
# 729 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
OPTION_REG equ 081h ;# 
# 799 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
TRISIO equ 085h ;# 
# 849 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
PIE1 equ 08Ch ;# 
# 897 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
PCON equ 08Eh ;# 
# 931 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
OSCCAL equ 090h ;# 
# 991 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
WPU equ 095h ;# 
# 1036 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
IOC equ 096h ;# 
# 1041 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
IOCB equ 096h ;# 
# 1210 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
VRCON equ 099h ;# 
# 1270 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
EEDATA equ 09Ah ;# 
# 1275 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
EEDAT equ 09Ah ;# 
# 1308 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
EEADR equ 09Bh ;# 
# 1328 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
EECON1 equ 09Ch ;# 
# 1366 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
EECON2 equ 09Dh ;# 
# 1386 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
ADRESL equ 09Eh ;# 
# 1406 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
ANSEL equ 09Fh ;# 
# 54 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
INDF equ 00h ;# 
# 74 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
TMR0 equ 01h ;# 
# 94 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
PCL equ 02h ;# 
# 114 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
STATUS equ 03h ;# 
# 200 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
FSR equ 04h ;# 
# 220 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
GPIO equ 05h ;# 
# 308 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
PCLATH equ 0Ah ;# 
# 328 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
INTCON equ 0Bh ;# 
# 406 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
PIR1 equ 0Ch ;# 
# 454 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
TMR1 equ 0Eh ;# 
# 461 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
TMR1L equ 0Eh ;# 
# 481 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
TMR1H equ 0Fh ;# 
# 501 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
T1CON equ 010h ;# 
# 566 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
CMCON equ 019h ;# 
# 625 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
ADRESH equ 01Eh ;# 
# 645 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
ADCON0 equ 01Fh ;# 
# 729 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
OPTION_REG equ 081h ;# 
# 799 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
TRISIO equ 085h ;# 
# 849 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
PIE1 equ 08Ch ;# 
# 897 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
PCON equ 08Eh ;# 
# 931 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
OSCCAL equ 090h ;# 
# 991 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
WPU equ 095h ;# 
# 1036 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
IOC equ 096h ;# 
# 1041 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
IOCB equ 096h ;# 
# 1210 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
VRCON equ 099h ;# 
# 1270 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
EEDATA equ 09Ah ;# 
# 1275 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
EEDAT equ 09Ah ;# 
# 1308 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
EEADR equ 09Bh ;# 
# 1328 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
EECON1 equ 09Ch ;# 
# 1366 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
EECON2 equ 09Dh ;# 
# 1386 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
ADRESL equ 09Eh ;# 
# 1406 "/Applications/microchip/mplabx/v5.45/packs/Microchip/PIC10-12Fxxx_DFP/1.3.46/xc8/pic/include/proc/pic12f675.h"
ANSEL equ 09Fh ;# 
	debug_source C
	FNROOT	_main
	global	_GPIO
_GPIO	set	0x5
	global	_CMCON
_CMCON	set	0x19
	global	_GP0
_GP0	set	0x28
	global	_TRISIO
_TRISIO	set	0x85
	global	_ANSEL
_ANSEL	set	0x9F
; #config settings
	config pad_punits      = on
	config apply_mask      = off
	config ignore_cmsgs    = off
	config default_configs = off
	config default_idlocs  = off
	config FOSC = "INTRCIO"
	config WDTE = "OFF"
	config PWRTE = "ON"
	config MCLRE = "OFF"
	config BOREN = "ON"
	config CP = "OFF"
	config CPD = "OFF"
	file	"build/firmware.s"
	line	#
psect cinit,class=CODE,delta=2
global start_initialization
start_initialization:

global __initialization
__initialization:
psect cinit,class=CODE,delta=2,merge=1
global end_of_initialization,__end_of__initialization

;End of C runtime variable initialization code

end_of_initialization:
__end_of__initialization:
clrf status
ljmp _main	;jump to C main() function
psect	cstackBANK0,class=BANK0,space=1,noexec
global __pcstackBANK0
__pcstackBANK0:
?_main:	; 1 bytes @ 0x0
??_main:	; 1 bytes @ 0x0
	ds	3
;!
;!Data Sizes:
;!    Strings     0
;!    Constant    0
;!    Data        0
;!    BSS         0
;!    Persistent  0
;!    Stack       0
;!
;!Auto Spaces:
;!    Space          Size  Autos    Used
;!    COMMON            0      0       0
;!    BANK0            62      3       3

;!
;!Pointer List with Targets:
;!
;!    None.


;!
;!Critical Paths under _main in COMMON
;!
;!    None.
;!
;!Critical Paths under _main in BANK0
;!
;!    None.

;;
;;Main: autosize = 0, tempsize = 3, incstack = 0, save=0
;;

;!
;!Call Graph Tables:
;!
;! ---------------------------------------------------------------------------------
;! (Depth) Function   	        Calls       Base Space   Used Autos Params    Refs
;! ---------------------------------------------------------------------------------
;! (0) _main                                                 3     3      0       0
;!                                              0 BANK0      3     3      0
;! ---------------------------------------------------------------------------------
;! Estimated maximum stack depth 0
;! ---------------------------------------------------------------------------------
;!
;! Call Graph Graphs:
;!
;! _main (ROOT)
;!

;!Address spaces:

;!Name               Size   Autos  Total    Usage
;!BITCOMMON            0      0       0      0.0%
;!BITBANK0            62      0       0      0.0%
;!COMMON               0      0       0      0.0%
;!BANK0               62      3       3      4.8%
;!STACK                0      0       0      0.0%
;!DATA                 0      0       3      0.0%

	global	_main

;; *************** function _main *****************
;; Defined at:
;;		line 13 in file "main.c"
;; Parameters:    Size  Location     Type
;;		None
;; Auto vars:     Size  Location     Type
;;		None
;; Return value:  Size  Location     Type
;;                  1    wreg      void 
;; Registers used:
;;		wreg, status,2
;; Tracked objects:
;;		On entry : B00/0
;;		On exit  : 0/0
;;		Unchanged: 0/0
;; Data sizes:     COMMON   BANK0
;;      Params:         0       0
;;      Locals:         0       0
;;      Temps:          0       3
;;      Totals:         0       3
;;Total ram usage:        3 bytes
;; This function calls:
;;		Nothing
;; This function is called by:
;;		Startup code after reset
;; This function uses a non-reentrant model
;;
psect	maintext,global,class=CODE,delta=2,split=1,group=0
	file	"main.c"
	line	13
global __pmaintext
__pmaintext:	;psect for function _main
psect	maintext
	file	"main.c"
	line	13
	
_main:	
;incstack = 0
	callstack 8
; Regs used in _main: [wreg+status,2]
	line	15
	
l576:	
	bsf	status, 5	;RP0=1, select bank1
	clrf	(159)^080h	;volatile
	line	16
	
l578:	
	movlw	07h
	bcf	status, 5	;RP0=0, select bank0
	movwf	(25)	;volatile
	line	18
	clrf	(5)	;volatile
	line	19
	bsf	status, 5	;RP0=1, select bank1
	clrf	(133)^080h	;volatile
	line	22
	
l580:	
	bcf	status, 5	;RP0=0, select bank0
	bsf	(40/8),(40)&7	;volatile
	line	23
	
l582:	
	asmopt push
asmopt off
movlw  3
movwf	((??_main)+2)
movlw	138
movwf	((??_main)+1)
	movlw	85
movwf	((??_main))
	u17:
decfsz	((??_main)),f
	goto	u17
	decfsz	((??_main)+1),f
	goto	u17
	decfsz	((??_main)+2),f
	goto	u17
	nop2
asmopt pop

	line	25
	
l584:	
	bcf	status, 5	;RP0=0, select bank0
	bcf	(40/8),(40)&7	;volatile
	line	26
	
l586:	
	asmopt push
asmopt off
movlw  3
movwf	((??_main)+2)
movlw	138
movwf	((??_main)+1)
	movlw	85
movwf	((??_main))
	u27:
decfsz	((??_main)),f
	goto	u27
	decfsz	((??_main)+1),f
	goto	u27
	decfsz	((??_main)+2),f
	goto	u27
	nop2
asmopt pop

	goto	l580
	global	start
	ljmp	start
	callstack 0
	line	28
GLOBAL	__end_of_main
	__end_of_main:
	signat	_main,89
global	___latbits
___latbits	equ	0
	global	btemp
	btemp set 05Eh

	DABS	1,0x5E,2	;btemp
	global btemp0
	btemp0 set btemp+0
	global btemp1
	btemp1 set btemp+1
	global wtemp0
	wtemp0 set btemp+0
	global wtemp0a
	wtemp0a set btemp+1
	global ttemp0a
	ttemp0a set btemp+1
	global ltemp0a
	ltemp0a set btemp+2
	end

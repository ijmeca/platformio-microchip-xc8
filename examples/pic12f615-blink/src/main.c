#include <xc.h>

#define _XTAL_FREQ 4000000UL

#pragma config FOSC = INTOSCIO
#pragma config WDTE = OFF
#pragma config PWRTE = ON
#pragma config MCLRE = OFF
#pragma config CP = OFF
#pragma config IOSCFS = 4MHZ
#pragma config BOREN = ON

void main(void)
{
    ANSEL = 0x00;
    CMCON0 = 0x07;
    GPIO = 0x00;
    TRISIO = 0x00;

    while (1) {
        GP0 = 1;
        __delay_ms(500);
        GP0 = 0;
        __delay_ms(500);
    }
}

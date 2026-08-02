#include <xc.h>

#define _XTAL_FREQ 4000000UL

#pragma config FOSC = INTOSCIO
#pragma config WDTE = OFF
#pragma config PWRTE = ON
#pragma config MCLRE = OFF
#pragma config BOREN = ON
#pragma config LVP = OFF
#pragma config CPD = OFF
#pragma config CP = OFF

void main(void)
{
    CMCON = 0x07;
    PORTB = 0x00;
    TRISB = 0x00;

    while (1) {
        RB0 = 1;
        __delay_ms(500);
        RB0 = 0;
        __delay_ms(500);
    }
}

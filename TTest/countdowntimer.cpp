#include "countdowntimer.h"


CountDownTimer::CountDownTimer(QTimer *parent) : QTimer(parent)
{
    this->start(1000);

}

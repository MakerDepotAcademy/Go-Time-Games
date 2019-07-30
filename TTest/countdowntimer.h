#ifndef COUNTDOWNTIMER_H
#define COUNTDOWNTIMER_H

#include <QTimer>

class CountDownTimer : public QTimer
{
    Q_OBJECT
public:
    explicit CountDownTimer(QTimer *parent = nullptr);
    QTimer timer;

signals:

public slots:

};

#endif // COUNTDOWNTIMER_H

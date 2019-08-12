#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "countdowntimer.h"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
    CountDownTimer   *timer;
    void updateCountdown();

private:
    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H

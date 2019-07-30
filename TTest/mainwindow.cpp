#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "countdowntimer.h"
#include <QtCore>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    CountDownTimer *timer = new CountDownTimer();

    connect(timer, SIGNAL(timeout()), this, SLOT(updateCountdown()));
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::updateCountdown()
{
     ui->countdown->setText(QString::number(timer->remainingTime()));
    //    this->set   setHMS(0,1,0);
    //do something along the lines of ui->countdown->setText(....);
}

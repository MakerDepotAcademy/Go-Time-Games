#ifndef QTQUICK2TEST_PLUGIN_H
#define QTQUICK2TEST_PLUGIN_H

#include <QQmlExtensionPlugin>

class QTQuick2TestPlugin : public QQmlExtensionPlugin
{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID QQmlExtensionInterface_iid)

public:
    void registerTypes(const char *uri) override;
};

#endif // QTQUICK2TEST_PLUGIN_H

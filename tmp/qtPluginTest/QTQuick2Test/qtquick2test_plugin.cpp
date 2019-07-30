#include "qtquick2test_plugin.h"
#include "myitem.h"

#include <qqml.h>

void QTQuick2TestPlugin::registerTypes(const char *uri)
{
    // @uri com.mycompany.qmlcomponents
    qmlRegisterType<MyItem>(uri, 1, 0, "MyItem");
}


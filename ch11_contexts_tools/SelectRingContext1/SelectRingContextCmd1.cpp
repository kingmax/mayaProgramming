#include "selectRingContextCmd1.h"

#include <maya/MPxContext.h>
#include <maya/MPxContextCommand.h>

/*
class SelectRingContextCmd1 : public MPxContextCommand
{
public:
	virtual MPxContext *makeObj();
	static void *creator();
};
*/

MPxContext *SelectRingContextCmd1::makeObj()
{
	return new SelectRingContext1();
}

void *SelectRingContextCmd1::creator()
{
	return new SelectRingContextCmd1;
}


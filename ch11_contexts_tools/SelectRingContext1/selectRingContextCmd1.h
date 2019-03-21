#pragma once
#include "SelectRingContext1.h"
#include <maya/MPxContextCommand.h>

class SelectRingContextCmd1 : public MPxContextCommand
{
public:
	virtual MPxContext *makeObj();
	static void *creator();
};
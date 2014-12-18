package com.silvermoon.client;

import android.graphics.Point;

import com.silvermoon.client.GruntMessages.msgMapElement1;

public class MapElement implements IMapElement
{
    public msgMapElement1 msgMapElement;

    @Override
    public Point getPoint() {
        return null;
    }

    @Override
    public int getHeight() {
        return 0;
    }

    @Override
    public int getWidth() {
        return 0;
    }
}

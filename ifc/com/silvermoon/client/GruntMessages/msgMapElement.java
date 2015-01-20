package com.silvermoon.client.GruntMessages;

import com.perblue.grunt.translate.GruntMessage;
import java.util.List;

public class msgMapElement extends GruntMessage
{
    public String elementId;

    public List<msgAction> availableActions;

    public List<msgDisplayLayer> displayLayers;
}

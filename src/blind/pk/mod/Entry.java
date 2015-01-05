package blind.pk.mod;

import com.silvermoon.client.GameController;
import com.silvermoon.client.GruntMessages.*;
import com.silvermoon.client.MapElement;
import com.silvermoon.client.PKMain2;

import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

public class Entry {

    public static PKMain2 pk;

    private static Boolean hasDisplayLayer(msgMapElement element, String layerName) {
        if (element == null || layerName == null)
            return false;
        Iterator<msgDisplayLayer> i = element.displayLayers.iterator();
        while (i.hasNext())
            if (layerName.equals(i.next().info))
                return true;
        return false;
    }

    // returns true when action was picked.
    public static boolean autoPickAction(GameController controller, MapElement mapElement) {
        List<msgAction> actionsList = mapElement.msgMapElement.availableActions;
        Iterator<msgAction> iterator = actionsList.iterator();
        Map<String, msgAction> map = new HashMap<String, msgAction>();
        while (iterator.hasNext()) {
            msgAction act = iterator.next();
            map.put(act.command, act);
        }
        msgAction act;
        act = map.get("PICKUP_ALL");
        if (act == null)
            act = map.get("PICKUP");
//        if (act == null) {
//            act = map.get("COLLECT_SNOW");
//            if (act != null && !hasDisplayLayer(mapElement.msgMapElement, "mourning_tree_snow"))
//                act = null;
//        }
        if (act == null)
            act = map.get("PICKUP_ELEMENT");
        if (act == null)
            act = map.get("PICK"); // Harvest
        if (act == null)
            act = map.get("HARVEST_ELEMENT");
        if (act == null)
            act = map.get("CHOP_DOWN");
        if (act == null)
            act = map.get("BOARD_AIRSHIP");
        if (act == null) {
            act = map.get("ATTACK");
            if (act != null)
                if(!mapElement.msgMapElement.elementId.startsWith("Mon") &&
                   !mapElement.msgMapElement.elementId.startsWith("MAS")) {

                    act = null;
                }
        }
//        CALL_PHILOSTRATUS
        if (act != null)
        {
            pk.sendMapElementAction(act, mapElement.msgMapElement.elementId);
            return true;
        }
        return false;
    }
}
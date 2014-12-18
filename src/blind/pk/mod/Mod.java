package blind.pk.mod;

import com.silvermoon.client.GruntMessages.*;
import com.silvermoon.client.MapElement;

import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

public class Mod {
    public static int autoPickAction(MapElement mapElement) {
        int res = -1;
        List actionsList = mapElement.msgMapElement.availableActions;
        Iterator<msgAction1> iterator = actionsList.iterator();
        Map<String, Integer> map = new HashMap<String, Integer>();
        int i = 0;
        while (iterator.hasNext()) {
            map.put(iterator.next().ActionName, new Integer(i));
            ++i;
        }
        if (map.containsKey("PICKUP_ALL")) return map.get("PICKUP_ALL");
        if (map.containsKey("PICKUP")) return map.get("PICKUP");

        return res;
    }
}
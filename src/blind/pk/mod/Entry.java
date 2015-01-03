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

    // returns true when action was picked.
    public static boolean autoPickAction(GameController controller, MapElement mapElement) {
        List<msgAction1> actionsList = mapElement.msgMapElement.availableActions;
        Iterator<msgAction1> iterator = actionsList.iterator();
        Map<String, msgAction1> map = new HashMap<String, msgAction1>();
        while (iterator.hasNext()) {
            msgAction1 act = iterator.next();
            map.put(act.ActionName, act);
        }
        msgAction1 act;
        act = map.get("PICKUP_ALL");
        if (act == null) {
            act = map.get("PICKUP");
        }

        if (act != null)
        {
            pk.sendMapElementAction(act, mapElement.msgMapElement.globalId);
            return true;
        }
        return false;
    }
}
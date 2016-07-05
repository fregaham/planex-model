package org.foobarter.planex.model;

import java.util.List;
import java.util.Map;

/**
 * Created by marcho on 03/07/16.
 */
public class Entity {
    Snapshot latestSnapshot;

    List<Flow> inputFlows;
    List<Flow> outputFlows;

    Map<Good, Long> capacity;

    List<OverflowEvent> overflows;
    List<UnderflowEvent> underflows;
}

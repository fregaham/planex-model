package org.foobarter.planex.model;

import java.util.Map;

/**
 * Created by marcho on 03/07/16.
 */
public class Snapshot {
    long timestamp;
    Map<Good, Long> values;
}

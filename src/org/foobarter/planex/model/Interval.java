package org.foobarter.planex.model;

import java.util.Collection;

/**
 * Created by marcho on 03/07/16.
 */
public enum Interval {

    SECOND(1L),
    MINUTE(60L),
    HOUR(3600L);

    long value;

    Interval(long value) {
        this.value = value;
    }

    private static Interval[] reverseValues = {HOUR, MINUTE, SECOND};

    public static Interval[] reverseValues() {
        return reverseValues;
    }
}

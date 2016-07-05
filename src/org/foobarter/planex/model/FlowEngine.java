package org.foobarter.planex.model;

import java.util.Collection;
import java.util.LinkedHashMap;
import java.util.LinkedList;
import java.util.List;

/**
 * Created by marcho on 03/07/16.
 */
public class FlowEngine {

    static final int intervalTypes = Interval.values().length;
    static final int goodTypes = Good.values().length;

    public static void computeUnderAndOverflows(EventQueue queue, Entity entity) {
        // we expect the intervals are such that the largest is always the lcd of all the others (e.g. 10, 100, 1000). lcd = 1000

        long sums[][] = new long[goodTypes][intervalTypes];

        for (Flow flow : entity.inputFlows) {
            sums[flow.good.ordinal()][flow.interval.ordinal()] += flow.amount;
        }

        for (Flow flow : entity.inputFlows) {
            sums[flow.good.ordinal()][flow.interval.ordinal()] -= flow.amount;
        }

        for (int good = 0; good < goodTypes; ++good) {
            for (int interval = intervalTypes - 1; interval >= 0; -- interval) {

            }
        }

     /*   long intervalLcd[] = new long[goodTypes];
        long sums[] = new long[goodTypes];

        for (int i = 0; i < goodTypes; ++i) {
            intervalLcd[i] = 0;
            sums[i] = 0;
        }

        for (Flow flow : entity.inputFlows) {
            int ordinal = flow.good.ordinal();
            long interval = flow.interval;
            intervalLcd[ordinal] = Long.max(intervalLcd[ordinal], interval);
        }

        for (Flow flow : entity.outputFlows) {
            int ordinal = flow.good.ordinal();
            long interval = flow.interval;
            intervalLcd[ordinal] = Long.max(intervalLcd[ordinal], interval);
        }

        for (Flow flow : entity.inputFlows) {
            int ordinal = flow.good.ordinal();
            sums[ordinal] += flow.amount * (intervalLcd[ordinal] / flow.interval);
        }

        for (Flow flow : entity.outputFlows) {
            int ordinal = flow.good.ordinal();
            sums[ordinal] -= flow.amount * (intervalLcd[ordinal] / flow.interval);
        }

        for (int i = 0; i < goodTypes) {
            if (sums[i] < 0) {

            }
        }*/
    }

    public static void computeUnderAndOverflows(EventQueue queue, Collection<Entity> entities) {

    }
}

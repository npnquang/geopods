package org.example.stream;

import java.util.Map;

public class POSTBody {
    private int uid;
    private double timestamp;
    private String msg_type;
    private Map<String, Float> data;

    public int getUid() {
        return uid;
    }

    public double getTimestamp() {
        return timestamp;
    }

    public String getMsg_type() {
        return msg_type;
    }

    public Map<String, Float> getData() {
        return data;
    }
}

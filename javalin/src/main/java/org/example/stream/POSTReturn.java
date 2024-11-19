package org.example.stream;

public class POSTReturn {
    private float output;
    private double timestamp;
    private double server_latency;

    public POSTReturn(float output, double timestamp, double server_latency) {
        this.output = output;
        this.timestamp = timestamp;
        this.server_latency = server_latency;
    }

    public float getOutput() {
        return output;
    }

    public double getTimestamp() {
        return timestamp;
    }

    public double getServer_latency() {
        return server_latency;
    }

}
